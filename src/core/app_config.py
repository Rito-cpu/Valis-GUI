import os
import sys

from src.core.keyword_store import *
from src.core.scripts.valis.gui_options import *


# Project root directory
APP_ROOT = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)

# Image resources directory
image_dir = "resources/images"
IMG_RSC_PATH = os.path.join(APP_ROOT, image_dir)

# --- Home Directory Instance ---
PROJECT_DIRECTORY = None

# --- Valis Imports ---
DEFAULT_FD = None
DETECTORS = None
try:
    DEFAULT_FD, DETECTORS = get_feature_detectors()
except Exception as error:
    print('Valis detector import failed. Exiting application...')
    sys.exit(1)

COMBINED_PROCESSOR_OPTIONS = []
IF_PROCESSOR_OPTIONS = None
DEFAULT_PROCESSOR_IF = None
BF_PROCESSOR_OPTIONS = None
DEFAULT_PROCESSOR_BF = None
try:
    default_processors, all_processors = get_image_processers()

    IF_PROCESSOR_OPTIONS = all_processors[IF_PROCESSOR_KEY]
    DEFAULT_PROCESSOR_IF = default_processors[IF_PROCESSOR_KEY]
    default_if_processor_args = IF_PROCESSOR_OPTIONS[DEFAULT_PROCESSOR_IF]

    BF_PROCESSOR_OPTIONS = all_processors[BF_PROCESSOR_KEY]
    DEFAULT_PROCESSOR_BF = default_processors[BF_PROCESSOR_KEY]
    default_bf_processor_args = BF_PROCESSOR_OPTIONS[DEFAULT_PROCESSOR_BF]

    for item in IF_PROCESSOR_OPTIONS.keys():
        COMBINED_PROCESSOR_OPTIONS.append(item)
    for item in BF_PROCESSOR_OPTIONS.keys():
        COMBINED_PROCESSOR_OPTIONS.append(item)
except Exception as error:
    print('Valis processors import failed. Exiting application...')
    sys.exit(1)

FMM_LIST = None
try:
    FMM_LIST = get_feature_matching_metrics()
except Exception as error:
    print('Valis feature matching metric import failed. Exiting application...')
    sys.exit(1)

SM_LIST = None
try:
    SM_LIST = get_similarity_metrics()
except Exception as error:
    print('Valis similarity metric import failed. Exiting application...')
    sys.exit(1)

NONRIGID_REGISTRARS = None
try:
    NONRIGID_REGISTRARS = get_nonrigid_registrars()
except Exception as error:
    print('Valis non-rigid registrar import failed. Exiting application...')
    sys.exit(1)

MATCH_FILTERS = None
try:
    MATCH_FILTERS = get_matchers()
except Exception as error:
    print('Valis match filter import failed. Exiting application...')
    sys.exit(1)

# --- Menu States ---
"""
    Menu States represent menu completion states and
    are used to determine which menu is enabled.
    0 = Incomplete (No data was submitted and passed)
    1 = Complete
"""
INCOMPLETE = 0
COMPLETE = 1

UPLOAD_STATE = INCOMPLETE
REGISTRATION_STATE = INCOMPLETE
RESULTS_STATE = INCOMPLETE
EXPORT_STATE = INCOMPLETE

# Menu Data Storage
UPLOADED_DATA = None
