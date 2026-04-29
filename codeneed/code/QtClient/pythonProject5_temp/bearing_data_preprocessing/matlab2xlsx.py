import scipy.io
import pandas as pd
from tqdm import tqdm
import os


def loadmatdata(mat_file_path):
    # 使用loadmat函数加载.mat文件
    mat_data = scipy.io.loadmat(mat_file_path)

    # 输出.mat文件中的所有变量名
    print("Variable names in the .mat file:", mat_data.keys())

    # 替换为你想要读取的变量名
    de = 'DE_time'
    fe = 'FE_time'

    for key in mat_data:
        if key.endswith(de):
            de_value = mat_data[key]
            break

    for key in mat_data:
        if key.endswith(fe):
            fe_value = mat_data[key]
            break

    print(f"Value of '{de}': {de_value}")
    print(f"Value of '{fe}': {fe_value}")

    return de_value, fe_value


def mat2xlsx(excel_file_root_path, de_value, fe_value):
    # 检查目录是否存在
    if not os.path.exists(excel_file_root_path):
        # 如果目录不存在，则创建目录
        os.makedirs(excel_file_root_path)
        print(f"Directory '{excel_file_root_path}' created!")

    # 将array分组，每组100个数据
    group_size = 100
    num_groups = len(de_value) // group_size

    # 创建Excel表格并写入数据
    for group_num in tqdm(range(1, num_groups + 1), desc="Processing groups"):
        start_index = (group_num - 1) * group_size
        end_index = group_num * group_size

        # 创建DataFrame
        data = {
            'sn': range(1, group_size + 1),
            'de': de_value[start_index:end_index].flatten(),
            'fe': fe_value[start_index:end_index].flatten(),
        }

        df = pd.DataFrame(data)

        # 将DataFrame写入Excel文件
        excel_file_path = f'{excel_file_root_path}\data{group_num}.xlsx'
        df.to_excel(excel_file_path, index=False)


to_read_data = [
    r'data\12kde\Outer Race\Orthogonal\0007\OR007@3_0.mat',
    r'data\12kde\Outer Race\Orthogonal\0007\OR007@3_1.mat',
    r'data\12kde\Outer Race\Orthogonal\0007\OR007@3_2.mat',
    r'data\12kde\Outer Race\Orthogonal\0007\OR007@3_3.mat',
    r'data\12kde\Outer Race\Orthogonal\0021\OR021@3_0.mat',
    r'data\12kde\Outer Race\Orthogonal\0021\OR021@3_1.mat',
    r'data\12kde\Outer Race\Orthogonal\0021\OR021@3_2.mat',
    r'data\12kde\Outer Race\Orthogonal\0021\OR021@3_3.mat'
]
to_write_data = [
    r'xlsx_file\OR@3_007_0', r'xlsx_file\OR@3_007_1', r'xlsx_file\OR@3_007_2',
    r'xlsx_file\OR@3_007_3', r'xlsx_file\OR@3_021_0', r'xlsx_file\OR@3_021_1',
    r'xlsx_file\OR@3_021_2', r'xlsx_file\OR@3_021_3'
]

for i in range(len(to_read_data)):
    de_value, fe_value = loadmatdata(to_read_data[i])
    mat2xlsx(to_write_data[i], de_value, fe_value)

# de_value, fe_value = loadmatdata(r'data\12kde\Ball\0007\B007_1.mat')
# mat2xlsx(r'xlsx_file\B007_1', de_value, fe_value)
