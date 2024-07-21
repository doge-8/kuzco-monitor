import os
import signal
import time
import sys
import re
import subprocess

# 可调用户设置参数
workers = 3  # 开越多网页控制板Generations计算延迟越高，计算延迟控制在3w左右合适，超过3万会假死！！
check_interval = 300  # 检测时间间隔，单位：秒
restart_wait_time = 30  # 重启等待时间，单位：秒

# 获取当前脚本的目录
current_directory = os.path.dirname(os.path.abspath(__file__))
log_directory = os.path.join(current_directory, 'log')
pid_directory = os.path.join(current_directory, 'pids')

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

def total_finish_counts():
    finish_counts = {}
    for i in range(1, workers + 1):
        log_file_path = f'{log_directory}/log{i}.txt'
        if os.path.exists(log_file_path):
            finish_counts[i] = count_finish(log_file_path)
        else:
            finish_counts[i] = 0
    return finish_counts

def clear_log(worker_id):
    log_file_path = f'{log_directory}/log{worker_id}.txt'
    if os.path.exists(log_file_path):
        with open(log_file_path, 'w') as file:
            file.truncate(0)

def clear_all_logs():
    for i in range(1, workers + 1):
        clear_log(i)

def start_kuzco(worker_id, start_suffix):
    print(f"启动{worker_id}号kuzco中")
    log_file_path = f'{log_directory}/log{worker_id}.txt'
    pid_file_path = f'{pid_directory}/pid{worker_id}.txt'
    
    # 启动进程并记录PID
    process = subprocess.Popen(f"kuzco worker start {start_suffix} > {log_file_path} 2>&1 & echo $!", shell=True, stdout=subprocess.PIPE)
    pid = process.stdout.read().decode().strip()
    
    with open(pid_file_path, 'w') as pid_file:
        pid_file.write(pid)
    
    time.sleep(6)

def stop_kuzco(worker_id):
    pid_file_path = f'{pid_directory}/pid{worker_id}.txt'
    if os.path.exists(pid_file_path):
        with open(pid_file_path, 'r') as pid_file:
            pid = pid_file.read().strip()
        os.system(f"kill -9 {pid}")
        os.remove(pid_file_path)

def stop_all_kuzco():
    for i in range(1, workers + 1):
        stop_kuzco(i)

def exit_handler(signal, frame):
    print("\n检测脚本已关闭，清除所有kuzco...")
    stop_all_kuzco()
    clear_all_logs()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    if not os.path.exists(pid_directory):
        os.makedirs(pid_directory)

    for i in range(1, workers + 1):
        start_kuzco(i, start_suffix)

    last_finish_counts = total_finish_counts()

    while True:
        print("当前的'finish'数量:", last_finish_counts)

        time.sleep(check_interval)

        current_finish_counts = total_finish_counts()
        print("新的'finish'数量:", current_finish_counts)

        for i in range(1, workers + 1):
            if current_finish_counts[i] > last_finish_counts[i]:
                print(f"{i}号kuzco正常运行")
            else:
                print(f"检测到{i}号kuzco异常，尝试重启中...")
                stop_kuzco(i)
                time.sleep(restart_wait_time)
                start_kuzco(i, start_suffix)

        last_finish_counts = current_finish_counts

        clear_all_logs()

if __name__ == "__main__":
    main()
