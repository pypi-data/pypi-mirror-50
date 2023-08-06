"""Module containing tools for EM-Bright classification of
compact binaries using trained supervised classifier
"""

import pickle
from os import path
import h5py

import numpy as np
import pkg_resources

from .computeDiskMass import compute_isco
from .computeDiskMass import computeDiskMass


def mchirp(m1, m2):
    return(m1 * m2)**(3./5.)/(m1 + m2)**(1./5.)


def q(m1, m2):
    return m2/m1 if m2 < m1 else m1/m2


def source_classification(m1, m2, chi1, chi2, snr,
                          ns_classifier=None,
                          emb_classifier=None):
    """
    Returns the predicted probability of whether a
    compact binary either has an EM counterpart or
    has a NS as one of its components

    Parameters
    ----------
    m1 : float
        primary mass
    m2 : float
        secondary mass
    chi1 : float
        dimensionless primary spin
    chi2 : float
        dimensionless secondary spin
    snr : float
        signal to noise ratio of the signal
    ns_classifier : object
        pickled object for NS classification
    emb_classifier : object
        pickled object for EM brightness classification

    Returns
    -------
    tuple
        (P_NS, P_EMB) predicted values.

    Notes
    -----
    By default the classifiers are trained using the
    ``KNearestNeighbor`` algorithm from ``scikit-learn``,
    data is used to make predictions. Custom `ns_classifier`,
    `emb_classifier` can be supplied so long as they provide
    ``predict_proba`` method and the feature set is
    [[mass1, mass2, spin1z, spin2z, snr]].

    Examples
    --------
    >>> from ligo import em_bright
    >>> em_bright.source_classification(2.0 ,1.0 ,0. ,0. ,10.0)
    (1.0, 1.0)
    """
    if not ns_classifier:
        ns_classifier = pickle.load(open(pkg_resources.resource_filename(
            __name__, 'data/knn_ns_classifier.pkl'), 'rb'))
    if not emb_classifier:
        emb_classifier = pickle.load(open(pkg_resources.resource_filename(
            __name__, 'data/knn_em_classifier.pkl'), 'rb'))

    features = [[m1, m2, chi1, chi2, snr]]
    prediction_em, prediction_ns = \
        emb_classifier.predict_proba(features).T[1], \
        ns_classifier.predict_proba(features).T[1]
    return prediction_ns[0], prediction_em[0]


def source_classification_pe(posterior_samples_file, hdf5=True, threshold=3.0):
    """
    Returns the predicted probability of whether a
    compact binary either has an EM counterpart or
    has a NS as one of its components from PE
    results.

    Returns
    -------
    tuple
        (P_NS, P_EMB) predicted values.


    Examples
    --------
    >>> from ligo import em_bright
    >>> em_bright.source_classification_pe('posterior_samples.hdf5')
    (1.0, 1.0)
    """
    if hdf5:
        data = h5py.File(posterior_samples_file)
        engine = list(data['lalinference'].keys())[0]
        samples = data['lalinference'][engine]['posterior_samples'][()]
    else:
        samples = np.recfromtxt(posterior_samples_file, names=True)
    mc = samples['mc']
    q = samples['q']
    m1 = mc * (1 + q)**(1/5) * (q)**(-3/5)
    m2 = mc * (1 + q)**(1/5) * (q)**(2/5)
    chi1 = samples['a1']
    chi2 = samples['a2']
    M_rem = computeDiskMass(m1, m2, chi1, chi2)
    prediction_ns = np.sum(m2 <= threshold)/len(m2)
    prediction_em = np.sum(M_rem > 0)/len(M_rem)

    return prediction_ns, prediction_em
