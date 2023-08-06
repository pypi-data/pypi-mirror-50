#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Victor Calderon
# Created      : 2018-05-14
# Last Modified: 2019-03-06
from __future__ import absolute_import, division, print_function
__author__     = ['Victor Calderon']
__copyright__  = ["Copyright 2018 Victor Calderon"]
__email__      = ['victor.calderon@vanderbilt.edu']
__maintainer__ = ['Victor Calderon']
__all__        = [  'Behroozi2010Relation',
                    'Moster2010Relation']

## Import modules
import numpy as np
import pandas as pd
from   cosmo_utils.utils             import file_utils as fd
from   cosmo_utils.custom_exceptions import LSSUtils_Error

## Functions and Classes

# Behroozi Relation class
class Behroozi2010Relation(object):
    """
    Class used to define the stellar-halo mass relation of
    central galaxies as a function of halo mass.
    """
    def __init__(self, **kwargs):
        r"""
        Parameters
        -----------
        input_h : {`int`, `float`} optional
            Value of the Hubble constant in limits of between :math:`[0, 1]`.
            This variable acts as the input `h` of variables, and it is set
            to `1` by default.

        out_h : {`int`, `float`} optional
            Value of the Hubble constant in limits of between :math:`[0, 1]`.
            This variable acts as the output `h` of variables, and it is set
            to `1` by default.
        """
        # Assigning variables
        self.input_h = kwargs.get('input_h', 1)
        self.out_h   = kwargs.get('out_h', 1)
        # Checking input parameters
        self._check_input_parameters()

    # Checking input parameters to make sure they are `expected`
    def _check_input_parameters(self):
        r"""
        Checks whether or not the input parameters are what is expected or not.
        """
        # Checking input types
        h_type_arr = (float, int)
        # `input_h` - Type
        if not (isinstance(self.input_h, h_type_arr)):
            msg = '`input_h` {0} is not a valid input type: {1}'
            msg = msg.format(type(self.input_h), h_type_arr)
            raise TypeError(msg)
        # Checking input values
        if not ((self.input_h > 0) and (self.input_h <= 1)):
            msg = '`input_h` ({0}) is not within the proper range [0, 1]!'
            msg = msg.format(self.input_h)
            raise ValueError(msg)
        # `out_h` - Type
        if not (isinstance(self.out_h, h_type_arr)):
            msg = '`out_h` {0} is not a valid input type: {1}'
            msg = msg.format(type(self.out_h), h_type_arr)
            raise TypeError(msg)
        # Checking input values
        if not ((self.out_h > 0) and (self.out_h <= 1)):
            msg = '`out_h` ({0}) is not within the proper range [0, 1]!'
            msg = msg.format(self.out_h)
            raise ValueError(msg)

    # Default dictionary to return to the user
    def _return_default_dict(self):
        r"""
        Creates the directory used for the end-user with input variables of
        the model.

        Returns
        -----------
        param_dict : `dict`
            Dictionary containing default model parameter values of
            Behroozi et al. (2010) paper, plus any additional input
            parameters to the model.
        """
        param_dict            = self._retrieve_model_default_dict()
        param_dict['input_h'] = self.input_h
        param_dict['out_h']   = self.out_h

        return param_dict

    # Default dictionary with input parameters
    def _retrieve_model_default_dict(self):
        r"""
        Dictionary of the default values of all model parameters set to the
        column 2 values in Table 2 of Behroozi et al. (2010) publication.

        Returns
        ----------
        d : `dict`
            Dictionary containing default model parameter values of
            Behroozi et al. (2010) paper.

        Notes
        ---------
        All calculations are done internally using the same h=0.7 units as
        in Behroozi et al. (2010), ['arXiv:1001.0015'] so the parameter values
        here are the same as in Table 2, even though the `mean_log_halo_mass`
        and `mean_stellar_mass` methods use accept and return arguments
        in ``h = 1`` units.
        """
        # Main dictionary
        d = ({'smhm_m0_0': 10.72,
            'smhm_m0_a': 0.59,
            'smhm_m1_0': 12.35,
            'smhm_m1_a': 0.3,
            'smhm_beta_0': 0.43,
            'smhm_beta_a': 0.18,
            'smhm_delta_0': 0.56,
            'smhm_delta_a': 0.18,
            'smhm_gamma_0': 1.54,
            'smhm_gamma_a': 2.52})

        return d

    # Mean relation of the model to compute the mean halo mass of galaxies.
    def mean_log_halo_mass(self, log_mstar, z=0):
        r"""
        Returns the halo mass of a central galaxy as a function of its stellar
        mass.

        Parameters
        -----------
        log_mstar : {`float`, `numpy.ndarray`, `list`}
            Logarithmic 10-base stellar mass array of the galaxies.

        z : {`float`, `int`}, optional
            Redshift of the halo hosting the galaxy. If passing an array,
            it must be the same length as the input `log_mstar`.

        Returns
        --------
        mass_dict : `dict`
            Dictionary with the logarithmic 10-base stellar mass and halo
            mass arrays in the same units as `self.out_h`.
        """
        # file_msg = fd.Program_Msg(__file__)
        file_msg = '>>>  '
        little_h = 0.7
        ## Checking input parameters
        # `log_mstar`
        log_mstar_valid_types = (int, float, np.ndarray, list)
        if not (isinstance(log_mstar, log_mstar_valid_types)):
            msg = '{0} `log_mstar` ({1}) is not a valid input type: {2}!'
            msg = msg.format(file_msg, type(log_mstar), log_mstar_valid_types)
            raise TypeError(msg)
        # `z` - Type
        z_valid_types = (int, float)
        if not (isinstance(z, z_valid_types)):
            msg = '{0} `z` ({1}) is not a valid input type: {2}!'
            msg = msg.format(file_msg, type(z), z_valid_types)
            raise TypeError(msg)
        # `z` - Value
        if not (z >= 0):
            msg = '{0} `z` ({1}) must be larger than `0`!'
            msg = msg.format(file_msg, z)
            raise ValueError(msg)
        #
        # Retrieving parameter dictionary
        param_dict = self._retrieve_model_default_dict()
        ## Checking units of `log_mstar` and converting to ``h = 0.7`` if
        ## necessary.
        # Converting stellar mass from units of `self.input_h` to `h == 1`
        # and to `h = 0.7`
        mstar_h1 = (10**log_mstar) * (self.input_h**2)
        # Converting to `h=0.7` units
        mstar    = mstar_h1 / (little_h**2)
        # Scale factor
        a = 1./(1. + z)
        # Behroozi function
        logm0 = param_dict['smhm_m0_0'] + (param_dict['smhm_m0_a'] * (a - 1))
        m0    = 10.**logm0
        logm1 = param_dict['smhm_m1_0'   ] + (param_dict['smhm_m1_a'] * (a - 1))
        beta  = param_dict['smhm_beta_0' ] + param_dict['smhm_beta_a' ]*(a - 1)
        delta = param_dict['smhm_delta_0'] + param_dict['smhm_delta_a']*(a - 1)
        gamma = param_dict['smhm_gamma_0'] + param_dict['smhm_gamma_a']*(a - 1)
        #
        stellar_mass_by_m0 = mstar / m0
        term3_numerator = stellar_mass_by_m0**delta
        term3_denominator = 1. + (stellar_mass_by_m0)**(-gamma)
        #
        # In units of `h = 0.7`
        log_halo_mass  = logm1 + (beta * np.log10(stellar_mass_by_m0))
        log_halo_mass += (term3_numerator / term3_denominator) - 0.5
        halo_mass      = 10.**log_halo_mass
        # Converting to desired units
        log_mstar_key = np.log10(mstar * (little_h**2) / (self.out_h**2))
        log_mhalo_key = np.log10(halo_mass * (little_h) / (self.out_h))
        # Saving to dictionary
        dict_names = ['log_mhalo', 'log_mstar']
        dict_vars  = [log_mhalo_key, log_mstar_key]
        mass_dict  = dict(zip(dict_names, dict_vars))

        return mass_dict

    def compute_example(self, log_mstar_min=8, log_mstar_max=12, mstep=500,
        return_pd=True):
        """
        Computes the ``Behroozi et al. (2010)`` relation for central galaxies.

        Parameters
        ------------
        log_mstar_min : {`float`, `int`}, optional
            Logarithmic 10-base minimum stellar mass. This variable is set to
            `10` by default.

        log_mstar_max : {`float`, `int`}, optional
            Logarithmic 10-base maximum stellar mass. This variable is set to
            `15` by default.

        mstep : {`float`, `int`} optional
            Number of elements in the output arrays of halo masses and
            stellar masses. This variable is set to `100` by default.

        return_pd : `bool`, optional
            If `True`, the function returns a `pandas.DataFrame` with the
            logarithmic 10-base halo masses and stellar masses of central
            galaxies in the units of `self.out_h`. This variable is set
            to `True` by default.

        Returns
        ---------
        mass_obj : {`dict`, `pandas.DataFrame`}
            Dictionary containing arrays or floats of the logarithmic
            10-base halo mass and stellar masses of central galaxies in
            units of `self.out_h`. If ``return_pd == True``, this function
            returns a `pandas.DataFrame` instead.
        """
        # Constants
        redshift = 0.
        # Defining logarithmic 10-base stellar mass array
        log_stellar_arr = np.linspace(log_mstar_min, log_mstar_max, mstep)
        # Computing dictionary of the Behroozi relation
        mass_dict = self.mean_log_halo_mass(log_stellar_arr, z=redshift)
        # Returning DataFrame if needed
        if return_pd:
            mass_obj = pd.DataFrame(mass_dict)
        else:
            mass_obj = mass_dict

        return mass_obj

