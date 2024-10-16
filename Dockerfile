# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . /app

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用程序的端口
EXPOSE 5000

# 运行 Flask 应用程序
CMD ["python", "main.py"]
