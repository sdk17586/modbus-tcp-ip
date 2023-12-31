# ROS Melodic with Python 3 Dockerfile

# Use the ROS Melodic image as base
FROM osrf/ros:melodic-desktop-full

# Install Python 3 and pip3
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-yaml \
    python-catkin-tools \
    && rm -rf /var/lib/apt/lists/*

# Update Python 3 packages
RUN pip3 install --upgrade \
    setuptools \
    wheel \
    rospkg \
    catkin_pkg

# Setup catkin workspace with Python 3
ENV CATKIN_WS=/root/catkin_ws
RUN mkdir -p $CATKIN_WS/src
WORKDIR $CATKIN_WS
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && \
                  catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3"

# Automatically source ROS workspace with every new shell
RUN echo "source $CATKIN_WS/devel/setup.bash" >> ~/.bashrc

# Set the default command to bash
CMD ["bash"]

