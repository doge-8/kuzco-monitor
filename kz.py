import os
import signal
import time
import sys
import re

# 可调用户设置参数
workers = 3  # 开越多网页控制板Generations计算延迟越高，计算延迟控制在3w左右合适，超过3万会假死！！
check_interval = 300  # 检测时间间隔，单位：秒
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

def get_individual_finish_counts():
    counts = {}
    for i in range(1, workers + 1):
        log_file_path = f'{log_directory}/log{i}.txt'
        if os.path.exists(log_file_path):
            counts[i] = count_finish(log_file_path)
        else:
            counts[i] = 0
    return counts

def clear_all_logs():
    for i in range(1, workers + 1):
        log_file_path = f'{log_directory}/log{i}.txt'
        if os.path.exists(log_file_path):
            with open(log_file_path, 'w') as file:
                file.truncate(0)

def start_kuzco(workers, start_suffix):
    pids = {}
    if workers > 0:
        for i in range(1, workers + 1):
            print(f"启动{i}号kuzco中")
            pid = os.fork()
            if pid == 0:  # 子进程
                os.system(f"kuzco worker start {start_suffix} > {log_directory}/log{i}.txt 2>&1")
                sys.exit(0)
            else:  # 父进程
                pids[i] = pid
                time.sleep(6)
    return pids

def restart_worker(worker_id, start_suffix):
    print(f"重启{worker_id}号kuzco中")
    pid = os.fork()
    if pid == 0:  # 子进程
        os.system(f"kuzco worker start {start_suffix} > {log_directory}/log{worker_id}.txt 2>&1")
        sys.exit(0)
    else:  # 父进程
        return pid

def exit_handler(signal, frame):
    print("\n检测脚本已关闭，清除所有kuzco...")
    os.system("pkill -9 'kuzco'")
    clear_all_logs()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    pids = start_kuzco(workers, start_suffix)

    while True:
        initial_finish_counts = get_individual_finish_counts()
        print("初始的'finish'数量:", initial_finish_counts)

        time.sleep(check_interval)

        current_finish_counts = get_individual_finish_counts()
        print("当前的'finish'数量:", current_finish_counts)

        for worker_id in initial_finish_counts:
            if current_finish_counts[worker_id] > initial_finish_counts[worker_id]:
                print(f"{worker_id}号kuzco正常运行")
            else:
                print(f"检测到{worker_id}号kuzco异常，尝试重启中...")
                os.kill(pids[worker_id], signal.SIGKILL)
                time.sleep(restart_wait_time)
                pids[worker_id] = restart_worker(worker_id, start_suffix)

        clear_all_logs()

if __name__ == "__main__":
    main()
