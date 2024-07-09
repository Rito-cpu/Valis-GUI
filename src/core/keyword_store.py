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

## Valis constructor parameters
SRC_DIR = "src_dir"
DST_DIR = "dst_dir"
SERIES = "series"
NAME = "name"
IMAGE_TYPE = "image_type"
FEATURE_DETECTOR_CLS = "feature_detector_cls"
TRANSFORMER_CLS = "transformer_cls"
AFFINE_OPTIMIZER_CLS = "affine_optimizer_cls"
SORTING_METRIC = "sorting_metric"
MATCH_FILTER_METHOD = "match_filter_method"
FEATURE_MATCHING_METRIC = "feature_matching_metric"
IMGS_ORDERED = "imgs_ordered"
NON_RIGID_REGISTRAR_CLS = "non_rigid_registrar_cls"
NON_RIGID_REG_PARAMS = "non_rigid_reg_params"
COMPOSE_NON_RIGID = "compose_non_rigid"
IMG_LIST = "image_list"
REFERENCE_IMG_F = "reference_img_f"
ALIGN_TO_REFERENCE = "align_to_reference"
DO_RIGID = "do_rigid"
CROP = "crop"
CREATE_MASKS = "create_masks"
DENOISE_RIGID = "denoise_rigid"
CROP_FOR_RIGID_REG = "crop_for_rigid_reg"
CHECK_FOR_REFLECTIONS = "check_for_reflections"
RESOLUTION_XYU = "resolution_xyu"
SLIDE_DIMS_DICT_WH = "slide_dims_dict_wh"
MAX_IMAGE_DIM_PX = "max_image_dim_px"
MAX_PROCESSED_IMAGE_DIM_PX = "max_processed_image_dim_px"
MAX_NON_RIGID_REGISTRAR_DIM_PX = "max_non_rigid_registrar_dim_px"
THUMBNAIL_SIZE = "thumbnail_size"
NORM_METHOD = "norm_method"
MICRO_RIGID_REGISTRAR_CLS = "micro_rigid_registrar_cls"
MICRO_RIGID_REGISTRAR_PARAMS = "micro_rigid_registrar_params"
QT_EMITTER = "qt_emitter"
IF_PROCESSOR = "if_processor"
IF_PROCESSING_CLS = "if_processing_cls"
IF_PROCESSING_KWARGS = "if_processing_kwargs"
BF_PROCESSOR = "bf_processor"
BRIGHTFIELD_PROCESSING_CLS = "brightfield_processing_cls"
BRIGHTFIELD_PROCESSING_KWARGS = "brightfield_processing_kwargs"
ADAPTIVE_EQ = "adaptive_eq"
CHANNEL = "channel"

## tooltips
TOOLTIP_IMAGE_PROCESSOR = ("The first step of VALIS registration in which samples are preprocessed to single channel " + 
                            "images to facilitate registration. Options represent available image processors. ")
TOOLTIP_FEATURE_DETECTOR = ("Identifies notable features to later be used for ordering images in the sample. Options " +
                            "represent available feature detectors." "Note that some selections may increase runtime " +
                            "significantly.")
TOOLTIP_FEATURE_MATCHING_METRIC = ("Matches individual features together within the sample and removes outliers. " +
                                    "Options represent available matching metrics.")
TOOLTIP_SORTING_METRIC = ("Measures the similarity between image pairs, which can be used to sort them " +
                            "accordingly. Options represent available similarity calculation algorithms.")
TOOLTIP_NON_RIGID_REG = ("Optional additional step in which VALIS will warp rigidly registered images to align " +
                            "features more closely than may be possible in rigid registration. Options represent " +
                            "available non rigid registrars.")
TOOLTIP_MICRO_RIGID_REG = ("Optional additional step in which VALIS will update rigid registration using a higher " +
                            "resolution version of the image. This will increase VALIS runtime and may not " +
                            "significantly improve results.")
