import os
import signal
import time
import sys
import re

# 可调用户设置参数
workers = 3  # 开越多网页控制板Generations计算延迟越高，计算延迟控制在3w左右合适，超过3万会假死！！
check_interval = 3600  # 检测时间间隔，单位：秒，修改为1小时
restart_wait_time = 30  # 重启等待时间，单位：秒

# 获取当前脚本的目录
current_directory = os.path.dirname(os.path.abspath(__file__))
log_directory = os.path.join(current_directory, 'log')

def get_start_suffix():
    while True:
        start_suffix = input("请输入启动后缀（例如：--worker Es0VkSLpgmpHAGkMOWP0A --code 402d6684-215e-4106-a834-164ef0507377）: ")
        if re.match(r'^--worker \S+ --code \S+$', start_suffix):
            return start_suffix
        else:
            print("后缀格式错误，请重新输入")

start_suffix = get_start_suffix()

def count_finish(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        finish_count = content.count('finish')
    return finish_count

def start_worker(worker_id, start_suffix):
    log_file_path = os.path.join(log_directory, f'log{worker_id}.txt')
    command = f"kuzco worker start {start_suffix} > {log_file_path} 2>&1 &"
    os.system(command)
    print(f"启动{worker_id}号kuzco中")
    time.sleep(6)

def start_kuzco(workers, start_suffix):
    for i in range(1, workers + 1):
        start_worker(i, start_suffix)

def exit_handler(signal, frame):
    print("\n检测脚本已关闭，清除所有kuzco...")
    os.system("pkill -9 'kuzco'")
    clear_all_logs()
    sys.exit(0)

def clear_all_logs():
    for i in range(1, workers + 1):
        log_file_path = os.path.join(log_directory, f'log{i}.txt')
        if os.path.exists(log_file_path):
            with open(log_file_path, 'w') as file:
                file.truncate(0)

def main():
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    start_kuzco(workers, start_suffix)

    while True:
        initial_finish_counts = {}
        for i in range(1, workers + 1):
            log_file_path = os.path.join(log_directory, f'log{i}.txt')
            if os.path.exists(log_file_path):
                initial_finish_counts[i] = count_finish(log_file_path)
            else:
                initial_finish_counts[i] = 0
        print("初始的'finish'数量:", initial_finish_counts)

        time.sleep(check_interval)

        final_finish_counts = {}
        for i in range(1, workers + 1):
            log_file_path = os.path.join(log_directory, f'log{i}.txt')
            if os.path.exists(log_file_path):
                final_finish_counts[i] = count_finish(log_file_path)
            else:
                final_finish_counts[i] = 0
        print("当前的'finish'数量:", final_finish_counts)

        all_workers_running = True
        for i in range(1, workers + 1):
            if final_finish_counts[i] > initial_finish_counts[i]:
                continue  # Worker 正常运行，继续检查下一个 worker
            else:
                print(f"检测到{i}号kuzco异常，尝试重启中...")
                time.sleep(restart_wait_time)
                os.system("pkill -9 'kuzco'")
                start_kuzco(workers, start_suffix)
                all_workers_running = False
                break

        if all_workers_running:
            print("所有kuzco正常运行")
        else:
            print("部分或全部kuzco已重启")

        clear_all_logs()

if __name__ == "__main__":
    main()
