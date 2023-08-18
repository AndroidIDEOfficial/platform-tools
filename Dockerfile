# Use the official Ubuntu base image
FROM ubuntu:latest

# Install necessary packages using apt-get
RUN apt-get update \
    && apt-get install -y \
    python3 \
    python3-pip \
    git \
    golang \
    build-essential \
    cmake \
    ninja-build \
    bison \
    flex \
    wget \
    nano \
    zip \
    unzip \
    tar

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the URL for downloading Android NDK
ADD https://dl.google.com/android/repository/android-ndk-r26-rc1-linux.zip /tmp/android-ndk.zip

# Download and install Android NDK if it's not in the cache
RUN unzip /tmp/android-ndk.zip -d /usr/local \
    && rm /tmp/android-ndk.zip

# Set environment variable for Android NDK
ENV ANDROID_NDK_HOME /usr/local/android-ndk-r26-beta1

# Add the Android NDK to the PATH
ENV PATH $PATH:$ANDROID_NDK_HOME

# Install required Python packages
RUN pip3 install requests


# Optional: Set the working directory inside the container
# WORKDIR /path/to/your/project

# Optional: Copy your project files into the container
# COPY . /path/to/your/project

# Optional: Run any additional commands if needed
# RUN <command>

# Optional: Expose any necessary ports if your project requires it
# EXPOSE <port>

# Optional: Define the command that will run when the container starts
# CMD ["<command>", "<arg1>", "<arg2>", ...]
