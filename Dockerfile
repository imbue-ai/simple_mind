FROM python:3.11-slim

# Install system dependencies including tini for proper signal handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    ca-certificates \
    curl \
    fd-find \
    git \
    git-lfs \
    jq \
    nano \
    openssh-server \
    procps \
    ripgrep \
    rsync \
    sqlite3 \
    tini \
    tmux \
    unison \
    wget \
    xxd \
    && rm -rf /var/lib/apt/lists/*

# Install ttyd binary from GitHub releases (not available via apt)
RUN ARCH=$(uname -m) && \
    curl -fsSL "https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.${ARCH}" \
    -o /usr/local/bin/ttyd && \
    chmod +x /usr/local/bin/ttyd

RUN mkdir -p -m 755 /etc/apt/keyrings \
	&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& apt update \
	&& apt install gh -y

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && echo 'PATH="/root/.local/bin:$PATH"' >> /root/.bashrc
ENV PATH="/root/.local/bin:$PATH"

# Install claude code (pass CLAUDE_CODE_VERSION as a build arg to pin a specific version)
ARG CLAUDE_CODE_VERSION=""
RUN curl -fsSL https://claude.ai/install.sh > /tmp/install_claude.sh && ( if [ -n "$CLAUDE_CODE_VERSION" ]; then cat /tmp/install_claude.sh | bash -s "$CLAUDE_CODE_VERSION"; else cat /tmp/install_claude.sh | bash; fi && test -x /root/.local/bin/claude ) || ( cat /tmp/install_claude.sh && exit 1 )
ENV CLAUDE_CODE_VERSION=${CLAUDE_CODE_VERSION}

# without this, there are some annoying bugs on modal's side with snapshotting
ENV UV_LINK_MODE=copy

# install python dependencies
RUN unset UV_INDEX_URL && uv tool install modal && uv tool install llm && llm install llm-anthropic && llm install llm-live-chat && llm install llm-matched-responses

# copy in all of our code:
COPY . /code/simple_mind/

# set working directory to the project root
WORKDIR /code/simple_mind/

# extract our code into the project directory
RUN git config --global --add safe.directory /code/simple_mind/ && chown -R root:root /code/simple_mind/

# add tk and mngr as a tool
RUN ln -s "/code/simple_mind/vendor/tk/ticket" ~/.local/bin/tk && uv tool install -e /code/simple_mind/vendor/mngr/libs/mngr && mngr plugin add --path vendor/mngr/libs/mngr_modal/ --path vendor/mngr/libs/mngr_llm/ --path vendor/mngr/libs/mngr_mind --path vendor/mngr/libs/mngr_claude --path vendor/mngr/libs/mngr_claude_mind --path vendor/mngr/libs/mngr_pi_coding --path vendor/mngr/libs/mngr_mind_chat/

# Run idly forever while being responsive to SIGTERM.
# PID 1 must explicitly install signal handlers in order to respect signals.
# `tail -f /dev/null` does not do this.
# Since `docker stop` issues a `SIGTERM`, we use an explicit `trap`.
# In practice, this appears to enable rapid interactions using `docker stop`.
CMD ["sh", "-c", "trap 'exit 0' TERM; tail -f /dev/null & wait"]
