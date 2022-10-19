#!/bin/bash
# Ask the user for their name
echo This script will test if the file /home/jovyan/local-channel/local_channel_env.yaml can solve
echo with the local channel /home/jovyan/local-channel
echo
echo Please enter docker image reference or tag below to be tested

read IMAGE_TAG

docker run -it --rm --entrypoint "/bin/bash" $IMAGE_TAG -c "source activate && cd /home/jovyan && mv /home/jovyan/local-channel/local_channel_env.yaml ./ && conda env create -f local_channel_env.yam"l


