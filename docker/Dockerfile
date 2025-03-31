FROM python:3.9.10-slim

# Set working directory
WORKDIR /app

# Set environment so that Python modules resolve properly
ENV PYTHONPATH=/app
ENV LD_LIBRARY_PATH=/usr/lib
ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig

# Install system-level dependencies (libvips, glib, Java for VALIS)
RUN apt-get update
RUN apt-get install -y --fix-missing \
    libvips libvips-tools libglib2.0-0 default-jre \
    build-essential cmake python3-dev git
RUN apt-get clean

# Copy your VALIS scripts and valis/ subpackage
COPY src/core/scripts/valis/ /app/

# Copy shared core module
COPY src/core/keyword_store.py /app/keyword_store.py

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set entrypoint (can still override with CMD if needed)
ENTRYPOINT ["python3", "/app/launch_valis.py"]