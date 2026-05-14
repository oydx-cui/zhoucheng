 # -*- coding: utf-8 -*-
from feature_extraction import BearingTensor
from feature_mapping import TensorSolution
from ranking import MultiAttrRanking
import torch
import os
import mysql.connector
from datetime import datetime
import sys
import json
os.chdir(r'E:\exp comter\remote_interface')

class Detection:

    def __init__(self):
        self.tensor_A = torch.load(r'tensor\tensor_a_freq_600_exOR12.pt')

    def detect(self, file_name, output_num):
        prefix = os.path.splitext(file_name)[0]
        tensor_B = BearingTensor().build_tensor_B_with_xlsx(file_name)
        if tensor_B == None:
            return None, None
        TX = TensorSolution(self.tensor_A, tensor_B, eval(prefix[-1])).ORM()
        ran = MultiAttrRanking(self.tensor_A, TX, tensor_B, prefix)
        pos, val = ran.rank(output_num)
        return pos, val


def insert_into_db(machine_id, bearing_id, pos, val):
    try:
        # Database connection configuration
        db_config = {
            'user': 'argSysAdmin',
            'password': 'argbearing',
            'host': 'localhost',
            'database': 'argbearing_db'
        }

        # Establish the database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Get the maximum detectSN value
        max_sn_query = "SELECT MAX(detectSN) FROM bearinginfo"
        cursor.execute(max_sn_query)
        result = cursor.fetchone()
        max_detect_sn = result[0] if result[0] is not None else 0
        new_detect_sn = max_detect_sn + 1

        # Insert the fault detection results into the database
        detect_time = datetime.now()
        insert_query = """
            INSERT INTO bearinginfo (
                detectSN, machineNumber, bearingNumber, 
                faultDia1, faultLoc1, faultScore1, 
                faultDia2, faultLoc2, faultScore2, 
                faultDia3, faultLoc3, faultScore3, 
                detectTime
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query,
                       (new_detect_sn, machine_id, bearing_id, pos[0][0],
                        pos[0][1], val[0], pos[1][0], pos[1][1], val[1],
                        pos[2][0], pos[2][1], val[2], detect_time))
        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)


def process(machine_id, bearing_id):
    det = Detection()
    dir = f'test_example\\machine-{machine_id}\\bearing-{int(bearing_id):02d}'
    name = os.listdir(dir)[0]
    pos, val = det.detect(file_name=os.path.join(dir, name), output_num=3)
    return pos, val


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python anomaly_detection.py process <machine_id> <bearing_id>"
        )
        sys.exit(1)

    command = sys.argv[1]
    machine_id = sys.argv[2]
    bearing_id = sys.argv[3]

    if command == "process":
        pos, val = process(machine_id, bearing_id)
        insert_into_db(machine_id, bearing_id, pos, val)
        result = {
            "machine_id": machine_id,
            "bearing_id": bearing_id,
            "faultDia1": pos[0][0],
            "faultLoc1": pos[0][1],
            "faultScore1": val[0],
            "faultDia2": pos[1][0],
            "faultLoc2": pos[1][1],
            "faultScore2": val[1],
            "faultDia3": pos[2][0],
            "faultLoc3": pos[2][1],
            "faultScore3": val[2]
        }
        print(json.dumps(result))
    else:
        print(json.dumps({}))
        sys.exit(1)
