# syntax=docker/dockerfile:1

FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG shell=/bin/bash
ENV SHELL=${shell}

ARG user=vscode
ARG group=vscode

ARG uid=1000
ARG gid=1000

WORKDIR /opt/devcontainer
COPY ./setup .

RUN /bin/bash ./setup.sh && \
    rm -rf /opt/devcontainer/

USER ${uid}:${gid}
