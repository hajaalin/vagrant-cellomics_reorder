FROM ubuntu:14.04

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    python2.7 \
    mdbtools \
    && apt-get autoremove \
    && apt-get clean

# run as non-root user
RUN adduser lmu

# create share volumes for data
RUN mkdir /input

# run the conversion script when container is run
ENTRYPOINT ["python2.7", "cellomics_reorder.py"]

# add source and test directories
ADD python /python
ADD test /test
WORKDIR python

# run as root for now...
#USER lmu
