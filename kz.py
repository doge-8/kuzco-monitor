import os
import signal
import time
import sys
import subprocess
import re

# 可调用户设置参数
workers = 3  # 开越多网页控制板Generations计算延迟越高，计算延迟控制在3w左右合适，超过3万会假死！！
check_interval = 300  # 检测时间间隔，单位：秒
restart_wait_time = 30  # 重启等待时间，单位：秒
discord_webhook_url = "https://discord.com/api/webhooks/"  # Discord Webhook URL
discord_message = "kuzco运行异常，正在重启程序..."  # 发送的消息内容

# 此参数不推荐修改！
send_discord_notifications = input("输入1以启用Discord消息推送功能，输入其他任意值以禁用: ") == '1'

log_directory = '/var/log/kuzco/'

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

def total_finish_count():
    total_count = 0
    for i in range(1, workers + 1):
        log_file_path = f'{log_directory}/log{i}.txt'
        if os.path.exists(log_file_path):
            total_count += count_finish(log_file_path)
    return total_count

def clear_all_logs():
    for i in range(1, workers + 1):
        log_file_path = f'{log_directory}/log{i}.txt'
        if os.path.exists(log_file_path):
            with open(log_file_path, 'w') as file:
                file.truncate(0)

def update_worker_status():
    os.system("jq '.status = \"Offline\"' /root/.kuzco/worker.json > /root/.kuzco/worker_temp.json && mv /root/.kuzco/worker_temp.json /root/.kuzco/worker.json")

def start_kuzco(workers, start_suffix):
    if workers > 0:
        for i in range(1, workers + 1):
            print(f"启动{i}号kuzco中")
            update_worker_status()
            os.system(f"kuzco worker start {start_suffix} > {log_directory}/log{i}.txt 2>&1 &")
            update_worker_status()
            time.sleep(6)

def send_discord_message():
    if send_discord_notifications:
        hostname = subprocess.run("hostname", shell=True, capture_output=True, text=True).stdout.strip()
        message = f"当前主机：{hostname} - {discord_message}"
        curl_command = f'curl -H "Content-Type: application/json" -X POST -d \'{{"content": "{message}"}}\' "{discord_webhook_url}"'
        subprocess.run(curl_command, shell=True)

def exit_handler(signal, frame):
    print("\n检测脚本已关闭，清除所有kuzco...")
    os.system("pkill -9 'kuzco'")
    update_worker_status()
    clear_all_logs()
    sys.exit(0)

def install_jq_if_not_installed():
    jq_installed = subprocess.run("which jq", shell=True, stdout=subprocess.PIPE).stdout.decode().strip()
    if not jq_installed:
        print("jq 未安装，正在安装...")
        install_command = "sudo apt-get install -qq jq -y"  # 适用于 Ubuntu/Debian 系统
        subprocess.run(install_command, shell=True)
        print("jq 安装完毕，启动kuzco中...")

def main():
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    install_jq_if_not_installed()  # 添加安装 jq 的检查

    start_kuzco(workers, start_suffix)

    while True:
        initial_finish_count = total_finish_count()
        print("初始的'finish'数量:", initial_finish_count)

        time.sleep(check_interval)

        final_finish_count = total_finish_count()
        print("当前的'finish'数量:", final_finish_count)

        if final_finish_count > initial_finish_count:
            print("kuzco正常运行")
        else:
            print("检测到kuzco异常，尝试重启中...")
            os.system("pkill -9 'kuzco'")
            time.sleep(restart_wait_time)
            send_discord_message()
            start_kuzco(workers, start_suffix)

        clear_all_logs()

if __name__ == "__main__":
    main()
