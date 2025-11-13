FROM --platform=linux/amd64 ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    libc6 \
    build-essential \
    && apt-get clean

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh &&  /bin/bash ~/miniconda.sh -b -p /opt/conda && rm ~/miniconda.sh

# Update PATH environment variable
ENV PATH /opt/conda/bin:$PATH

# Initialize Conda for non-interactive shells
RUN /opt/conda/bin/conda init bash

# Set up entrypoint
ENTRYPOINT ["/bin/bash"]
