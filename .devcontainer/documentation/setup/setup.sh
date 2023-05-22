#!/bin/bash

# Exit on error
set -e

function apt-packages {
    # Install apt packages

    apt-get update
    xargs apt-get install --yes < "packages.txt"
    rm -rf /var/lib/apt/lists/*
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
    container-user
}

main
