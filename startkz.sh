#!/bin/bash

# 默认工作线程数量
workers=1

# 设置信号处理器
trap "cleanup" SIGINT SIGTERM

# 清理函数，用于终止程序并删除日志
cleanup() {
    echo "关闭所有kuzco"
    pkill -9 "kuzco"
    echo "删除旧的日志文件"
    rm -f /root/log_kuzco*.txt
    exit 0
}

# 定义函数：等待指定秒数
wait_seconds() {
    local seconds=$1
    sleep $seconds
}

# 检查GPU使用率
check_gpu_usage() {
    local usage_sum=0
    local count=0
    local interval=10  # 检查间隔（秒）

    for ((i=0; i<18; i++)); do  # 改成18次循环，每次间隔10秒，共计3分钟
        local usage=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | awk '{print $1}')
        usage_sum=$((usage_sum + usage))
        ((count++))
        sleep $interval
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
    # 启动程序并将输出重定向到不同的日志文件
    echo "启动kuzco中"
    for ((i=1; i<=$workers; i++)); do
        kuzco worker start >> /root/log_kuzco${i}.txt 2>&1 &
        sleep 2
    done
    echo "启动完毕，开始监控GPU使用率"

    # 持续监控GPU使用率
    while true; do
        wait_seconds 180  # 每3分钟检查一次
        if ! check_gpu_usage; then
            echo "GPU利用率低，重启程序中"
            break
        fi
    done

    echo "重启程序中"
    # 终止程序
    pkill -9 "kuzco"
    # 删除旧的日志文件
    echo "删除旧的日志文件"
    rm -f /root/log_kuzco*.txt
    # 等待5秒
    sleep 5
done
