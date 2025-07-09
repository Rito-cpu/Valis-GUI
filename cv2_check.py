import cv2

print(f"OpenCV version: {cv2.__version__}")
print(f"cv2.optflow exists: {hasattr(cv2, 'optflow')}")
print(f"cv2.dnn.DictValue exists: {hasattr(cv2.dnn, 'DictValue')}")