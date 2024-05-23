import os
import signal
import time
import sys
import subprocess

# 设置参数
workers = 5  # 工作的数量
check_interval = 600  # 检测时间间隔，单位：秒
restart_wait_time = 30  # 重启等待时间，单位：秒

# Discord参数
discord_webhook_url = "https://discord.com/api/webhooks/1240579391172640842/qZy"
discord_message = "kuzco运行异常，正在重启程序..."
send_discord_notifications = input("输入1以禁用Discord消息推送功能，输入其他任意值以启用: ") != '1'

def count_finish(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        finish_count = content.count('finish')
    return finish_count

def clear_log(file_path):
    with open(file_path, 'w') as file:
        file.truncate(0)  # 清空文件内容

def start_kuzco(workers):
    print("启动1号kuzco中")
    os.system("kuzco worker start > /root/log.txt 2>&1 &")  # 第一个kuzco启动时记录日志到指定文件
    time.sleep(6)
    for i in range(2, workers + 1):
        print(f"启动{i}号kuzco中")
        os.system("kuzco worker start > /dev/null 2>&1 &")
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
    clear_log('/root/log.txt')  # 清除log.txt文件
    sys.exit(0)

def main():
    file_path = '/root/log.txt'

    # 注册信号处理函数
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    # 程序启动时先启动指定数量的kuzco程序
    start_kuzco(workers)

    while True:
        initial_finish_count = count_finish(file_path)
        print("初始的'finish'数量:", initial_finish_count)

        time.sleep(check_interval)  # 每隔时间检测一次

        final_finish_count = count_finish(file_path)
        print("当前的'finish'数量:", final_finish_count)

        if final_finish_count > initial_finish_count:
            print("kuzco正常运行")
        else:
            print("检测到kuzco异常，尝试重启中...")
            os.system("pkill -9 'kuzco'")
            time.sleep(restart_wait_time)  # 结束所有kuzco后等待30秒
            send_discord_message()  # 发送 Discord 消息
            start_kuzco(workers)

        # 清除日志内容
        clear_log(file_path)

if __name__ == "__main__":
    main()
