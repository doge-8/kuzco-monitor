kuzco多开+GPU监控脚本

我使用的ubuntu系统，需要安装nvidia-smi为前提、安装方法输入一次nvidia-smi会提示安装命令。

在脚本内更改workers=来改变多大多开数量

##安装后使用授权
chmod 777 startkz.sh

##启动
./startkz.sh

启动-bash: ./startkz.sh: /bin/bash^M: bad interpreter: No such file or directory报错的话使用下面的方法启动解决

##安装dos2unix
sudo apt-get install dos2unix -y
##启动
dos2unix startkz.sh
