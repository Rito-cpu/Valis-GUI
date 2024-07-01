import inspect
import cv2

from valis import feature_detectors, preprocessing, registration, non_rigid_registrars
from src.core.keyword_store import FD_KEY, PROCESSOR_KEY, IF_PROCESSOR_KEY, BF_PROCESSOR_KEY
from sklearn.metrics.pairwise import _VALID_METRICS


def _get_subclasses(module, base_class, exclude=()):
    include_list = []
    module_members = inspect.getmembers(module)
    for name, obj in module_members:
        if inspect.isclass(obj):
            if issubclass(obj, base_class) and obj.__name__ != base_class.__name__ and obj.__name__ not in exclude:
                include_list.append(name)
    return include_list

def get_feature_detectors():
    """Get all feature detectors
    Returns
    -------
    default_fd : str
        Default feature detector

    feature_detector_names : list
        List of all feature detectors
    """
    default_fd = registration.DEFAULT_FD.__name__
    exclude_list = (
        feature_detectors.SkDaisy.__name__
    )
    feature_detector_names = _get_subclasses(feature_detectors, feature_detectors.FeatureDD, exclude_list)

    return default_fd, feature_detector_names

def get_image_processers():
    """Get all image processers

    Returns
    -------
    default_dict: dict
        Dictionary of default immunofluorescent and brightfield image processors

    processor_dict : dict
        Dictionary of all immunofluorescent and brightfield image processors.
        There are subdictionaries inside of each  processing dictionary (IF or BF), the keys
        of which are the processer names and the values are the arguments and
        default values that can be used to create each processor's widget.

    """
    default_bf = registration.DEFAULT_BRIGHTFIELD_CLASS.__name__
    default_if = registration.DEFAULT_FLOURESCENCE_CLASS.__name__
    exclude_list = ()
    processor_names = _get_subclasses(preprocessing, preprocessing.ImageProcesser, exclude_list)

    if_processors = [preprocessing.ChannelGetter.__name__]
    bf_pdict = {}
    if_pdict = {}
    for p_name in processor_names:
        p_cls = getattr(preprocessing, p_name)
        # p_args = inspect.signature(p_cls.process_image)
        # dir(p_args.parameters.items())
        p_args = inspect.getfullargspec(p_cls.process_image)

        if "self" in p_args.args:
            args = p_args.args[1:]
        else:
            args = p_args.args

        arg_dict = {args[i]: p_args.defaults[i] for i in range(len(args))}
        if p_name in if_processors:
            if_pdict[p_name] = arg_dict
        else:
            bf_pdict[p_name] = arg_dict

    processor_dict = {IF_PROCESSOR_KEY:if_pdict, BF_PROCESSOR_KEY:bf_pdict}
    default_dict = {IF_PROCESSOR_KEY:default_if, BF_PROCESSOR_KEY:default_bf}

    return default_dict, processor_dict

def get_feature_matching_metrics():
    """Get all feature matching metrics

    Returns
    --------
    fmm_list: list
        list of all available feature matching metrics, default (index 0) is "euclidean"
    """

    fmm_list = _VALID_METRICS.copy()

    return fmm_list


def get_similarity_metrics():
    """Get all similarity matching (sorting) metrics

    Returns
    --------
    sm_list: list
        list of all available sorting metrics, default (index 0) defined in registration.py
    """

    sm_list = _VALID_METRICS.copy()
    sm_list.insert(0, registration.DEFAULT_SIMILARITY_METRIC)

    return sm_list


def get_nonrigid_registrars():
    """Get all nonrigid registrars

        Returns
        --------
        nrr_list: list
            list of all available non-rigid registrars, default (index 0) defined in registration.py
        """

    nrr_list = [registration.DEFAULT_NON_RIGID_CLASS().method.split("_")[1]]
    nrr_to_append = [i.split("_")[1] for i in dir(cv2.optflow) if
                     (i.find("createOptFlow") != -1) and (i.find("Sparse") == -1) and i.split("_")[1] not in nrr_list]
    # appends only what appears after the underscore for each i that isn't the default

    nrr_list.extend(nrr_to_append)
    nrr_list.extend(["SimpleElastixWarper, SimpleElastixGroupwiseWarper"])

    return nrr_list


if __name__ == "__main__":
    # Get feature detector options
    default_fd, feature_detector_combobox_vals = get_feature_detectors()

    # Get image processor options
    default_processors, all_processors = get_image_processers()

    ## Get default immunofluorescent image processor and options
    IF_PROCESSOR_OPTIONS = all_processors[IF_PROCESSOR_KEY]
    DEFAULT_PROCESSOR_IF = default_processors[IF_PROCESSOR_KEY]
    default_if_processor_args = IF_PROCESSOR_OPTIONS[DEFAULT_PROCESSOR_IF]

    ## Get default brightfield image processor and options
    BF_PROCESSOR_OPTIONS = all_processors[BF_PROCESSOR_KEY]
    DEFAULT_PROCESSOR_BF = default_processors[BF_PROCESSOR_KEY]
    default_bf_processor_args = BF_PROCESSOR_OPTIONS[DEFAULT_PROCESSOR_BF]
