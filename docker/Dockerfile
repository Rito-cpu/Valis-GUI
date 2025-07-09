# Start from the optimized official image
FROM cdgatenbee/valis-wsi:1.2.0
# Do NOT download opencv here, inherit it from cdgatenbee/valis-wsi

USER root

# Install system dependencies first
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN /usr/bin/python3 -m pip install --no-cache-dir --upgrade pip --break-system-packages && \
    /usr/bin/python3 -m pip install --no-cache-dir --force-reinstall \
        "numpy<2" \
        opencv-contrib-python==4.9.0.80 \
        valis-wsi \
        --break-system-packages

RUN rm -rf /root/.local

WORKDIR /app

# Set environment so that Python modules resolve properly
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV PYTHONPATH=/app
ENV LD_LIBRARY_PATH=/usr/lib
ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig

COPY cv2_check.py /app/cv2_check.py

# Copy your VALIS scripts and valis/ subpackage
COPY src/core/scripts/valis/ /app/
# Copy shared core module
COPY src/core/keyword_store.py /app/keyword_store.py

# Keep the container alive (we'll run commands via docker exec)
CMD ["tail", "-f", "/dev/null"]
