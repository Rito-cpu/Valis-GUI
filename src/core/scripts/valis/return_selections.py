import cv2

from valis import feature_detectors, preprocessing, non_rigid_registrars, feature_matcher, affine_optimizer, micro_rigid_registrar
import skimage.transform


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

    if user_selection is None:
        return None, None

    optical_flow_dict = {"optical_flow_obj": None}
    if user_selection.find("SimpleElastix") == -1:
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
    if match_filter_method != "superglue":
        m_obj = feature_matcher.Matcher(metric=feature_matching_metric, match_filter_method=match_filter_method)
    elif feature_detector == "SuperPointFD":
        m_obj = feature_matcher.SuperPointAndGlue()
    else:
        m_obj = feature_matcher.SuperGlueMatcher()
    return m_obj


def get_image_transformer(selection: bool):
    """

    Args:
        selection: user selection to allow image scaling

    Returns:
        transformer_obj: uninitialized transformer object to be passed into transformer_cls parameter on start of Valis
    """
    transformer_obj = None
    if selection is True:
        transformer_obj = skimage.transform.SimilarityTransform
    else:
        transformer_obj = skimage.transform.EuclideanTransform

    return transformer_obj


def get_affine_optimizer(selection: bool):
    """

    Args:
        selection: user selection to maximize mutual information

    Returns: optimizer_obj: uninitialized optimizer object to be passed into affine_optimzer_cls parameter on start
    of Valis. Will be None if the user selected not to maximize mutual information.
    """

    optimizer_obj = None

    if selection:
        optimizer_obj = affine_optimizer.AffineOptimizerMattesMI

    return optimizer_obj


def get_micro_rigid_registrar(selection: bool):
    """

    Args:
        selection: user choice to do micro rigid registration

    Returns: micro_rigid_registrar_obj: uninitialized micro rigid registrar object to be passed into
    micro_rigid_registrar_cls parameter on start of Valis, will be None if the user selected not to do micro rigid
    registration.
    """

    micro_rigid_registrar_obj = None
    if selection:
        micro_rigid_registrar_obj = micro_rigid_registrar.MicroRigidRegistrar
    return micro_rigid_registrar_obj
