#!/bin/bash
# 
# > ssh-keygen -t ed25519 -C "mattt.hoooper@gmail.com"
# > pbcopy < ~/.ssh/id_ed25519.pub
# > mkdir ~/workspace; cd ~/workspace
# > git clone git@github.com:M-J-Hooper/dotfiles.git
# > ./setup.sh

set -e

echo "🍺  Installing Homebrew packages..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/opt/homebrew/bin/brew shellenv)"

brew install \
  wget \
  curl \
  tmux \
  vim \
  zsh \
  jq \
  fzf

brew install --cask \
  iterm2 \
  karabiner-elements \
  visual-studio-code \
  spotify

echo "💣  Installing Oh My Zsh..."
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

echo "⛓️  Linking files..."
./create_links.sh
source ~/.zshrc

echo "🧹  Cleaning up..."
rm -rf /tmp/*
brew update
brew upgrade
brew cleanup

echo "✅  Setup complete!"
