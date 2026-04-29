import socket
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading
import time
import csv

# 设置服务器和传感器的IP地址和端口
SERVER_IP = '192.168.1.169'
SERVER_PORT = 22009
PACKET_SIZE = 1420  # 单个报文的大小

# 标志位，用于控制线程结束
running = True


# 创建TCP服务器
def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"Server started at {ip}:{port}")
    return server_socket


# 解析并输出传感器报文
def parse_sensor_data(data):
    # 解析头部数据
    header_format = '4s I f f I I'
    header_size = struct.calcsize(header_format)
    header_data = struct.unpack(header_format, data[:header_size])

    # 提取加速度数据
    acceleration_data_format = 'f f f'
    acceleration_data_size = struct.calcsize(acceleration_data_format)
    num_acceleration_data = 116  # 每个方向有116组数据
    acceleration_data = []

    for i in range(num_acceleration_data):
        offset = header_size + i * acceleration_data_size
        x, y, z = struct.unpack(acceleration_data_format,
                                data[offset:offset + acceleration_data_size])
        # acceleration_data.append((x, y, z))
        acceleration_data.append((x, y))

    # 检查包结束字符
    end_offset = header_size + num_acceleration_data * acceleration_data_size
    end_format = '4s'
    end_data = struct.unpack(
        end_format, data[end_offset:end_offset + struct.calcsize(end_format)])

    if end_data[0] != b'PEND':
        raise ValueError("Invalid packet end marker")

    return acceleration_data


# 接收传感器报文
def receive_sensor_data(server_socket, data_queue):
    global running
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    while running:
        data = client_socket.recv(PACKET_SIZE)
        if len(data) == PACKET_SIZE:
            try:
                accel_data = parse_sensor_data(data)
                data_queue.extend(accel_data)
            except struct.error as e:
                print(f"Error parsing data: {e}")
            except ValueError as e:
                print(f"Error in packet structure: {e}")
        else:
            print(
                f"Received incomplete packet: expected {PACKET_SIZE} bytes, got {len(data)} bytes"
            )
    client_socket.close()


# 实时绘图
def animate(i, data_queue, x_data, y_data, lines, x_range, data_buffer):
    while data_queue:
        x, y = data_queue.popleft()
        x_data.append(x)
        y_data.append(y)
        # z_data.append(z)
        data_buffer.append((x, y))

    lines[0].set_ydata(x_data)
    lines[1].set_ydata(y_data)
    # lines[2].set_ydata(z_data)

    return lines


# 保存数据到CSV文件
def save_data_to_csv(data_buffer, filename="./acceleration_data.csv"):
    # 使用data_buffer的副本来写入CSV文件，避免在写入过程中修改原始deque
    buffer_copy = [(x / 10, y / 10) for x, y in list(data_buffer)]
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])
        writer.writerows(buffer_copy)
    print(f"Data saved to {filename}")


# 检查数据缓冲区并保存
def check_and_save_data(data_buffer, buffer_limit=282 * 116):
    if len(data_buffer) >= buffer_limit:
        save_data_to_csv(data_buffer)
        data_buffer.clear()


if __name__ == '__main__':
    # 初始化数据队列
    data_queue = deque(maxlen=10000000)  # 使用最大长度maxlen的队列
    data_buffer = deque(maxlen=282 * 116)  # 用于存储282个报文内的数据
    x_range = 27777  # 显示点数

    # 启动服务器线程
    server_socket = start_server(SERVER_IP, SERVER_PORT)

    server_thread = threading.Thread(target=receive_sensor_data,
                                     args=(server_socket, data_queue))
    server_thread.daemon = True
    server_thread.start()

    # 设置实时绘图
    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(10, 6))
    # x = range(x_range)
    # x_data = deque([0] * x_range, maxlen=x_range)
    # y_data = deque([0] * x_range, maxlen=x_range)
    # z_data = deque([0] * x_range, maxlen=x_range)
    #
    # line_x, = ax1.plot(x, list(x_data), label='X', linewidth=0.5, color='r')
    # line_y, = ax2.plot(x, list(y_data), label='Y', linewidth=0.5, color='g')
    # line_z, = ax3.plot(x, list(z_data), label='Z', linewidth=0.5, color='b')
    #
    # ax1.legend()
    # ax2.legend()
    # ax3.legend()
    # ax1.set_xlim(0, x_range)
    # ax1.set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    # ax2.set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    # ax3.set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    # ax3.set_xlabel('Time')
    # ax1.set_ylabel('Acceleration X (g)')
    # ax2.set_ylabel('Acceleration Y (g)')
    # ax3.set_ylabel('Acceleration Z (g)')

    # 设置动画，显式地设置save_count以避免警告，调整interval提高帧率

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
    x = range(x_range)
    x_data = deque([0] * x_range, maxlen=x_range)
    y_data = deque([0] * x_range, maxlen=x_range)
    # z_data = deque([0] * x_range, maxlen=x_range)

    line_x, = ax1.plot(x, list(x_data), label='X', linewidth=0.5, color='r')
    line_y, = ax2.plot(x, list(y_data), label='Y', linewidth=0.5, color='b')
    # line_z, = ax3.plot(x, list(z_data), label='Z', linewidth=0.5, color='b')

    ax1.legend()
    ax2.legend()
    # ax3.legend()
    ax1.set_xlim(0, x_range)
    ax1.set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    ax2.set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    # ax3.set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    # ax3.set_xlabel('Time')
    ax1.set_ylabel('Acceleration X (g)')
    ax2.set_ylabel('Acceleration Y (g)')
    # ax3.set_ylabel('Acceleration Z (g)')
    ani = animation.FuncAnimation(fig,
                                  animate,
                                  fargs=(data_queue, x_data, y_data,
                                         [line_x,
                                          line_y], x_range, data_buffer),
                                  interval=200,
                                  save_count=1)

    # 设置关闭事件
    def on_close(event):
        global running
        running = False
        server_socket.close()
        # save_data_to_csv(data_buffer)  # 关闭时保存剩余数据

    fig.canvas.mpl_connect('close_event', on_close)

    # 创建检查并保存数据的线程
    def buffer_check_thread():
        while running:
            check_and_save_data(data_buffer)
            time.sleep(1)  # 每秒钟检查一次缓冲区

    buffer_thread = threading.Thread(target=buffer_check_thread)
    buffer_thread.daemon = True
    buffer_thread.start()

    plt.tight_layout()
    plt.show()
