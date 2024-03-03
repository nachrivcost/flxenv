# Flux Version Manager

## Description

Flux Version Manager (flxenv) is a command-line tool designed to simplify the management of Flux CLI versions. It enables users to easily install, switch between, and manage different versions of Flux, the open-source tool that automates the deployment of applications to Kubernetes.

## Prerequisites

Before installing flxenv, make sure you have Python and pip installed on your system. Flux Version Manager is compatible with Python 3.6 and newer.

## Installation

To install Flux Version Manager, run the following command:

pip install flxenv

After installing flxenv, you need to add the directory where the Flux binaries are stored to your $PATH variable. This ensures that you can run Flux from any terminal session.

### For Bash Users:
echo 'export PATH="$HOME/flux/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

### For Zsh Users:
echo 'export PATH="$HOME/flux/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

## Usage

After installation, you can start using flxenv to manage your Flux CLI versions. Here are some common commands:

* To list all available Flux versions:

``` flxenv --list ```

* To install a specific version of Flux:

``` flxenv --install <version> ``` 

* To set a specific version of Flux as the current version:

``` flxenv --set-version <version> ```

* To list installed Flux versions:

``` flxenv --list-installed ```