#!/bin/bash

# Exit on error
set -e

function apt-packages {
    # Install apt packages

    apt-get update
    xargs apt-get install --yes < "packages.txt"
    rm -rf /var/lib/apt/lists/*
}

function pip-requirements {
    # Install pip requirements
    PYTHONDONTWRITEBYTECODE=1
    PYTHONUNBUFFERED=1

    python -m venv /opt/venv/
    pip install -r requirements.txt
    chown -R ${uid}:${gid} /opt/venv/
}

function container-user {
    # Add container user

    groupadd --gid ${gid} ${group}
    useradd --uid ${uid} --gid ${group} --create-home ${user}

    adduser ${user} sudo
    echo "${user} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${user}
}

function main {
    apt-packages
    pip-requirements
    container-user
}

main
