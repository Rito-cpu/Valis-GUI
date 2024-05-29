### HDF% Thumbnail suffixes
THMB_DIM = 512

### Status
PENDING_S: str = "Pending"
CONVERTING_S: str = "Converting"
PROCESSING_S: str = "Processing"
FEATURE_DETECT_S: str = "Detecting features (rigid)"
FEATURE_MATCHING_S: str = "Matching images (rigid)"
ALIGNING_COMMUNITIES_S: str = "Aligning communities (rigid)"
STITCHING_COMMUNITIES_S: str = "Stitching communities (rigid)"
OPTIMIZING_RIGID_S: str = "Optimizing rigid alignment (rigid)"
RIGID_S: str = "Rigid registration"
NON_RIGID_S: str = "Calculating deformation fields (non-rigid)"
COMPLETE_S: str = "Finished alignment"
IF_PROCESSOR_KEY = "if processor"
BF_PROCESSOR_KEY = "bf processor"

## ALIGNMENT CODE
RIGID_KEY: str = 'Rigid'
NON_RIGID_KEY: str = 'Non-Rigid'

## FEATURE
FD_KEY = "feature dd"
PROCESSOR_KEY = "image processors"
IF_PROCESSOR_KEY = "if processor"
BF_PROCESSOR_KEY = "bf processor"

## PROCESSOR TYPES
CHANNEL_GETTER_KEY = "ChannelGetter"
BG_COLOR_DISTANCE_KEY = "BgColorDistance"
COLORFUL_STANDARDIZER_KEY = "ColorfulStandardizer"
GRAY_KEY = "Gray"
HEDECONVOLUTION_KEY = "HEDeconvolution"
LUMINOSITY_KEY = "Luminosity"
STAIN_FLATTENER_KEY = "StainFlattener"
