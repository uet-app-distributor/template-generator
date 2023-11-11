#!/bin/bash

# Check if Docker is installed
if command -v docker &>/dev/null; then
  echo "Docker is already installed."
else
  # Install Docker
  echo "Docker is not installed. Installing Docker..."

  # Update the package index
  sudo apt update

  # Install necessary dependencies
  sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

  # Add Docker's official GPG key
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

  # Add Docker repository
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

  # Install Docker
  sudo apt update
  sudo apt install -y docker-ce docker-ce-cli containerd.io

  # Check if Docker installation was successful
  if command -v docker &>/dev/null; then
    echo "Docker has been successfully installed."
  else
    echo "Failed to install Docker. Please check the installation process."
    exit 1
  fi
fi
