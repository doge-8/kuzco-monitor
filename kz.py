import os
import signal
import time
import sys
import subprocess

# 可调用户设置参数
workers = 2  # 工作的数量
check_interval = 600  # 检测时间间隔，单位：秒
restart_wait_time = 30  # 重启等待时间，单位：秒
discord_webhook_url = "https://discord.com/api/webhooks/"  # Discord Webhook URL
discord_message = "kuzco运行异常，正在重启程序..."  # 发送的消息内容

#此参数不推荐修改！
send_discord_notifications = input("输入1以禁用Discord消息推送，输入其他任意值以启用: ") != '1'

log_directory = '/var/log/kuzco/'

def count_finish(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        finish_count = content.count('finish')
    return finish_count

def clear_log(file_path):
    with open(file_path, 'w') as file:
        file.truncate(0)

def start_kuzco(workers):
    if workers > 0:
        print("启动1号kuzco中")
        os.system(f"kuzco worker start > {log_directory}/log.txt 2>&1 &")
        time.sleep(6)
        for i in range(2, workers + 1):
            print(f"启动{i}号kuzco中")
            os.system(f"kuzco worker start > /dev/null 2>&1 &")
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
    clear_log(f'{log_directory}/log.txt')
    sys.exit(0)

def main():
    file_path = f'{log_directory}/log.txt'

    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    start_kuzco(workers)

    while True:
        initial_finish_count = count_finish(file_path)
        print("初始的'finish'数量:", initial_finish_count)

        time.sleep(check_interval)

        final_finish_count = count_finish(file_path)
        print("当前的'finish'数量:", final_finish_count)

        if final_finish_count > initial_finish_count:
            print("kuzco正常运行")
        else:
            print("检测到kuzco异常，尝试重启中...")
            os.system("pkill -9 'kuzco'")
            time.sleep(restart_wait_time)
            send_discord_message()
            start_kuzco(workers)

        clear_log(file_path)

if __name__ == "__main__":
    main()
