import torch
import numpy as np
import os


class MultiAttrRanking:

    def __init__(self, a, TX, b, file_path):
        self.TA = a
        self.TX = TX
        self.TB = b
        self.file_path = file_path
        self.load = eval(self.file_path[-1])

    def rank(self, k=1):
        try:
            o1_size = 4
            o2_size = 4
            if not isinstance(k, int) or k <= 0 or k > 16:
                raise ValueError(
                    "k must be a positive integer not exceeding 16")
            if self.TX.shape[0:] != (4, 4):
                raise ValueError("Tensor X must have shape (4, 4)")
            if self.TA.shape[0:] != (4, 4, 4, 2, 100):
                raise ValueError("Tensor A must have shape (4, 4, 4, 2, 100)")
            if self.TB.shape[0:] != (4, 2, 100):
                raise ValueError("Tensor B must have shape (4, 2, 100)")
            match_ratio_array = np.ones((o1_size, o2_size))

            for index_1 in range(o1_size):
                for index_2 in range(o2_size):
                    subtensorA = self.TA[index_1, index_2, :, :, :]
                    match_ratio_array[index_1, index_2] = self.cal_match_ratio(
                        subtensorA, self.TX, index_1, index_2)

            positions = []
            values = []
            visited = np.zeros((o1_size, o2_size))
            for _ in range(k):
                max_position = None
                max_value = np.min(match_ratio_array) - 1
                for i in range(o1_size):
                    for j in range(o2_size):
                        if match_ratio_array[i][j] > max_value and visited[i][
                                j] == 0:
                            max_value = match_ratio_array[i][j]
                            max_position = (i, j)
                if max_position is not None:
                    visited[max_position[0]][max_position[1]] = 1
                    positions.append(max_position)
                    values.append(max_value)
            return positions, values

        except ValueError as e:
            print("Error occurred during ranking:", e)
            return None, None

        except Exception as e:
            print("An unexpected error occurred:", e)
            return None, None

    def cal_match_ratio(self, subtensorA, TX, o1_index, o2_index):
        try:
            load = self.load
            return (
                1 -
                torch.norm(subtensorA[load, :, :] * TX[o1_index][o2_index] -
                           self.TB[load, :, :]) /
                torch.norm(self.TB[load, :, :]))
        except Exception as e:
            raise
