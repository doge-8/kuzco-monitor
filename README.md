# Kuzco 监控脚本(最新版本2024.7.21编写)

## 已更新监控单独worker，某个worker异常的时候单独重启某个worker

## 需要你的点赞关注！ X 账户：https://x.com/188888_x

# 为了避免不必要的环境错误，请使用root账户来安装kuzco，并运行脚本！！！

## 简介

本脚本旨在一键多开启动并监控 Kuzco 在特定时间内产生的任务完成情况，以判断其运行状态是否异常。一旦监测到没有任务完成产生，则会自动重启 Kuzco。

## 功能特点

- 一键多开启动并实时监测 Kuzco 运行状态，确保正常运行。
- 支持自动重启功能，保障系统稳定性。

## 使用说明(使用kz.py，old.py是旧版本无法使用不需要使用！！！)

1. 在脚本开头可以轻松更改需要的参数。
2. 输入自己worker的启动号（在自己网页worker里点击Launch Worker后二级菜单中Register Worker内获取）
   <img width="486" alt="1718516732980" src="https://github.com/doge-8/kuzco-monitor/assets/84656053/23dd6593-41ab-400b-bab9-9c487a688ec2">


6. 可使用tail -f log/log1.txt查看1号worker运行状态、其他的worker状态更改成2、3、4即可。(在脚本的同目录使用)

## 环境要求

- 适用于全平台-所有cli版本kuzco、win系统使用wsl安装kuzco也可使用
- 确保系统已安装 最新版本kuzco、Python 3。（ubuntu22.04有默认安装）
- 若系统未安装 Python 3，可通过谷歌搜索安装方法。

## 使用方法

在终端中运行以下命令启动脚本：

```
python3 kz.py
```
