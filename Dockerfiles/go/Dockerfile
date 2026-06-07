FROM golang:latest

# Build-time args to match host user/group
ARG USERNAME=dev
ARG UID=1000
ARG GID=1000

# Create a matching group/user if they don't already exist, and prepare writable dirs
RUN set -eux; \
    groupadd -g "$GID" "$USERNAME" || true; \
    if ! getent passwd "$UID" >/dev/null; then \
        useradd -m -u "$UID" -g "$GID" -s /bin/bash "$USERNAME"; \
    fi; \
    mkdir -p /go /workspace /home/"$USERNAME"; \
    chown -R "$UID:$GID" /go /workspace /home/"$USERNAME"

# Environment
ENV HOME=/home/$USERNAME
ENV GOPATH=/go
ENV GO111MODULE=on

# Working directory
WORKDIR /workspace

# Run as the host-matched UID:GID (numeric is reliable even if names differ)
USER ${UID}:${GID}

# Optional default command for interactive dev
CMD ["bash"]
