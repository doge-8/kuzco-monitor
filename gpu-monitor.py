import time
from pynvml import *

def get_gpu_utilization():
    try:
        nvmlInit()
        device_count = nvmlDeviceGetCount()
        total_utilization = 0
        for i in range(device_count):
            handle = nvmlDeviceGetHandleByIndex(i)
            utilization = nvmlDeviceGetUtilizationRates(handle)
            total_utilization += utilization.gpu
        nvmlShutdown()
        return total_utilization / device_count if device_count > 0 else 0
    except NVMLError as err:
        print(f"NVMLError: {err}")
        return 0

def monitor_gpu_usage():
    interval = 5  # 检测间隔时间（秒）
    duration = 5 * 60  # 总监控时间（秒），这里是5分钟
    num_intervals = duration // interval
    utilizations = []

    try:
        while True:
            current_utilization = get_gpu_utilization()
            utilizations.append(current_utilization)

            if len(utilizations) > num_intervals:
                utilizations.pop(0)

            if len(utilizations) == num_intervals:
                avg_utilization = sum(utilizations) / len(utilizations)
                print(f"过去5分钟内GPU使用率的平均值: {avg_utilization:.2f}%")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("监控结束")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    monitor_gpu_usage()
