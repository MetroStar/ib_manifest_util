#!/bin/bash
# Script for loosely recreating what will happen when files
# are push to the IB Repo.
# This script will build and run the docker image, allowing for
# testing of the environment build inside

LOCAL_CHANNEL_DIR=/path/to/local_channel
DOCKERFILE=/path/to/Dockerfile
TMPDIR=/output/tmpdir

# copy all packages in the local channel into the current directory
cp $LOCAL_CHANNEL_DIR/linux-64/* $TMPDIR
cp $LOCAL_CHANNEL_DIR/noarch/* $TMPDIR

# build the docker image
docker build -f $DOCKERFILE $TMPDIR -t ib_test
# run the docker image
docker run -it --rm --entrypoint bash ib_test
