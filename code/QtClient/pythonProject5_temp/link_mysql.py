import pymysql
import datetime


def to_mysql(res, m, b):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host="127.0.0.1", database="argbearing_db", user='argSysAdmin', password='argbearing', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute("insert into machines(machineNumber,bearingNumber) values(%d, %d);" % (m, b))
    except Exception:
        conn.rollback()
    conn.commit()
    last_sn = "SELECT MAX(detectSN) FROM bearinginfo"
    cur.execute(last_sn)
    result = cur.fetchone()
    if result[0] is not None:
        detectSN = result[0] + 1
    else:
        detectSN = 1
    try:
        cur.execute("insert into bearinginfo(detectSN,machineNumber,bearingNumber,faultDia1,faultLoc1,faultScore1," 
                "faultDia2,faultLoc2,faultScore2,faultDia3,faultLoc3,faultScore3,detectTime) "
                "values(%d, %d, %d, %d, %d, %f, %d, %d, %f, %d, %d, %f, '%s');" %
                (detectSN, m, b, res[0][0][0], res[0][0][1], res[1][0],
                res[0][1][0], res[0][1][1], res[1][1],
                res[0][2][0], res[0][2][1], res[1][2], time))
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()


def to_mysql_h_2(m, b):
    conn = pymysql.connect(host="127.0.0.1", database="argbearing_db", user='argSysAdmin', password='argbearing', charset='utf8')
    cur = conn.cursor()
    res = []
    try:
        cur.execute(
            "SELECT faultDia1, faultLoc1, faultScore1,"
            "faultDia2, faultLoc2, faultScore2,"
            "faultDia3, faultLoc3, faultScore3 FROM bearinginfo WHERE machineNumber = %d AND bearingNumber = %d "
            "ORDER BY detectSN DESC" % (
            m, b))
        result = cur.fetchall()
        res = result[0]
        print(res)
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()
    return res


def to_mysql_h_3():
    conn = pymysql.connect(host="127.0.0.1", database="argbearing_db", user='argSysAdmin', password='argbearing', charset='utf8')
    cur = conn.cursor()
    res = []
    try:
        cur.execute(
            "SELECT detectTime, machineNumber, bearingNumber,faultDia1, faultLoc1, faultScore1,"
            "faultDia2, faultLoc2, faultScore2,"
            "faultDia3, faultLoc3, faultScore3 FROM bearinginfo  "
            "ORDER BY detectTime ASC")
        result = cur.fetchall()
        res = result
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()
    return res


def to_mysql_h_4(m, b):
    conn = pymysql.connect(host="127.0.0.1", database="argbearing_db", user='argSysAdmin', password='argbearing', charset='utf8')
    cur = conn.cursor()
    res = []
    try:
        cur.execute(
            "SELECT detectTime, machineNumber, bearingNumber,faultDia1, faultLoc1, faultScore1,"
            "faultDia2, faultLoc2, faultScore2,"
            "faultDia3, faultLoc3, faultScore3 FROM bearinginfo WHERE machineNumber = %d AND bearingNumber = %d "
            "ORDER BY detectSN DESC" % (m, b))
        result = cur.fetchall()
        res = result
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()
    return res


def to_my_sql_rul(m, b, rul_data):
    conn = pymysql.connect(host="127.0.0.1", database="argbearing_db", user='argSysAdmin', password='argbearing', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT rul FROM rul_pred WHERE machineNumber = %d AND bearingNumber = %d ORDER BY predictSN ASC" % (m, b))
        result = cur.fetchall()
        for i in range(0, len(result)):
            rul_data.append((result[i][0]))
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()


def to_mysql_h_3_rul():
    conn = pymysql.connect(host="127.0.0.1", database="argbearing_db", user='argSysAdmin', password='argbearing', charset='utf8')
    cur = conn.cursor()
    res = []
    try:
        cur.execute(
            "SELECT predictTime, machineNumber, bearingNumber, rul FROM rul_pred "
            "ORDER BY predictTime ASC")
        result = cur.fetchall()
        res = result
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()
    return res


def to_mysql_h_4_rul(m, b):
    conn = pymysql.connect(host="127.0.0.1", database="argbearing_db", user='argSysAdmin', password='argbearing', charset='utf8')
    cur = conn.cursor()
    res = []
    try:
        cur.execute(
            "SELECT predictTime, machineNumber, bearingNumber, rul FROM rul_pred "
            " WHERE machineNumber = %d AND bearingNumber = %d "
            "ORDER BY predictSN DESC" % (m, b))
        result = cur.fetchall()
        res = result
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()
    return res




