# -*- coding: utf-8 -*-
import torch
import pandas as pd
import numpy as np
import os


class BearingTensor:

    def __init__(self):
        self.info1 = ['normal_', '007_', '014_', '021_']
        self.o1 = len(self.info1)
        self.info2 = ['B', 'IR', 'OR@3_', 'OR@6_']
        self.o2 = len(self.info2)
        self.info3 = ['0', '1', '2', '3']
        self.o3 = len(self.info3)
        self.info4 = ['de', 'fe']
        self.o4 = len(self.info4)
        self.info5 = range(0, 100)
        self.o5 = len(self.info5)

    def build_tensor_B_with_xlsx(self, file_name):  # freq
        try:
            if not file_name.lower().endswith('.xlsx'):
                raise ValueError("File is not in .xlsx format.")

            prefix = os.path.splitext(file_name)[0]
            tensor_b = torch.zeros((self.o3, self.o4, self.o5))
            load = prefix[-1]
            excel_file_path = file_name
            df = pd.read_excel(excel_file_path)

            if not all(col in df.columns for col in self.info4):
                raise ValueError(
                    "Columns required for processing not found in the dataframe."
                )

            for col in self.info4:
                if col not in df.columns:
                    raise ValueError(
                        f"Column '{col}' is missing in the dataframe.")

                if len(df[col]) > 100:
                    raise ValueError(
                        f"Column '{col}' has more than 100 rows of data.")

                if len(df[col]) < 100:
                    raise ValueError(
                        f"Column '{col}' has less than 100 rows of data.")

                if df[col].isnull().any():
                    raise ValueError(
                        f"Column '{col}' contains missing values.")

            for index_4, value4 in enumerate(self.info4):
                accr_fre = np.abs(np.fft.fft(df[value4]))
                for index_5, value5 in enumerate(self.info5):
                    acc_fre = accr_fre[value5]
                    tensor_b[eval(load), index_4, index_5] += acc_fre

            return tensor_b

        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")
            return None

        except pd.errors.ParserError:
            print(
                "Error parsing the Excel file. Please ensure it is formatted correctly."
            )
            return None

        except ValueError as ve:
            print(ve)
            return None

        except Exception as e:
            print("An error occurred:", e)
            return None