class Moster2010Relation(object):
    """
    Class used to define the stellar-halo mass relation of
    central galaxies as a function of halo mass.
    """
    def __init__(self, **kwargs):
        r"""
        Parameters
        -----------
        input_h : {`int`, `float`} optional
            Value of the Hubble constant in limits of between :math:`[0, 1]`.
            This variable acts as the input `h` of variables, and it is set
            to `1` by default.

        out_h : {`int`, `float`} optional
            Value of the Hubble constant in limits of between :math:`[0, 1]`.
            This variable acts as the output `h` of variables, and it is set
            to `1` by default.
        """
        # Assigning variables
        self.input_h = kwargs.get('input_h', 1)
        self.out_h   = kwargs.get('out_h', 1)
        # Checking input parameters
        self._check_input_parameters()

    # Checking input parameters to make sure they are `expected`
    def _check_input_parameters(self):
        r"""
        Checks whether or not the input parameters are what is expected or not.
        """
        # Checking input types
        h_type_arr = (float, int)
        # `input_h` - Type
        if not (isinstance(self.input_h, h_type_arr)):
            msg = '`input_h` {0} is not a valid input type: {1}'
            msg = msg.format(type(self.input_h), h_type_arr)
            raise TypeError(msg)
        # Checking input values
        if not ((self.input_h > 0) and (self.input_h <= 1)):
            msg = '`input_h` ({0}) is not within the proper range [0, 1]!'
            msg = msg.format(self.input_h)
            raise ValueError(msg)
        # `out_h` - Type
        if not (isinstance(self.out_h, h_type_arr)):
            msg = '`out_h` {0} is not a valid input type: {1}'
            msg = msg.format(type(self.out_h), h_type_arr)
            raise TypeError(msg)
        # Checking input values
        if not ((self.out_h > 0) and (self.out_h <= 1)):
            msg = '`out_h` ({0}) is not within the proper range [0, 1]!'
            msg = msg.format(self.out_h)
            raise ValueError(msg)

    # Default dictionary to return to the user
    def _return_default_dict(self):
        r"""
        Creates the directory used for the end-user with input variables of
        the model.

        Returns
        -----------
        param_dict : `dict`
            Dictionary containing default model parameter values of
            Moster et al. (2010) paper, plus any additional input
            parameters to the model.
        """
        param_dict            = self._retrieve_model_default_dict()
        param_dict['input_h'] = self.input_h
        param_dict['out_h']   = self.out_h

        return param_dict

    # Default dictionary with input parameters
    def _retrieve_model_default_dict(self):
        r"""
        Dictionary of the default values of all model parameters set to the
        column 2 values in Table 2 of Moster et al. (2013) publication.

        Returns
        ----------
        d : `dict`
            Dictionary containing default model parameter values of
            Moster et al. (2010) paper.

        Notes
        ---------
        All calculations are done internally using the same h=0.7 units as
        in Moster et al. (2010), ['arXiv:0903.4682'] so the parameter values
        here are the same as in Table 2, even though the `mean_log_halo_mass`
        and `mean_stellar_mass` methods use accept and return arguments
        in ``h = 1`` units.
        """
        # Main dictionary
        d = ({'smhm_m1':11.899,
            'smhm_m_M_0':0.02817,
            'smhm_beta':1.068,
            'smhm_gamma':0.611})

        return d

    # Mean relation of the model to compute the mean halo mass of galaxies.
    def mean_log_stellar_mass(self, log_halo_mass, z=0):
        r"""
        Returns the halo mass of a central galaxy as a function of its halo
        mass.

        Parameters
        -----------
        log_halo_mass : {`float`, `numpy.ndarray`, `list`}
            Logarithmic 10-base halo mass array of the galaxies.

        z : {`float`, `int`}, optional
            Redshift of the halo hosting the galaxy. If passing an array,
            it must be the same length as the input `log_mstar`.

        Returns
        --------
        mass_dict : `dict`
            Dictionary with the logarithmic 10-base stellar mass and halo
            mass arrays in the same units as `self.out_h`.
        """
        # file_msg = fd.Program_Msg(__file__)
        file_msg = '>>>  '
        little_h = 0.72
        ## Checking input parameters
        # `log_halo_mass`
        log_halo_mass_valid_types = (int, float, np.ndarray, list)
        if not (isinstance(log_halo_mass, log_halo_mass_valid_types)):
            msg = '{0} `log_halo_mass` ({1}) is not a valid input type: {2}!'
            msg = msg.format(file_msg, type(log_halo_mass),
                log_halo_mass_valid_types)
            raise TypeError(msg)
        # `z` - Type
        z_valid_types = (int, float)
        if not (isinstance(z, z_valid_types)):
            msg = '{0} `z` ({1}) is not a valid input type: {2}!'
            msg = msg.format(file_msg, type(z), z_valid_types)
            raise TypeError(msg)
        # `z` - Value
        if not (z >= 0):
            msg = '{0} `z` ({1}) must be larger than `0`!'
            msg = msg.format(file_msg, z)
            raise ValueError(msg)
        #
        # Retrieving parameter dictionary
        param_dict = self._retrieve_model_default_dict()
        ## Checking units of `log_halo_mass` and converting to ``h = 0.7`` if
        ## necessary.
        # Converting halo mass from units of `self.input_h` to `h == 1`
        # and to `h = 0.7`
        halo_mass_h1 = (10**log_halo_mass) * (self.input_h)
        # Converting to `h=0.7` units
        halo_mass    = halo_mass_h1 / (little_h)
        # Scale factor
        a = 1./(1. + z)
        # Moster 2010 function
        halo_mass_by_m1 = halo_mass / (10.**param_dict['smhm_m1'])
        m_m1_beta       = halo_mass_by_m1**(-param_dict['smhm_beta'])
        m_m1_gamma      = halo_mass_by_m1**(param_dict['smhm_gamma'])
        inverse_term    = (m_m1_beta + m_m1_gamma)**(-1)
        mass_over_M     = 2. * param_dict['smhm_m_M_0'] * inverse_term
        mstar           = halo_mass * mass_over_M
        # Converting to desired units
        log_mstar_key = np.log10(mstar * (little_h**2) / (self.out_h**2))
        log_mhalo_key = np.log10(halo_mass * (little_h) / (self.out_h))
        # Saving to dictionary
        dict_names = ['log_mhalo', 'log_mstar']
        dict_vars  = [log_mhalo_key, log_mstar_key]
        mass_dict  = dict(zip(dict_names, dict_vars))

        return mass_dict

    def compute_example(self, log_mhalo_min=10, log_halo_max=15, mstep=500,
        return_pd=True):
        """
        Computes the ``Moster et al. (2010)`` relation for central galaxies.

        Parameters
        ------------
        log_mhalo_min : {`float`, `int`}, optional
            Logarithmic 10-base minimum halo mass. This variable is set to
            `10` by default.

        log_halo_max : {`float`, `int`}, optional
            Logarithmic 10-base maximum halo mass. This variable is set to
            `15` by default.

        mstep : {`float`, `int`} optional
            Number of elements in the output arrays of halo masses and
            halo masses. This variable is set to `100` by default.

        return_pd : `bool`, optional
            If `True`, the function returns a `pandas.DataFrame` with the
            logarithmic 10-base halo masses and stellar masses of central
            galaxies in the units of `self.out_h`. This variable is set
            to `True` by default.

        Returns
        ---------
        mass_obj : {`dict`, `pandas.DataFrame`}
            Dictionary containing arrays or floats of the logarithmic
            10-base halo mass and stellar masses of central galaxies in
            units of `self.out_h`. If ``return_pd == True``, this function
            returns a `pandas.DataFrame` instead.
        """
        # Constants
        redshift = 0.
        # Defining logarithmic 10-base stellar mass array
        log_mhalo_arr = np.linspace(log_mhalo_min, log_halo_max, mstep)
        # Computing dictionary of the Behroozi relation
        mass_dict = self.mean_log_stellar_mass(log_mhalo_arr, z=redshift)
        # Returning DataFrame if needed
        if return_pd:
            mass_obj = pd.DataFrame(mass_dict)
        else:
            mass_obj = mass_dict

        return mass_obj

