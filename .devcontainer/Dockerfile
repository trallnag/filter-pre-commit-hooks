FROM  mcr.microsoft.com/devcontainers/base:ubuntu

USER vscode

# Perform general setup.
# Install packages with APT.
RUN <<-EOT
  set -eux

  mkdir -p ~/.local/bin

  export DEBIAN_FRONTEND=noninteractive

  sudo apt-get update

  sudo apt-get install --yes --no-install-recommends \
    build-essential \
    curl \
    gnupg2
EOT

# Set up Homebrew.
RUN <<-EOT
  set -eux

  export NONINTERACTIVE=1

  installer=https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh

  bash -c "$(curl --location --silent --show-error --fail $installer)"

  echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' \
    | tee --append \
      /home/vscode/.bashrc \
      /home/vscode/.zshrc
EOT

# Install tools with Homebrew.
RUN <<-EOT
	set -eux

  eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

  brew --version

	brew install --formula \
    just \
    shellcheck \
    shfmt \
    uv \
    yamlfmt
EOT

# Install tools with uv.
RUN <<-EOT
	set -eux

  eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

  uv --version

	uv tool install copier
  uv tool install mdformat
  uv tool install pre-commit
EOT
