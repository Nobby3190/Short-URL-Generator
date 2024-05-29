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



# 安裝 FastAPI 和依賴
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# 複製當下目錄
COPY . /app/


# 啟動fastapi
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
