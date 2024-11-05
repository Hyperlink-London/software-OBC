# Use the official ROS Noetic image as the base
FROM ros:noetic

# Set the working directory inside the container
WORKDIR /root/ros_workspace

# Copy fsm.py into the container
COPY /src/fsm.py /root/ros_workspace/fsm.py

# Install necessary ROS packages
RUN apt-get update && apt-get install -y \
    python3-rospy \
    ros-noetic-std-msgs \
    ros-noetic-smach

# Source the ROS setup file by default
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Set the script to run as the default command
CMD ["bash", "-c", "roscore & sleep 5; python3 /root/ros_workspace/fsm.py"]
