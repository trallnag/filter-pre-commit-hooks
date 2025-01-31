FROM  mcr.microsoft.com/devcontainers/python:latest

USER vscode

# Perform general setup.
# Install additional packages with APT.
RUN <<-EOT
  set -eux

  mkdir -p ~/.local/bin
  mkdir -p ~/.local/share/bash-completion/completions

  export DEBIAN_FRONTEND=noninteractive

  sudo apt-get update

  sudo apt-get install --yes --no-install-recommends \
    curl \
    dnsutils \
    gnupg2
EOT

# Install additional packages with pipx.
RUN <<-EOT
	set -eux

  pipx --version

	pipx install \
    copier \
    pre-commit \
    uv
EOT

# Install Task with the official installer.
# Set up completion in Bash.
RUN <<-EOT
	set -eux

  curl --location --silent --show-error --fail \
    https://taskfile.dev/install.sh \
    | sh -s -- -b ~/.local/bin

  ~/.local/bin/task --version

  ~/.local/bin/task --completion bash \
    > ~/.local/share/bash-completion/completions/task
EOT
