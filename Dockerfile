# FROM python:3.9-slim
FROM python:3.10-slim

WORKDIR /app

ENV PYENV_ROOT="/opt/pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    && rm -rf /var/lib/apt/lists/*

# 安裝 pyenv
# RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

# # 安裝 Python 版本
# ARG PYTHON_VERSION=3.10.8
# RUN pyenv install $PYTHON_VERSION && pyenv global $PYTHON_VERSION


# # 建立虛擬環境
# ARG VENV_NAME=fastapi-venv
# RUN python -m venv $VENV_NAME
# ENV VIRTUAL_ENV="/app/$VENV_NAME"
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# 安裝 FastAPI 和依賴
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# 複製當下目錄
COPY . /app/


# 啟動fastapi
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
