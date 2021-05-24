# Docker file for lung_cnp ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-lung_cnp .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-lung_cnp .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-lung_cnp
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-lung_cnp
#

FROM python:3.9.1-slim-buster
LABEL maintainer="FNNDSC <dev@babyMRI.org>"

# Pass a UID on build command line (see above) to set internal UID
ARG UID=1001
ENV UID=$UID DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .
COPY . .
RUN pip --disable-pip-version-check install .                   \
    && useradd -u $UID -ms /bin/bash localuser                  \
    && apt update                                               \
    && apt-get install -y sudo                                  \
    && echo "localuser:localuser" | chpasswd                    \
    && addgroup localuser sudo                                  \
    && echo "localuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


CMD ["lung_cnp", "--help"]