## Retrieves default values for Behroozi et al. (2013)
def _retrieve_Behroozi_default_dict():
    """
    Dictionary of default values of all model parameters set to the
    column 2 values in Table 2 of Behroozi et al. (2013)

    Returns
    --------
    d : `dict`
        Dictionary containing default parameters for the Stellar-Halo
        Mass relation of Behroozi et al. (2013)

    Notes
    ----------
    All calculations are done internally ising the same h=0.7 units as
    in Behroozi ete al. (2010), ['arXiv:1001.0015'] so the parameter values
    here are the same as in Table 2, even though the `mean_log_halo_mass`
    and `mean_stellar_mass` methods use accept and return arguments in
    h=1 units.
    """
    ## Main dictionary
    d = ({'smhm_m0_0': 10.72,
        'smhm_m0_a': 0.59,
        'smhm_m1_0': 12.35,
        'smhm_m1_a': 0.3,
        'smhm_beta_0': 0.43,
        'smhm_beta_a': 0.18,
        'smhm_delta_0': 0.56,
        'smhm_delta_a': 0.18,
        'smhm_gamma_0': 1.54,
        'smhm_gamma_a': 2.52})

    return d

## Behroozi SHMR function
def Behroozi_relation(log_mstar, z=0.):
    """
    Returns the halo mass of a central galaxy as a function of its stellar
    mass.

    Parameters
    -----------
    log_mstar : `float` ,`np.ndarray`, or array-like
        Value or array of values of base-10 logarithm of stellar mass
        in h=1 solar mass units.

    z : int, float, `np.ndarray` or array-like
        Redshift of the halo hosting the galaxy. If passing an array,
        it must be of the same length as the input `log_mstar`.

    Returns
    -----------
    log_halo_mass : float or `np.ndarray`
        Array or float containing 10-base logarithm of halo mass in ``h=1``
        solar mass units.

    Notes
    ----------
    The parameter values in Behroozi+10 were fit to data assuming ``h=0.7``.
    Thus, we will transform our input stellar mass to ``h=0.7`` units,
    evaluate using the Behroozi parameters, and then transform back to
    ``h=1`` units before returning the result.
    """
    file_msg = fd.Program_Msg(__file__)
    little_h = 0.7
    ## Checking input parameters
    # `log_mstar`
    mstar_valid_types = (int, float, np.ndarray, list)
    if not (isinstance(log_mstar, mstar_valid_types)):
        msg = '{0} `log_mstar` ({1}) is not a valid type!'.format(
            file_msg, type(log_mstar))
        raise TypeError(msg)
    ##
    ## Behroozi dictionary
    param_dict = _retrieve_Behroozi_default_dict()
    ## COnverting stellar mass from ``h=1`` units to ``h=0.7`` units.
    mstar = (10.**log_mstar) / (little_h**2)
    ## Scale factor
    a = 1./(1. + z)
    ##
    ## Behroozi function
    logm0 = param_dict['smhm_m0_0'] + param_dict['smhm_m0_a']*(a - 1.)
    m0    = 10.**logm0
    logm1 = param_dict['smhm_m1_0'   ] + param_dict['smhm_m1_a'   ]*(a - 1)
    beta  = param_dict['smhm_beta_0' ] + param_dict['smhm_beta_a' ]*(a - 1)
    delta = param_dict['smhm_delta_0'] + param_dict['smhm_delta_a']*(a - 1)
    gamma = param_dict['smhm_gamma_0'] + param_dict['smhm_gamma_a']*(a - 1)
    #
    stellar_mass_by_m0 = mstar/m0
    term3_numerator    = (stellar_mass_by_m0)**delta
    term3_denominator  = 1. + (stellar_mass_by_m0)**(-gamma)
    #
    log_halo_mass = logm1 + beta*np.log10(stellar_mass_by_m0)
    log_halo_mass += (term3_numerator/term3_denominator) - 0.5
    #
    # Convert back from ``h=0.7`` to ``h=1`` units
    return np.log10((10.**log_halo_mass)*(little_h))

