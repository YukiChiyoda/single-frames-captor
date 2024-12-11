#!/bin/bash

# 检查 python3 和 venv 模块是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 请先安装 Python3"
    exit 1
fi

# 设置虚拟环境目录
ENV_DIR="./env"

# 如果虚拟环境不存在，创建它
if [ ! -d "$ENV_DIR" ]; then
    echo "创建虚拟环境..."
    python3 -m venv $ENV_DIR
    if [ $? -ne 0 ]; then
        echo "错误: 创建虚拟环境失败"
        exit 1
    fi
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source $ENV_DIR/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

echo "环境配置完成！"
echo "您现在已经在虚拟环境中。"
echo "使用 'deactivate' 命令可以退出虚拟环境。"

# 保持 shell 会话
exec $SHELL