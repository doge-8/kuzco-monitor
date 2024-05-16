#!/bin/bash

# 设置信号处理器
trap "cleanup" SIGINT SIGTERM

# Discord Webhook URL
discord_webhook_url="your webhook link"

send_discord_message() {
    local message="当前主机：$(hostname) - GPU利用率低，正在重启程序..."
    curl -H "Content-Type: application/json" -X POST -d "{\"content\": \"$message\"}" "$discord_webhook_url"
}

# 清理函数，用于终止程序
cleanup() {
    echo "关闭所有kuzco"
    pkill -9 "kuzco"
    exit 0
}

# 默认工作线程数量
workers=4

# 默认检测间隔（秒）
check_interval=180

# 定义函数：等待指定秒数
wait_seconds() {
    local seconds=$1
    sleep $seconds
}

# 检查GPU使用率
check_gpu_usage() {
    local usage_sum=0
    local count=0

    for ((i=0; i<$((check_interval / 10)); i++)); do
        local usage=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | awk '{print $1}')
        usage_sum=$((usage_sum + usage))
        ((count++))
        sleep 10
    done

    local average_usage=$((usage_sum / count))
    echo "GPU平均使用率：${average_usage}%"

    if [ $average_usage -lt 35 ]; then
        return 1
    else
        return 0
    fi
}


# 循环执行程序
while true; do
    # 启动程序
    echo "启动kuzco中"
    for ((i=1; i<=$workers; i++)); do
    kuzco worker start > /dev/null 2>&1 &
    sleep 2
done
    echo "启动完毕，开始监控GPU使用率"

    # 持续监控GPU使用率
    while true; do
        wait_seconds $check_interval
        if ! check_gpu_usage; then
            echo "GPU利用率低，重启程序中"
	    send_discord_message "GPU利用率低，Kuzco 正在重启"
            break
        fi
    done

    echo "重启程序中"
    # 终止程序
    pkill -9 "kuzco"
    # 等待5秒
    sleep 5
done