## Retrieves default values for Moster et al. (2010)
def _retrieve_Moster_default_dict():
    """
    Dictionary of default values of all model parameters set to the
    column 2 values in Table 2 of Moster et al. (2010)

    Returns
    --------
    d : `dict`
        Dictionary containing default parameters for the Stellar-Halo
        Mass relation of Moster et al. (2010)

    Notes
    ----------
    All calculations are done internally using the same h=0.7 units as
    in Moster et al. (2010), ['arXiv:0903.4682'] so the parameter values
    here are the same as in Table 2, even though the `mean_log_halo_mass`
    and `mean_stellar_mass` methods use accept and return arguments in
    h=1 units.
    """
    ## Main dictionary
    d = ({'smhm_m1':11.899,
        'smhm_m_M_0':0.02817,
        'smhm_beta':1.068,
        'smhm_gamma':0.611})

    return d

## Moster SHMR function
def Moster2010_relation(log_halo_mass, return_h0=False):
    """
    Returns the halo mass of a central galaxy as a function of its stellar
    mass.

    Parameters
    -----------
    log_halo_mass : `float` ,`np.ndarray`, or array-like
        Value or array of values of base-10 logarithm of halo mass
        in ``h = 1`` solar mass units.

    return_h0 : `bool`, optional
        If `True`, the function returns both stellar mass and halo mass
        arrays in units of ``h = 1`` units.

    Returns
    -----------
    mass_dict : `dict`
        Dictionary containing arrays or floats containing 10-base logarithm
        of halo mass and stellar mass of central galaxies in units of
        either ``h = 1`` or ``h = 0.7``. The units of ``h`` depend on the
        choice of ``return_h0``.

    Notes
    ----------
    The parameter values in Moster+10 were fit to data assuming ``h=0.7``.
    Thus, we will transform our input stellar mass to ``h=0.7`` units,
    evaluate using the Moster parameters, and then transform back to
    ``h=1`` units before returning the result.
    """
    # file_msg = fd.Program_Msg(__file__)
    file_msg = '>>>'
    little_h = 0.72
    ## Checking input parameters
    # `log_halo_mass`
    mstar_valid_types = (int, float, np.ndarray, list)
    if not (isinstance(log_halo_mass, mstar_valid_types)):
        msg = '{0} `log_halo_mass` ({1}) is not a valid type!'.format(
            file_msg, type(log_halo_mass))
        raise LSSUtils_Error(msg)
    ##
    ## Moster dictionary
    param_dict = _retrieve_Moster_default_dict()
    # Converting halo mass from h=1 to h=0.7
    log_halo_mass -= np.log10(little_h)
    halo_mass = (10.**log_halo_mass)
    ##
    ## Moster function
    mass_over_m1 = halo_mass / (10.**param_dict['smhm_m1'])
    m_m1_beta    = mass_over_m1**(-1. * param_dict['smhm_beta'])
    m_m1_gamma   = mass_over_m1**(param_dict['smhm_gamma'])
    inverse_term = (m_m1_beta + m_m1_gamma)**(-1)
    mass_over_M  = 2. * param_dict['smhm_m_M_0'] * inverse_term
    stellar_mass = halo_mass * mass_over_M
    # Converting to log-scale
    log_stellar_mass = np.log10(stellar_mass)
    # Choosing which values to return
    if (return_h0):
        # Returns both masses in units of ``h = 1``
        log_stellar_mass += np.log10(little_h**2)
        log_halo_mass    += np.log10(little_h)
    # Dictionary of masses
    return_obj = [log_halo_mass, log_stellar_mass]
    mass_dict = dict(zip(['m_halo', 'm_stellar'], return_obj))

    return mass_dict

