# GazeAssist Docker Container
# For truly cross-platform deployment
#
# Build:
#   docker build -t gazeassist .
#
# Run (with webcam access):
#   Windows: docker run -it --device=/dev/video0 gazeassist
#   Linux: docker run -it --device=/dev/video0 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix gazeassist

FROM python:3.11-slim

# Install system dependencies for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgstreamer1.0-0 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY version1/requirements.txt /app/version1/
COPY version2/requirements.txt /app/version2/

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r version1/requirements.txt
RUN pip install --no-cache-dir -r version2/requirements.txt

# Copy project files
COPY . /app

# Set display for GUI (override with docker run -e DISPLAY=...)
ENV DISPLAY=:0

# Default command shows help
CMD ["python", "check_compatibility.py"]

# Alternatively run specific versions:
# CMD ["python", "version1/main.py"]
# CMD ["python", "version2/enhanced_tracker.py"]
