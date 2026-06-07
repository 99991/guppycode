FROM ubuntu:24.04

ARG UID=1000
ARG GID=1000

# Install without asking questions
ENV DEBIAN_FRONTEND=noninteractive

# Set timezone
ENV TZ="UTC"

RUN apt-get update && \
    apt-get -y install \
        bsdmainutils \
        binutils \
        build-essential \
        valgrind \
        gdb \
        curl \
        dnsutils \
        git \
        iputils-ping \
        jq \
        ltrace \
        make \
        net-tools \
        nmap \
        pkg-config \
        python3 \
        python3-pip \
        python3-venv \
        sqlite3 \
        strace \
        tree \
        unzip \
        w3m \
        wget \
        xxd \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    EXISTING_GROUP="$(getent group "${GID}" | cut -d: -f1 || true)"; \
    if [ -n "${EXISTING_GROUP}" ] && [ "${EXISTING_GROUP}" != "testuser" ]; then \
        groupmod -n testuser "${EXISTING_GROUP}"; \
    fi; \
    if ! getent group testuser >/dev/null; then \
        groupadd --gid "${GID}" testuser; \
    fi; \
    EXISTING_USER="$(getent passwd "${UID}" | cut -d: -f1 || true)"; \
    if [ -n "${EXISTING_USER}" ] && [ "${EXISTING_USER}" != "testuser" ]; then \
        usermod -l testuser "${EXISTING_USER}"; \
    fi; \
    if ! id -u testuser >/dev/null 2>&1; then \
        useradd --uid "${UID}" --gid "${GID}" --create-home --shell /bin/bash testuser; \
    fi; \
    usermod --uid "${UID}" --gid "${GID}" --home /home/testuser --move-home --shell /bin/bash testuser

# Switch to testuser
USER testuser

# Create and activate a virtual environment, then install Python packages
RUN python3 -m venv /home/testuser/testenv && \
    /home/testuser/testenv/bin/pip install --no-cache-dir \
        torch torchvision numpy scipy scikit-learn pillow pandas requests matplotlib transformers accelerate opencv-contrib-python-headless  && \
    rm -rf /home/testuser/testenv/share/python-wheels && \
    echo 'export PATH="/home/testuser/testenv/bin:$PATH"' >> ~/.bashrc && \
    echo 'alias p="python3"' >> ~/.bashrc

# Set PATH globally so that the venv's python/python3 is found first in all contexts
ENV PATH="/home/testuser/testenv/bin:$PATH"

# Set the working directory
WORKDIR /home/testuser

