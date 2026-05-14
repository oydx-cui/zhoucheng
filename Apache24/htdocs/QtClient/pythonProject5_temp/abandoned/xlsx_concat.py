import os
import pandas as pd
from tqdm import tqdm

data_folder = r'xlsx_file\B007_0'
output_folder = r'concat_xlsx_file\B007_0'
start_concat_num = 601  # 从第start_concat_num个文件开始拼接

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取文件夹中所有文件的路径
file_paths = [
    os.path.join(data_folder, filename) for filename in os.listdir(data_folder)
    if filename.endswith('.xlsx')
]

# 确保文件按照文件名排序
file_paths.sort()

# 每12个文件一组进行拼接
for i in tqdm(range(start_concat_num - 1, len(file_paths), 12),
              desc='Processing Files',
              unit='group'):
    # 定义一个空的DataFrame用于存储拼接后的数据
    concatenated_df = pd.DataFrame(columns=['sn', 'de', 'fe'])

    # 读取当前组中的所有文件并进行拼接
    for file_path in file_paths[i:i + 12]:
        df = pd.read_excel(file_path)
        concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

    # 将序列号重新编号，确保递增
    concatenated_df['sn'] = range(1, len(concatenated_df) + 1)

    # 输出拼接后的数据到文件
    output_file_path = os.path.join(
        output_folder, f'data{(i-start_concat_num+1)//12 + 1}.xlsx')

    # 如果拼接的文件数量不足12个，则删除最后一个输出文件
    if len(file_paths[i:i + 12]) < 12:
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
    else:
        concatenated_df.to_excel(output_file_path, index=False)
