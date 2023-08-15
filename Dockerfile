# 使用一个基础镜像，这里使用 Python 3.10
FROM python:3.10-bullseye

ENV PYTHONIOENCODING=utf-8

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装 ffmpeg
RUN \
    /bin/bash -c "echo -e 'deb http://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free\ndeb http://mirrors.ustc.edu.cn/debian-security/ bullseye-security main contrib non-free' > /etc/apt/sources.list"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt -y install ffmpeg

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY ./guag_bot /app

# 安装项目依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# 启动应用程序
CMD ["python", "main.py"]
