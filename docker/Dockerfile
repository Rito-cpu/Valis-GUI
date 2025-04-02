# Start from the optimized official image
FROM cdgatenbee/valis-wsi:latest

WORKDIR /app

# Set environment so that Python modules resolve properly
ENV PYTHONPATH=/app
ENV LD_LIBRARY_PATH=/usr/lib
ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig

# Copy your VALIS scripts and valis/ subpackage
COPY src/core/scripts/valis/ /app/

# Copy shared core module
COPY src/core/keyword_store.py /app/keyword_store.py

# Keep the container alive (we'll run commands via docker exec)
CMD ["tail", "-f", "/dev/null"]
