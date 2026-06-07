FROM node:latest

# Build-time args to match host user/group
ARG USERNAME=dev
ARG UID=1000
ARG GID=1000

# Create matching group/user and prepare writable dirs
RUN set -eux; \
    groupadd -g "$GID" "$USERNAME" || true; \
    if ! getent passwd "$UID" >/dev/null; then \
        useradd -m -u "$UID" -g "$GID" -s /bin/bash "$USERNAME"; \
    fi; \
    mkdir -p /workspace /home/"$USERNAME"/.npm-global /home/"$USERNAME"/.npm /home/"$USERNAME"/.cache; \
    chown -R "$UID:$GID" /workspace /home/"$USERNAME"

# Environment: user HOME and npm global prefix under HOME
ENV HOME=/home/$USERNAME
ENV NPM_CONFIG_PREFIX=$HOME/.npm-global
ENV npm_config_cache=$HOME/.npm
ENV PATH=$PATH:$HOME/.npm-global/bin

# Enable Corepack (yarn/pnpm shims)
RUN corepack enable

# Working directory
WORKDIR /workspace

# Run as host-matched UID:GID (numeric for reliability)
USER ${UID}:${GID}

# RUN chmod 777 /usr/local/bin/docker-entrypoint.sh \
#    && ln -s /usr/local/bin/docker-entrypoint.sh

# Default shell for interactive use
CMD ["bash"]
