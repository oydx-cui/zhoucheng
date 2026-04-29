from feature_extraction import BearingTensor
from feature_mapping import TensorSolution
from ranking import MultiAttrRanking
from progress.bar import Bar
import torch


class ModelAssessment_freq:

    def __init__(self):
        self.tensor_A = torch.load(r'tensor\tensor_a_freq_600.pt')

    def process(self, file_path, id, output_num):
        tensor_B = BearingTensor().build_tensor_B(file_path, id)
        TX = TensorSolution(self.tensor_A, tensor_B,
                            eval(file_path[-1])).ORM(4)
        rank = MultiAttrRanking(self.tensor_A, TX, tensor_B, file_path, 4, 5)
        rank.cal_match_ratio_array()
        pos, val = rank.return_match_ratio_pos(output_num)
        return pos, val

    def certain_acc_test(self, file_path, test_start, test_num, output_num,
                         pos1, pos2):
        first_corr_num = 0
        second_corr_num = 0
        bar = Bar('Testing:', max=test_num)
        for test_id in range(test_start, test_start + test_num):
            res_pos, res_val = self.process(file_path, test_id, output_num)
            if pos1 != 0:
                if res_pos[0][0] == pos1 and res_pos[0][1] == pos2:
                    first_corr_num += 1
                    second_corr_num += 1
                else:
                    for i in range(1, output_num):
                        if res_pos[i][0] == pos1 and res_pos[i][1] == pos2:
                            second_corr_num += 1
                            break
            else:
                if res_pos[0][0] == pos1:
                    first_corr_num += 1
                    second_corr_num += 1
                else:
                    for i in range(1, output_num):
                        if res_pos[i][0] == pos1:
                            second_corr_num += 1
                            break
            bar.next()
        bar.finish()
        return (first_corr_num / test_num), (second_corr_num / test_num)

    def all_acc_test(self, test_start, test_num, output_num):
        info1 = ['normal_', '007_', '014_', '021_']
        info2 = ['B', 'IR', 'OR@3_', 'OR@6_', 'OR@12_']
        info3 = ['0', '1', '2', '3']
        first_corr_num = 0
        second_corr_num = 0
        curr_file = ""
        bar = Bar('Testing:', max=test_num * 72)
        for index_1, value1 in enumerate(info1):
            for index_2, value2 in enumerate(info2):
                if index_2 == 2 or index_2 == 4:
                    if index_1 == 2:
                        continue
                for index_3, value3 in enumerate(info3):
                    if index_1 == 0:
                        curr_file = 'xlsx_file\\' + value1 + value3
                    else:
                        curr_file = 'xlsx_file\\' + value2 + value1 + value3
                    for test_id in range(test_start, test_start + test_num):
                        res_pos, res_val = self.process(
                            curr_file, test_id, output_num)
                        if index_1 != 0:
                            if res_pos[0][0] == index_1 and res_pos[0][
                                    1] == index_2:
                                first_corr_num += 1
                                second_corr_num += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1 and res_pos[i][
                                            1] == index_2:
                                        second_corr_num += 1
                                        break
                        else:
                            if res_pos[0][0] == index_1:
                                first_corr_num += 1
                                second_corr_num += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1:
                                        second_corr_num += 1
                                        break
                        bar.next()
        bar.finish()
        return (first_corr_num / (test_num * 72)), (second_corr_num /
                                                    (test_num * 72))

    def all_acc_test_print(self, test_start, test_num, output_num):
        info1 = ['normal_', '007_', '014_', '021_']
        info2 = ['B', 'IR', 'OR@3_', 'OR@6_', 'OR@12_']
        info3 = ['0', '1', '2', '3']
        first_corr_num = 0
        second_corr_num = 0
        curr_file = ""
        for index_1, value1 in enumerate(info1):
            for index_2, value2 in enumerate(info2):
                if index_2 == 2 or index_2 == 4:
                    if index_1 == 2:
                        continue
                for index_3, value3 in enumerate(info3):
                    if index_1 == 0:
                        curr_file = 'xlsx_file\\' + value1 + value3
                    else:
                        curr_file = 'xlsx_file\\' + value2 + value1 + value3
                    first_corr_num_temp = 0
                    second_corr_num_temp = 0
                    for test_id in range(test_start, test_start + test_num):
                        res_pos, res_val = self.process(
                            curr_file, test_id, output_num)
                        if index_1 != 0:
                            if res_pos[0][0] == index_1 and res_pos[0][
                                    1] == index_2:
                                first_corr_num += 1
                                first_corr_num_temp += 1
                                second_corr_num += 1
                                second_corr_num_temp += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1 and res_pos[i][
                                            1] == index_2:
                                        second_corr_num += 1
                                        second_corr_num_temp += 1
                                        break
                        else:
                            if res_pos[0][0] == index_1:
                                first_corr_num += 1
                                first_corr_num_temp += 1
                                second_corr_num += 1
                                second_corr_num_temp += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1:
                                        second_corr_num += 1
                                        second_corr_num_temp += 1
                                        break
                    print(curr_file, ":", end=" ")
                    print("First acc:", (first_corr_num_temp / test_num),
                          "Second acc:", (second_corr_num_temp / test_num))
        return (first_corr_num / (test_num * 72)), (second_corr_num /
                                                    (test_num * 72))


