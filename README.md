# Kuzco 监控脚本

## 需要你的点赞关注！ X 账户：@188888.X

## 简介

本脚本旨在监控 Kuzco 在特定时间内产生的任务完成情况，以判断其运行状态是否异常。一旦监测到没有任务完成产生，则会自动重启 Kuzco。

## 功能特点

- 实时监测 Kuzco 运行状态，确保正常运行。
- 支持自动重启功能，保障系统稳定性。
- 可选择性地启用 DC 推送功能，若不需要可轻松禁用。

## 使用说明

1. 在脚本开头可以轻松更改需要的参数。
2. 如何启用 DC 推送功能：
   - 填入你的webhook地址（创建 Webhook 机器人方法简单，详细步骤可参考谷歌搜索结果。）
   - 启动脚本时直接按回车键
3. 如果需要禁用 DC 推送功能，在启动时输入 `1` 启用。

## 环境要求

- 确保系统已安装 Python 3。
- 若系统未安装 Python 3，可通过谷歌搜索安装方法。
- 安装 Python 后，脚本可在所有平台通用。

## 使用方法

在终端中运行以下命令启动脚本：

```bash
python3 kz.sh