def Moster_example(logmhalo_min=11, logmhalo_max=15, return_h0=True):
    """
    Computes the ``Moster et al. (2010)`` relation and returns a dictionary
    of stellar masses and halo masses of central galaxies

    Parameters
    ------------
    

    return_h0 : `bool`, optional
        If `True`, the function returns both stellar mass and halo mass
        arrays in units of ``h = 1`` units.

    Returns
    ------------
    mass_dict : `dict`
        Dictionary containing arrays or floats containing 10-base logarithm
        of halo mass and stellar mass of central galaxies in units of
        either ``h = 1`` or ``h = 0.7``. The units of ``h`` depend on the
        choice of ``return_h0``.
    """
    # file_msg = fd.Program_Msg(__file__)
    file_msg = '>> '
    # Constants
    dlogM = 1000
    # Checking input parameters
    # `logmhalo_min`
    mhalo_min_max_type = (float, int)
    if not (isinstance(logmhalo_min, mhalo_min_max_type)):
        msg = '{0} `logmhalo_min` ({1}) is not a valid input type: {2}'
        msg = msg.format(file_msg, type(logmhalo_min), mhalo_min_max_type)
        raise TypeError(msg)
    else:
        logmhalo_min = float(logmhalo_min)
    # `logmhalo_max`
    if not (isinstance(logmhalo_max, mhalo_min_max_type)):
        msg = '{0} `logmhalo_max` ({1}) is not a valid input type: {2}'
        msg = msg.format(file_msg, type(logmhalo_max), mhalo_min_max_type)
        raise TypeError(msg)
    else:
        logmhalo_max = float(logmhalo_max)
    # Checking relation between `logmhalo_min` and `mhalo_max`
    if not (logmhalo_min < logmhalo_max):
        msg = '{0} `logmhalo_min` ({1}) must be smaller than `logmhalo_max` '
        msg = '({2})!'
        msg = msg.format(file_msg, logmhalo_min, logmhalo_max)
        raise ValueError(msg)
    # Creating array of halo masses in units of ``h = 1``
    log_halo_mass_arr = np.linspace(logmhalo_min, logmhalo_max, dlogM)
    # Computing stellar masses
    mass_dict = Moster2010_relation(log_halo_mass_arr, return_h0=return_h0)

    return mass_dict
