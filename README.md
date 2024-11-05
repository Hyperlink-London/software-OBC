# Hyperlink-OBC

## Overview

Hyperlink OBC (on board computer) is a Python-based application designed to control the Hyperlink pod.  It also sends data to the Hyperlink API.

## Installation

You can install the Hyperlink OBC via git:

```bash
git clone https://github.com/Hyperlink-London/hyperlink-OBC.git
cd hyperlink-OBC
```

then build the docker (you should install docker [here](https://www.docker.com/products/docker-desktop/))

```bash
docker build -t ros-obc .
```

## To run


You can run the Hyperlink OBC by running:

```bash
docker run -it ros-obc
```
