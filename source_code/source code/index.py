from simple_facerec import SimpleFacerec
import cv2
import base64
import numpy as np
import requests
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning






sfr = SimpleFacerec()
sfr.detect_and_display_faces()
