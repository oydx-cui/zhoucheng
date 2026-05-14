from feature_extraction import BearingTensor
from feature_mapping import TensorSolution
from ranking import MultiAttrRanking
import torch
import os


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
