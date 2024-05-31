# Kuzco 监控脚本

## 需要你的点赞关注！ X 账户：https://x.com/188888_x

# 为了避免不必要的环境错误，请使用root账户来安装kuzco，并运行脚本！！！

## 简介

本脚本旨在一键多开启动并监控 Kuzco 在特定时间内产生的任务完成情况，以判断其运行状态是否异常。一旦监测到没有任务完成产生，则会自动重启 Kuzco。

## 功能特点

- 一键多开启动并实时监测 Kuzco 运行状态，确保正常运行。
- 支持自动重启功能，保障系统稳定性。
- 可选择性地启用 DC 推送功能，若不需要可轻松禁用。

## 使用说明

1. 在脚本开头可以轻松更改需要的参数。
2. 如何启用 DC 推送功能：
   - 填入你的webhook地址（创建 Webhook 机器人方法简单，详细步骤可参考谷歌搜索结果。）
   - 启动脚本时直接按回车键
3. 如果需要禁用 DC 推送功能，在启动时输入 `1` 启用。
4. 可使用tail -f /var/log/kuzco/log1.txt查看1号worker运行状态、其他的worker状态更改成2、3、4即可。

## 环境要求

- 适用于ubuntu22.04或者windows WSL的22.04版本
- 确保系统已安装 Python 3。（ubuntu22.04有默认安装）
- 若系统未安装 Python 3，可通过谷歌搜索安装方法。

## 使用方法

在终端中运行以下命令启动脚本：

```
python3 kz.py
```



#EN

# Kuzco Monitoring Script

## Don't forget to like and follow! X account: [https://x.com/188888_x](https://x.com/188888_x)

#To avoid unnecessary environmental errors, please use the root account to install kuzco and run the script!!!

## Introduction

This script aims to start and monitor Kuzco in multiple instances at specific times to determine if its task completion status is abnormal. If no tasks are completed, the script will automatically restart Kuzco.

## Features

- One-click multi-instance startup and real-time monitoring of Kuzco's operational status to ensure normal operation.
- Supports automatic restart functionality to ensure system stability.
- Optionally enable DC push notifications, which can be easily disabled if not needed.

## Instructions

1. You can easily change the required parameters at the beginning of the script.
2. How to enable the DC push notification feature:
   - Enter your webhook address (creating a Webhook bot is simple, detailed steps can be found via Google search).
   - Press the Enter key when starting the script.
3. To disable the DC push notification feature, enter `1` when starting.

## Requirements

- Applicable to Ubuntu 22.04 or Windows WSL version 22.04
- Ensure that Python 3 is installed on your system (Ubuntu 22.04 has it installed by default).
- If Python 3 is not installed, you can find installation methods via Google search.

## Usage

Run the following command in the terminal to start the script:

```
python3 kz.py
```
