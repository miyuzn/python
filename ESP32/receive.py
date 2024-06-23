import socket
import signal
import sys
import sensor

data_list = []
file_name = "sensor_data.csv"

# 定义一个信号处理器，用于捕获中断信号
def signal_handler(sig, frame):
    print(f'\nExiting gracefully. Sensor data saved to {file_name}.')
    sensor.save_sensor_data_to_csv(data_list, file_name)
    sys.exit(0)

# 配置信号处理器来监听SIGINT（通常是Ctrl+C）
signal.signal(signal.SIGINT, signal_handler)

# 接收广播数据函数
def receive_broadcast():
    udp_ip = ""  # 监听广播地址
    udp_port = 1370
    count = 0
    # 创建UDP socket
    # 接收数据的sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定端口和IP
    sock.bind((udp_ip, udp_port))


    local_ip = "127.0.0.1"
    local_port = 53000
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Connecting to sensor...")
    while True:
        data, addr = sock.recvfrom(1024)  # 缓冲区大小为1024字节
        sock2.sendto(data, (local_ip, local_port))
        data_list.append(sensor.parse_sensor_data(data))
        count += 1
        if count % 100 == 0:
            print(f"\rReceived {count} packets from {addr}, Press Ctrl+C to stop receive.")

if __name__ == "__main__":
    receive_broadcast()
