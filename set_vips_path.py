import os
import sys
import importlib.metadata
import site


# Add the path where libvips.42.dylib is located
vips_path = '/opt/homebrew/lib'  # Adjust this path based on where libvips is installed
if vips_path not in sys.path:
    sys.path.append(vips_path)

# Set DYLD_LIBRARY_PATH for macOS
if 'DYLD_LIBRARY_PATH' not in os.environ:
    os.environ['DYLD_LIBRARY_PATH'] = vips_path
else:
    os.environ['DYLD_LIBRARY_PATH'] += os.pathsep + vips_path


try:
    # Force Python to recognize scyjava as installed
    importlib.metadata.version("scyjava")
except importlib.metadata.PackageNotFoundError:
    # Manually add scyjava to sys.path
    site_packages = site.getsitepackages()
    for path in site_packages:
        scyjava_path = os.path.join(path, "scyjava")
        if os.path.exists(scyjava_path):
            sys.path.append(path)
            break