import cv2

from valis import feature_detectors, preprocessing, non_rigid_registrars, feature_matcher


def get_feature_detector_obj(user_selection: str):
    """Return selected feature detector to VALIS

            Returns
            --------
            fd_obj: feature detector subclass
                uninitialized feature detector subclass object with name matching user selection
            """

    fd_obj = getattr(feature_detectors, user_selection)

    return fd_obj


def get_nonrigid_registrar_obj(user_selection: str):
    """Return selected nonrigid registrar to VALIS

            Returns
            --------
            nrr_obj: nonrigid registrar subclass
                uninitialized nonrigid registrar subclass object,
                if the user has selected a CV2 optical flow registrar, this will always be OpticalFlowWarper.

            optical_flow_dict: dict
                dictionary with a single key "optical_flow_obj" that holds the user selected
                optical flow object for initialization of the OpticalFlowWarper object.
                If the user has not selected a CV2 optical flow registrar, this will be set to None.
            """

    optical_flow_dict = {"optical_flow_obj": None}
    if user_selection.find("Simple") == -1:
        user_selection = "createOptFlow_" + user_selection

        optical_flow_obj = getattr(cv2.optflow, user_selection)
        nrr_obj = getattr(non_rigid_registrars, "OpticalFlowWarper")

        optical_flow_dict["optical_flow_obj"] = optical_flow_obj

    else:
        nrr_obj = getattr(non_rigid_registrars, user_selection)

    return nrr_obj, optical_flow_dict


def get_image_processor_obj(bf_selection: str, if_selection: str):
    """Return selected image processor to VALIS

            Returns
            --------
            bf_obj: image processor subclass
                uninitialized brightfield image processor subclass object with name matching user selection
                
            if_obj: image processor subclass
                uninitialized immunofluorescence image processor subclass object with name matching user selection
            """

    bf_obj = getattr(preprocessing, bf_selection)
    if_obj = getattr(preprocessing, if_selection)
    return bf_obj, if_obj


def get_matcher_obj(match_filter_method: str, feature_matching_metric: str, feature_detector: str):

    """

    Args:
        match_filter_method: matcher method obtained from matcher combobox
        feature_matching_metric: feature matching metric obtained from feature matcher combobox
        feature_detector: feature detector obtained from feature detector combobox

    Returns:
        m_obj: matcher object initialized with user selections

    """
    m_obj = None
    if match_filter_method != "SUPERGLUE":
        m_obj =  feature_matcher.Matcher(metric=feature_matching_metric, match_filter_method=match_filter_method)
    elif feature_detector == "SuperPointFD":
        m_obj = feature_matcher.SuperPointAndGlue()
    else:
        m_obj = feature_matcher.SuperGlueMatcher()
    return m_obj