class ModelAssessment_tf:

    def __init__(self, tensor_A_file_num):
        self.tensor_A_file_num = tensor_A_file_num
        print("Building tensor...")
        self.tensor_A = BearingTensor().build_tensor_A_with_tf(
            self.tensor_A_file_num)
        print("Tensor is built!")

    def process(self, file_path, id, output_num):
        tensor_B = BearingTensor().build_tensor_B_with_tf(file_path, id)
        TX = TensorSolution(self.tensor_A, tensor_B,
                            eval(file_path[-1])).ORM_tf(4)
        rank = MultiAttrRanking(self.tensor_A, TX, tensor_B, file_path, 4, 5)
        rank.cal_match_ratio_array_tf()
        pos, val = rank.return_match_ratio_pos(output_num)
        return pos, val

    def certain_acc_test(self, file_path, test_start, test_num, output_num,
                         pos1, pos2):
        first_corr_num = 0
        second_corr_num = 0
        bar = Bar('Testing:', max=test_num)
        for test_id in range(test_start, test_start + test_num):
            res_pos, res_val = self.process(file_path, test_id, output_num)
            if pos1 != 0:
                if res_pos[0][0] == pos1 and res_pos[0][1] == pos2:
                    first_corr_num += 1
                    second_corr_num += 1
                else:
                    for i in range(1, output_num):
                        if res_pos[i][0] == pos1 and res_pos[i][1] == pos2:
                            second_corr_num += 1
                            break
            else:
                if res_pos[0][0] == pos1:
                    first_corr_num += 1
                    second_corr_num += 1
                else:
                    for i in range(1, output_num):
                        if res_pos[i][0] == pos1:
                            second_corr_num += 1
                            break
            bar.next()
        bar.finish()
        return (first_corr_num / test_num), (second_corr_num / test_num)

    def all_acc_test(self, test_start, test_num, output_num):
        info1 = ['normal_', '007_', '014_', '021_']
        info2 = ['B', 'IR', 'OR@3_', 'OR@6_', 'OR@12_']
        info3 = ['0', '1', '2', '3']
        first_corr_num = 0
        second_corr_num = 0
        curr_file = ""
        bar = Bar('Testing:', max=test_num * 72)
        for index_1, value1 in enumerate(info1):
            for index_2, value2 in enumerate(info2):
                if index_2 == 2 or index_2 == 4:
                    if index_1 == 2:
                        continue
                for index_3, value3 in enumerate(info3):
                    if index_1 == 0:
                        curr_file = 'xlsx_file\\' + value1 + value3
                    else:
                        curr_file = 'xlsx_file\\' + value2 + value1 + value3
                    for test_id in range(test_start, test_start + test_num):
                        res_pos, res_val = self.process(
                            curr_file, test_id, output_num)
                        if index_1 != 0:
                            if res_pos[0][0] == index_1 and res_pos[0][
                                    1] == index_2:
                                first_corr_num += 1
                                second_corr_num += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1 and res_pos[i][
                                            1] == index_2:
                                        second_corr_num += 1
                                        break
                        else:
                            if res_pos[0][0] == index_1:
                                first_corr_num += 1
                                second_corr_num += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1:
                                        second_corr_num += 1
                                        break
                        bar.next()
        bar.finish()
        return (first_corr_num / (test_num * 72)), (second_corr_num /
                                                    (test_num * 72))

    def all_acc_test_print(self, test_start, test_num, output_num):
        info1 = ['normal_', '007_', '014_', '021_']
        info2 = ['B', 'IR', 'OR@3_', 'OR@6_', 'OR@12_']
        info3 = ['0', '1', '2', '3']
        first_corr_num = 0
        second_corr_num = 0
        curr_file = ""
        for index_1, value1 in enumerate(info1):
            for index_2, value2 in enumerate(info2):
                if index_2 == 2 or index_2 == 4:
                    if index_1 == 2:
                        continue
                for index_3, value3 in enumerate(info3):
                    if index_1 == 0:
                        curr_file = 'xlsx_file\\' + value1 + value3
                    else:
                        curr_file = 'xlsx_file\\' + value2 + value1 + value3
                    first_corr_num_temp = 0
                    second_corr_num_temp = 0
                    for test_id in range(test_start, test_start + test_num):
                        res_pos, res_val = self.process(
                            curr_file, test_id, output_num)
                        if index_1 != 0:
                            if res_pos[0][0] == index_1 and res_pos[0][
                                    1] == index_2:
                                first_corr_num += 1
                                first_corr_num_temp += 1
                                second_corr_num += 1
                                second_corr_num_temp += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1 and res_pos[i][
                                            1] == index_2:
                                        second_corr_num += 1
                                        second_corr_num_temp += 1
                                        break
                        else:
                            if res_pos[0][0] == index_1:
                                first_corr_num += 1
                                first_corr_num_temp += 1
                                second_corr_num += 1
                                second_corr_num_temp += 1
                            else:
                                for i in range(1, output_num):
                                    if res_pos[i][0] == index_1:
                                        second_corr_num += 1
                                        second_corr_num_temp += 1
                                        break
                    print(curr_file, ":", end=" ")
                    print("First acc:", (first_corr_num_temp / test_num),
                          "Second acc:", (second_corr_num_temp / test_num))
        return (first_corr_num / (test_num * 72)), (second_corr_num /
                                                    (test_num * 72))


