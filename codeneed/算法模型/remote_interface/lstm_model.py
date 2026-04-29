import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import torch
import torch.nn as nn
import csv
import numpy as np
from numpy.fft import fft, ifftn
from tensorly.decomposition import tucker
import sys
import mysql.connector
from datetime import datetime
import json


class DualLSTMModel(nn.Module):

    def __init__(self, input_size_time, input_size_freq, hidden_size,
                 num_layers, output_size):
        super(DualLSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # 时域 LSTM 网络
        self.lstm_time = nn.LSTM(input_size_time * 2,
                                 hidden_size,
                                 num_layers,
                                 batch_first=True)
        # 频域 LSTM 网络
        self.lstm_freq = nn.LSTM(input_size_freq * 4,
                                 hidden_size,
                                 num_layers,
                                 batch_first=True)

        # 拼接后使用的全连接层
        self.fc = nn.Linear(hidden_size * 2, output_size)

    def forward(self, x_time, x_freq):
        # 初始化隐藏和记忆状态
        h0_time = torch.zeros(self.num_layers, x_time.size(0),
                              self.hidden_size).to(x_time.device)
        c0_time = torch.zeros(self.num_layers, x_time.size(0),
                              self.hidden_size).to(x_time.device)
        h0_freq = torch.zeros(self.num_layers, x_freq.size(0),
                              self.hidden_size).to(x_freq.device)
        c0_freq = torch.zeros(self.num_layers, x_freq.size(0),
                              self.hidden_size).to(x_freq.device)

        # 时域 LSTM 前向传播
        out_time, _ = self.lstm_time(x_time, (h0_time, c0_time))
        out_time = out_time[:, -1, :]  # 只取最后一个时间步的输出

        # 频域 LSTM 前向传播
        out_freq, _ = self.lstm_freq(x_freq, (h0_freq, c0_freq))
        out_freq = out_freq[:, -1, :]  # 只取最后一个时间步的输出

        # 将两个结果拼接在一起
        out_combined = torch.cat((out_time, out_freq), dim=1)

        # 通过全连接层生成最终输出
        out = self.fc(out_combined)
        return out


def load_model(model_path='model\\lstm.pth',
               input_size_time=7,
               input_size_freq=7,
               hidden_size=64,
               num_layers=2,
               output_size=1):
    """
    从指定的路径加载 LSTM 模型。

    Args:
    model_path (str): 模型参数存储的路径。
    input_size_time (int): 时域输入的特征数量。
    input_size_freq (int): 频域输入的特征数量。
    hidden_size (int): LSTM 隐藏层的大小。
    num_layers (int): LSTM 堆叠的层数。
    output_size (int): 输出层的大小。

    Returns:
    nn.Module: 加载了参数的 LSTM 模型。
    """
    # 实例化模型
    model = DualLSTMModel(input_size_time, input_size_freq, hidden_size,
                          num_layers, output_size)
    # 加载模型参数
    model.load_state_dict(torch.load(model_path))
    model.eval()  # 设置为评估模式
    return model


def predict(model, input_ttensor, input_ftensor):
    """
    使用加载的模型进行预测。

    Args:
    model (nn.Module): 加载了参数的模型。
    input_tensor (torch.Tensor): 需要进行预测的输入张量。

    Returns:
    torch.Tensor: 模型的输出结果。
    """
    with torch.no_grad():  # 在预测时不需要计算梯度
        output = model(input_ttensor, input_ftensor)
    return output


def read_single_csv(machine_id, bearing_id):
    """
    读取指定工况和轴承号的某一个振动数据文件，并返回振动数据。

    Args:
        machine_id (int): 机器的编号。
        bearing_id (int): 轴承的编号。

    Returns:
        data_H (list): 水平方向振动数据列表。
        data_L (list): 垂直方向振动数据列表。
    """
    data_H = []
    data_L = []

    # 构建文件夹路径
    folder_path = f"life_vib_example/machine-{machine_id}/bearing-{int(bearing_id):02d}/"
    # 假设每个文件夹下的第一个文件名是 "1.csv"
    file_path = folder_path + "1.csv"

    try:
        with open(file_path, "r") as file:
            csv_data = csv.reader(file)
            next(csv_data)  # 跳过标题行
            for row in csv_data:
                # 假设水平方向数据在第二列，垂直方向数据在第一列
                data_H.append(float(row[1]))
                data_L.append(float(row[0]))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return [data_H, data_L]


def extract_features_with_stride(data, window_size=100, stride=50):
    """
    使用固定步长从数据中提取特征，包括窗口统计特征、窗口间差值和连续时间点的差值。

    Args:
        data (list): 输入的数据列表。
        window_size (int): 每个窗口包含的数据点数。
        stride (int): 窗口之间的步长，控制重叠程度。

    Returns:
        np.array: 提取的特征数组。
    """
    num_windows = (len(data) - window_size) // stride + 1
    features = []

    for i in range(num_windows):
        start_index = i * stride
        end_index = start_index + window_size
        window = np.array(data[start_index:end_index])

        # 窗口统计特征
        mean = np.mean(window)
        std = np.std(window)
        maximum = np.max(window)
        minimum = np.min(window)

        # 连续时间点的差值特征
        deltas = np.diff(window, n=1)  # 计算连续时间点之间的差值
        delta_mean = np.mean(deltas)
        delta_std = np.std(deltas)

        # 窗口间差值
        if start_index > 0:
            inter_window_delta = window[0] - data[start_index - 1]
        else:
            inter_window_delta = 0  # 如果是第一个窗口，没有前一个时间点，设为0

        # 将所有特征组合
        features.append([
            mean, std, maximum, minimum, delta_mean, delta_std,
            inter_window_delta
        ])

    return np.array(features)


def build_tensor(data, window_size=100, stride=50):
    """
    使用特征提取函数从多个方向的数据中提取特征，并构建三阶张量。

    第1维：时间步（时间窗口的数量）
    每个样本包含的时间窗口数，这个数是基于滑动窗口的大小和步长计算得到的。时间步的数量由数据的总长度、选择的窗口大小和步长共同决定。
    
    第2维：方向
    数据从两个方向（水平和垂直）收集，因此这个维度大小为2。

    第3维：特征数
    在每个时间窗口内提取的特征数量。包括统计信息如均值、标准差等。

    Args:
        data (list of lists): 每个列表代表一个方向的时间序列数据。
        window_size (int): 每个窗口包含的数据点数。
        stride (int): 窗口之间的步长。

    Returns:
        torch.Tensor: 构建的三阶张量，维度为[时间步, 特征数, 方向数]。
    """
    num_directions = len(data)
    tensors = []

    for direction in range(num_directions):
        features = extract_features_with_stride(data[direction], window_size,
                                                stride)
        tensors.append(features)

    # 沿着新的轴堆叠特征，形成三阶张量
    tensor_np = np.stack(tensors, axis=1)  # 把每个方向的特征堆叠起来

    # 将 NumPy 数组转换为 PyTorch tensor
    tensor = torch.tensor(tensor_np, dtype=torch.float32)

    return tensor


def unfold(tensor):
    """
    沿着mode-1方向将张量纵向展开为矩阵(前后方向的切片)。

    Args:
        tensor (torch.Tensor): 输入的张量。

    Returns:
        torch.Tensor: mode-1展开后的矩阵。
    """
    # 改变维度，展开成二维矩阵
    order = [i for i in range(tensor.ndim) if i != 1] + [1]
    permuted_tensor = tensor.permute(order)
    unfolded_matrix = permuted_tensor.reshape(-1, tensor.size(1))

    return unfolded_matrix


def fold(matrix, original_shape):
    """
    将沿mode-1展开的矩阵(前后方向的切片)复原为原始张量。

    Args:
        matrix (torch.Tensor): mode-1展开(前后方向的切片)的矩阵。
        original_shape (tuple): 原始张量的形状。

    Returns:
        torch.Tensor: 复原后的张量。
    """
    # 获取原始张量的形状并生成新的排列顺序
    unfolded_shape = list(original_shape)
    first_dim = unfolded_shape.pop(1)
    new_shape = unfolded_shape + [first_dim]

    # 重塑矩阵为原始张量形状
    folded_tensor = matrix.view(new_shape)

    # 重新排列维度顺序，确保返回到原始顺序
    perm_order = [i for i in range(len(unfolded_shape) + 1) if i != 1] + [1]
    return folded_tensor.permute(perm_order)


def circ_block(tensor):
    """
    将张量的每个正面切片作为向量的元素，生成块循环矩阵。

    Args:
        tensor (torch.Tensor): 输入的张量，每个切片将作为循环块的一个元素。

    Returns:
        torch.Tensor: 生成的块循环矩阵。
    """
    # 将指定模式的维度放到第一个维度进行切片
    slices = tensor.unbind(dim=-1)
    num_blocks = len(slices)
    rows, cols = slices[0].shape

    # 初始化块循环矩阵
    circ_matrix = torch.zeros((rows * num_blocks, cols * num_blocks))

    # 填充块循环矩阵
    for i in range(num_blocks):
        for j in range(num_blocks):
            block_index = (i + j) % num_blocks
            circ_matrix[i * rows:(i + 1) * rows,
                        j * cols:(j + 1) * cols] = slices[block_index]

    return circ_matrix


def tensor_mul(A, B):
    """
    实现 A ∗ B = fold(circ(unfold(A, 1)) · unfold(B, 1))

    Args:
        A (torch.Tensor): 张量 A。
        B (torch.Tensor): 张量 B。

    Returns:
        torch.Tensor: A 与 B 乘积后的张量。
    """
    # 获取张量 A 的块循环矩阵和张量 B 的展开矩阵
    circ_A = circ_block(A)
    unfB = unfold(B)

    # 检查循环矩阵与 B_unfold 的维度匹配
    assert circ_A.shape[1] == unfB.shape[
        0], f"Circ_A: {circ_A.shape}, Unfold_B: {unfB.shape}"

    # 对循环卷积矩阵与 B 展开的矩阵进行矩阵乘法
    product = torch.matmul(circ_A, unfB)

    # 折叠回原始张量的形状
    result = fold(product, (A.shape[0], B.shape[1], A.shape[2]))
    return result


def tensor_dot(A, B):
    """
    对两个张量的正面切片分别进行普通矩阵乘法，再将结果沿进行切片的维度堆叠。

    Args:
        A (torch.Tensor): 第一个张量，切片形状应与 B 对应。
        B (torch.Tensor): 第二个张量，切片形状应与 A 对应。

    Returns:
        torch.Tensor: 对应切片矩阵乘法后堆叠的结果张量。
    """
    # 对第一个维度拆分成切片
    slices_A = A.unbind(dim=-1)
    slices_B = B.unbind(dim=-1)

    # 确保两个张量具有相同数量的切片
    assert len(slices_A) == len(slices_B), "两个张量的正面切片数量不匹配"

    # 对应切片进行矩阵乘法
    results = [torch.matmul(a, b) for a, b in zip(slices_A, slices_B)]

    # 堆叠结果
    result_tensor = torch.stack(results, dim=-1)

    return result_tensor


def normalize_tensor(tensor_data):
    """
    标准化输入张量，通过沿最后一个维度减去每个切片的平均值来进行。

    Args:
        tensor_data (torch.Tensor): 输入的三阶张量。

    Returns:
        torch.Tensor: 标准化后的张量。
    """
    mean_slice = torch.mean(tensor_data, dim=-1, keepdim=True)
    normalized_data = tensor_data - mean_slice
    return normalized_data


def t_svd(tensor):
    """
    对三阶张量进行傅里叶变换，并应用Tucker分解，在频域阶上拼接核心张量和因子矩阵。

    Args:
        tensor (np.array): 输入的三阶张量。
        rk (int): 在每个维度上保留的奇异值数量。

    Returns:
        tuple: 包含频域内原张量、核心张量和因子矩阵的元组。
    """
    tensor_fft = fft(tensor, axis=-1)
    cores = []
    factor_matrices = [[] for _ in range(2)]  # 预留两个因子矩阵的空间

    for i in range(tensor_fft.shape[-1]):
        core, factors = tucker(tensor_fft[..., i],
                               rank=tensor_fft[..., i].shape)
        cores.append(core)
        for j in range(2):
            factor_matrices[j].append(factors[j])

    full_core_fd = np.stack(cores, axis=-1)
    factor_tensors_fd = [
        np.stack(matrices, axis=-1) for matrices in factor_matrices
    ]

    return tensor_fft, full_core_fd, factor_tensors_fd


def ifft_on_core_and_factors(core, factors):
    """
    对核心张量和因子张量执行逆傅里叶变换，将它们从频域转换回时域。

    Args:
        core (np.array): 频域内的核心张量。
        factors (list of np.array): 频域内的因子矩阵列表。

    Returns:
        tuple: 包含时域内核心张量和因子矩阵的元组。
    """
    core_td = ifftn(core, axes=[-1]).real
    factors_td = [ifftn(factor, axes=[-1]).real for factor in factors]
    return core_td, factors_td


def td_ext(A, U, n1):
    """
    时域特征提取算法

    Args:
        A (torch.Tensor): 输入三阶张量
        U (torch.Tensor): 时域张量
        n1 (int): 张量 U 截取维数

    Returns:
        torch.Tensor: 时域特征张量
    """
    # 确保 A 和 U 都是 torch 的张量
    if not isinstance(A, torch.Tensor):
        A = torch.tensor(A, dtype=torch.float32)
    if not isinstance(U, torch.Tensor):
        U = torch.tensor(U, dtype=torch.float32)

    # 在第二阶上做截取
    U_k = U[:, :n1, :]
    # 转置 U_k 的前两阶
    U_kt = U_k.permute(1, 0, 2)
    # 张量乘法
    ts = tensor_mul(U_kt, A)
    if not isinstance(ts, torch.Tensor):
        ts = torch.tensor(ts, dtype=torch.float32)
    return ts


def fd_ext(A_, U_, n2):
    """
    频域特征提取算法

    Args:
        A_ (torch.Tensor): 输入三阶张量
        U_ (torch.Tensor): 频域张量
        n2 (int): 张量 U_ 截取维数

    Returns:
        torch.Tensor: 频域特征张量
    """
    # 确保 A_ 和 U_ 都是 torch 的张量
    if not isinstance(A_, torch.Tensor):
        A_ = torch.tensor(A_, dtype=torch.complex64)
    if not isinstance(U_, torch.Tensor):
        U_ = torch.tensor(U_, dtype=torch.complex64)
    # 在第二阶上做截取
    U_k = U_[:, :n2, :]
    # 转置 U_k 的前两阶
    U_kt = U_k.permute(1, 0, 2)
    # 张量点积
    ts = tensor_dot(U_kt, A_)
    if not isinstance(ts, torch.Tensor):
        ts = torch.tensor(ts, dtype=torch.complex64)
    return ts


# 准备数据
def prepare_data(machine_id,
                 bearing_id,
                 window_size=120,
                 stride=40,
                 n1=600,
                 n2=600):
    # 读取完整振动数据及其剩余寿命
    vibration_data = read_single_csv(machine_id, bearing_id)
    tensor = build_tensor(vibration_data, window_size, stride)

    # 标准化张量
    normalized_tensor = normalize_tensor(tensor)

    # t-svd
    ftensor, core_fd, factors_fd = t_svd(normalized_tensor)
    core_td, factors_td = ifft_on_core_and_factors(core_fd, factors_fd)

    # 时域、频域特征张量提取
    time_features = td_ext(normalized_tensor, factors_td[0], n1)
    freq_features = fd_ext(ftensor, factors_fd[0], n2)

    # 时域输入张量
    t_ext_tensor = torch.cat((time_features[:, 0, :], time_features[:, 1, :]),
                             dim=-1).unsqueeze(0)

    # 频域输入张量
    real_part = freq_features.real
    imag_part = freq_features.imag
    # 将实部和虚部沿特征维度合并
    f_ext_tensor = torch.cat([real_part, imag_part], dim=-1)
    f_ext_tensor = torch.cat((f_ext_tensor[:, 0, :], f_ext_tensor[:, 1, :]),
                             dim=-1).unsqueeze(0)

    return t_ext_tensor, f_ext_tensor


def insert_into_db(machine_id, bearing_id, rul):
    try:
        # Database connection configuration
        db_config = {
            'user': 'argSysAdmin',
            'password': 'argbearing',
            'host': '172.20.10.3',
            'database': 'argbearing_db'
        }

        # Establish the database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Get the maximum predictSN value
        max_sn_query = "SELECT MAX(predictSN) FROM rul_pred"
        cursor.execute(max_sn_query)
        result = cursor.fetchone()
        max_predict_sn = result[0] if result[0] is not None else 0
        new_predict_sn = max_predict_sn + 1

        # Insert the RUL prediction into the database
        predict_time = datetime.now()
        insert_query = """
            INSERT INTO rul_pred (predictSN, machineNumber, bearingNumber, rul, predictTime)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (new_predict_sn, machine_id, bearing_id, rul, predict_time))
        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)


def process(machine_id, bearing_id):
    lstm = load_model()
    t_ext_tensor, f_ext_tensor = prepare_data(machine_id,
                                              bearing_id)  # 机器号，轴承号
    res = predict(lstm, t_ext_tensor, f_ext_tensor)
    return float(res.item()) * 161


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python lstm_model.py process <machine_id> <bearing_id>")
        sys.exit(1)

    command = sys.argv[1]
    machine_id = sys.argv[2]
    bearing_id = sys.argv[3]

    if command == "process":
        rul = process(machine_id, bearing_id)
        insert_into_db(machine_id, bearing_id, rul)
        result = {
            "machine_id": machine_id,
            "bearing_id": bearing_id,
            "rul": rul
        }
        print(json.dumps(result))
    else:
        print(json.dumps({}))
        sys.exit(1)