if __name__ == '__main__':
    file_path = 'xlsx_file\\B007_0'
    model_freq = ModelAssessment_freq()
    print(model_freq.process(file_path, 601, 3))

    # acc1 = model_freq.certain_acc_test(file_path=file_path,
    #                                    test_start=601,
    #                                    test_num=50,
    #                                    output_num=3,
    #                                    pos1=1,
    #                                    pos2=0)
    # print("First acc:", acc1[0])
    # print("Second acc:", acc1[1])

    # acc2 = model_freq.all_acc_test_print(test_start=601,
    #                                      test_num=50,
    #                                      output_num=3)
    # print("First acc:", acc2[0])
    # print("Second acc:", acc2[1])

    # print()
    # model_tf = ModelAssessment_tf(200)
    # acc3 = model_tf.certain_acc_test(file_path=file_path,
    #                                  test_start=201,
    #                                  test_num=800,
    #                                  output_num=3,
    #                                  pos1=1,
    #                                  pos2=0)
    # print("First acc:", acc3[0])
    # print("Second acc:", acc3[1])

    # acc4 = model_tf.all_acc_test_print(test_start=201,
    #                                    test_num=800,
    #                                    output_num=3)
    # print("First acc:", acc4[0])
    # print("Second acc:", acc4[1])
