#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Victor Calderon
# Created      : 2018-04-28
# Last Modified: 2018-04-28
from __future__ import absolute_import, division, print_function
__author__     = ['Victor Calderon']
__copyright__  = ["Copyright 2018 Victor Calderon"]
__email__      = ['victor.calderon@vanderbilt.edu']
__maintainer__ = ['Victor Calderon']
__all__        = [  "myceil",
                    "myfloor",
                    "Bins_array_create",
                    "sigma_calcs",
                    "Stats_one_arr",
                    "Stats_one_arr_mod"]
"""
Set of statistical functions
"""

## Import modules
import math
import numpy as np
from   scipy import stats as sstats
from   cosmo_utils.utils             import file_utils as fd
from   cosmo_utils.custom_exceptions import LSSUtils_Error

## Functions

# Upper-bound values
def myceil(x, base=10):
    """
    Determines the upper-bound interger for a given number with a given base.

    Parameters
    ----------
    x : float
        Number to be approximated to closest number to `base`

    base : float
        Base used to calculate the closest largest number

    Returns
    ----------
    y : float
        Closest float number to `x`, i.e. upper-bound float

    Examples
    ----------
    >>> myceil(12, 10)
    20.0

    >>> myceil(12.05, 1.)
    13.0

    >>> myceil(12.05, 0.5)
    12.5
    """
    y = float(base * math.ceil(float(x)/base))

    return y

## Lower-bound values
def myfloor(x, base=10):
    """
    Determines the lower-bound interger for a given number with a given base.

    Parameters
    ----------
    x : float
        Number to be approximated to closest number to `base`

    base : float
        Base used to calculate the closest largest number

    Returns
    ----------
    y : float
        Closest float number to `x`, i.e. upper-bound float

    Examples
    ----------
    >>> myfloor(12, 10)
    10.0

    >>> myfloor(12.05, 1.)
    12.0

    >>> myfloor(12.05, 0.2)
    12.0
    """
    y = float(base * math.floor(float(x)/base))

    return y

## Generation of bins evenly spaced out
def Bins_array_create(arr, base=10, return_tuple=False):
    """
    Generates an evenly-spaced array between the minimum and maximum value
    of a given array,

    Parameters
    ----------
    arr : array_like
        Array of of numbers or floats

    base : `int` or `float`, optional
        Interval used to create the evenly-spaced array of elements

    return_tuple : `bool`, optional
        If `True`, the function returns a set of tuples for each bin. This
        variable  is set to `False` by default.

    Returns
    ----------
    bins_arr : `numpy.ndarray`
        Array of elements separated in intervals of `base`
    """
    file_msg = fd.Program_Msg(__file__)
    # Transforming input data
    base = float(base)
    arr = np.asarray(arr)
    # Checking array dimensions
    if arr.ndim != 1:
        msg = '{0} The input array is not of dimension 1, but of `{1}`'.format(
            file_msg, arr.ndim)
        raise LSSUtils_Error(msg)
    # Creating evenly-spaced array
    arr_min  = myfloor(arr.min(), base=base)
    arr_max  = myceil(arr.max(), base=base)
    bins_arr = np.arange(arr_min, arr_max + 0.5*base, base)
    # Creating tuple if necessary
    if return_tuple:
        bins_arr_mod = (np.array([[bins_arr[ii], bins_arr[ii+1]]
                            for ii in range(len(bins_arr) - 1)]))
        return_obj = bins_arr_mod
    else:
        return_obj = bins_arr

    return return_obj

## Calculations of percentiles and sigmas
def sigma_calcs(data_arr, type_sigma='std', perc_arr=[68., 95., 99.7],
    return_mean_std=False):
    """
    Calcualates the 1-, 2-, and 3-sigma ranges for `data_arr`

    Parameters
    -----------
    data_arr : `numpy.ndarray`, shape( param_dict['nrpbins'], param_dict['itern_tot'])
        array of values, from which to calculate percentiles or St. Dev.

    type_sigma : {'perc', 'std'} string, optional (default = 'std')
        Option for calculating either `percentiles` or `standard deviations`
            - 'perc': calculates percentiles
            - 'std' : uses standard deviations as 1-, 2-, and 3-sigmas

    perc_arr : array_like, optional (default = [68., 95., 99.7])
        Array of percentiles to calculate

    return_mean_std : `bool`, optional (default = False)
        Option for returning mean and St. Dev. along with `sigma_dict`

    Return
    ----------
    sigma_dict: python dicitionary
        dictionary containg the 1-, 2-, and 3-sigma upper and lower
        ranges for `data-arr`

    mark_mean: array_like
        array of the mean value of `data_arr`.
        Only returned if `return_mean_std == True`

    mark_std: array_like
        array of the St. Dev. value of `data_arr`.
        Only returned if `return_mean_std == True`
    """
    file_msg = fd.Program_Msg(__file__)
    ## Checking input variables
    # `data_arr`
    data_arr_valid_types = (np.ndarray, list)
    if not (isinstance(data_arr, data_arr_valid_types)):
        msg = '{0} `data_arr` ({1}) is not a valid type!'.format(
            file_msg, type(data_arr))
        raise LSSUtils_Error(msg)
    else:
        data_arr = np.asarray(data_arr)
    # `type_sigma`
    type_sigma_valid = ['perc', 'std']
    if not (isinstance(type_sigma, str)):
        msg = '{0} `type_sigma` ({1}) is not a valid type!'.format(
            file_msg, type(type_sigma))
        raise LSSUtils_Error(msg)
    if not (type_sigma in type_sigma_valid):
        msg = '{0} `type_sigma` ({1}) is not a valid input choice!'.format(
            file_msg, type_sigma)
    ## Determining if the object is a list of list or not
    data_arr_type = [[] for x in range(len(data_arr))]
    arr_type      = (np.ndarray, list)
    # Checking type of input parameter
    for zz, data_zz in enumerate(data_arr):
        data_arr_type[zz] = isinstance(data_zz, arr_type)
    # Choosing axis
    if (all([(zz == True) for zz in data_arr_type])):
        # If `data_arr` is a list of lists
        list_opt = True
        # Checking data dimension
        if (data_arr.ndim == 1):
            # Array of multiple elements in each bin
            ax_opt = True
        else:
            # Same number of elements in each bin
            ax_opt = False
    else:
        # If `data_arr` is a 1D array
        list_opt = False
        # Checking data dimension
        if (data_arr.ndim == 1):
            ax_opt = False
        else:
            msg = '{0} Invalid input of `data_arr`'.format(file_msg)
            raise TypeError(msg)
    # Determining `mean` and `standard deviation`
    if list_opt:
        # If different number of elements in each bin
        if ax_opt:
            # Number of bins in `data_arr`
            nbins = len(data_arr)
            # Calculating statistics
            mark_mean = np.zeros(nbins) * np.nan
            mark_std  = np.zeros(nbins) * np.nan
            # Calculating `mean` and `stdev` for each bin
            for ii, data_ii in enumerate(data_arr):
                mark_mean[ii] = np.nanmean(data_ii, axis=0)
                mark_std [ii] = np.nanstd( data_ii, axis=0)
        else:
            # Calculating `mean` and `stdev` for each bin
            mark_mean = np.nanmean(data_arr, axis=1)
            mark_std  = np.nanstd( data_arr, axis=1)
    else:
        # When dealing with a 1D array
        mark_mean = np.nanmean(data_arr, axis=0)
        mark_std  = np.nanstd( data_arr, axis=0)
    #
    ## Determining errors in each bin
    # Creating dictionary for saving `sigma`s
    sigma_dict = {ii: [] for ii in range(len(perc_arr))}
    # Using percentiles to estimate errors
    if (type_sigma == 'perc'):
        # If `data_arr` is a list
        if list_opt:
            # If different number of elements in each bin
            if ax_opt:
                # Number of bins in `data_arr`
                nbins = len(data_arr)
                # Looping over sigma values
                for zz, perc_zz in enumerate(perc_arr):
                    # Defining lower and upper ranges
                    mark_lims = np.zeros((nbins, 2)) * np.nan
                    # Populating lower and upper limits
                    for ii, data_ii in enumerate(data_arr):
                        perc_lims  = [50 - (perc_zz/2.), 50 + (perc_zz/2.)]
                        mark_lower = np.nanpercentile(data_ii, perc_lims[0])
                        mark_upper = np.nanpercentile(data_ii, perc_lims[1])
                        # Saving to `mark_lims`
                        mark_lims[ii] = [mark_lower, mark_upper]
                    # Saving to `sigma_dict`
                    sigma_dict[zz] = mark_lims.T
            else:
                # If same number of elements in each bin
                # Looping over sigma values
                for zz, perc_zz in enumerate(perc_arr):
                    perc_lims  = [50 - (perc_zz/2.), 50 + (perc_zz/2.)]
                    mark_lower = np.nanpercentile(data_arr, perc_lims[0], axis=1)
                    mark_upper = np.nanpercentile(data_arr, perc_lims[1], axis=1)
                    mark_lims  = np.column_stack((mark_lower, mark_upper))
                    # Saving to dictionary
                    sigma_dict[zz] = mark_lims.T
        else:
            # Looping over sigma's
            for zz, perc_zz in enumerate(perc_arr):
                perc_lims  = [50 - (perc_zz/2.), 50 + (perc_zz/2.)]
                mark_lower = np.nanpercentile(data_arr, perc_lims[0], axis=0)
                mark_upper = np.nanpercentile(data_arr, perc_lims[1], axis=0)
                mark_lims  = np.column_stack((mark_lower, mark_upper))[0]
                # Saving to dictionary
                sigma_dict[zz] = mark_lims
    # Using standard deviation to estimate errors
    if (type_sigma == 'std'):
        # Number of bins in `perc_arr`
        nperc = len(perc_arr)
        # Looping over St. Dev. ranges
        for zz in range(nperc):
            mark_lower = mark_mean - (mark_std * (zz + 1))
            mark_upper = mark_mean + (mark_std * (zz + 1))
            # Populating lower and upper limits
            sigma_dict[zz] = np.column_stack((mark_lower, mark_upper)).T
    #
    # Fixing values for when it's a 1D array
    if (not list_opt) and (not ax_opt):
        for zz in range(len(sigma_dict.keys())):
            sigma_dict[zz] = sigma_dict[zz].flatten()
    #
    # Deciding which objects to return
    if return_mean_std:
        return_obj = sigma_dict, mark_mean, mark_std
    else:
        return_obj = sigma_dict

    return return_obj

## Main framework for `Stats_one_arr` and `Stats_two_arr`
def Stats_one_arr(x, y, base=1., arr_len=0, arr_digit='n',
    statfunc=np.nanmean, bin_statval='average',
    return_perc=False, failval=np.nan, type_sigma='std', return_dict=False):
    """
    Calculates statistics for 2 arrays

    Parameters
    ----------
    x, y : array_like, shape(N,)
        Sets of elements for the 1st and 2nd observable

    base : float, optional
        Bin width in units of `x`. This variable is set to 1. by default.

    arr_len : int, optional
        Minimum number of elements in each bin of `x`

    arr_digit : {'n', 'y', 'o'} str, optional
        Option for which elements to return.

        Options:
            - 'n' : Returns `x_stat`, `y_stat`, `y_std`, `y_std_err`
            - 'y' : Returns `x_stat`, `y_stat`, `y_std`, `y_std_err`, `x_bins_data`, `y_bins_data`
            - 'o' : Returns `x_bins_data`, `y_bins_data`

    statfunc : {`numpy.nanmean`, `numpy.nanmedian`} statistical func, optional
        Numerical function used to calculate on bins of data.
        By default, this variable is set to `numpy.nanmean`

    bin_statval : {'average', 'left', 'right', 'center'} str, optional
        Option for where to put the bin values of `x` and `y`.
        By default, this variable is set to `average`, which means
        that the values are those of the averages of the bins in `x` and
        `y`.

    return_perc : `bool`, optional
        If true, it also returns the `percentiles` of the data.
        Last item in the return list.
        This variable is set to False by default.

    failval : `int`, `float`, `NoneType`, or `NaN`, optional
        This is the value used when no data is available for the bin.
        This is set to `numpy.nan` by default

    type_sigma : {'perc', 'std'} string, optional (default = 'std')
        Option for calculating either `percentiles` or `standard deviations`.
        This variable is set to `std` by default.

        Options:
            - ``perc`` : calculates percentiles
            - ``std`` : uses standard deviations as 1-, 2-, and 3-sigmas

    return_dict : `bool`, optional
        If `True`, the function returns a `dict` with the binned statistics
        and more. This variable is set to `False` by default.

    Returns
    ----------
    x_stat, y_stat : array_like
        Binned array of elements from `x`

    y_std : array_like
        Standard deviation of the binned array in `x`

    y_std_err : array_like
        Error in the `statfunc` of `y`

    x_bins_data : array_like, optional
        Elements of `x` in each bin with spacing of `base`.
        Only returned if `arr_digit` == 'y' or 'o'

    y_bins_data : array_like, optional
        Elements of `y` in each bin with spacing of `base`.
        Only returned if `arr_digit` == 'y' or 'o'

    perc_lims : array_like, shape(N,3)
        Percentiles in each bin of `x_stat`.
        Only returned if `arr_digit` == 'y' or 'o'
    """
    file_msg = fd.Program_Msg(__file__)
    ## Verifying input values
    # `arr_digit`
    if not ((arr_digit == 'y') or (arr_digit == 'n') or (arr_digit == 'o')):
        msg = '{0} `arr_digit` ({1}) is not a valid input. Exiting'.format(
            file_msg, arr_digit)
        raise LSSUtils_Error(msg)
    # Array dimensions
    if not ((len(x) > 0) and (len(y) > 0)):
        msg = '{0} The arrays `x` and `y` must have at least one value'
        msg = msg.format(file_msg)
        raise LSSUtils_Error(msg)
    if not ((np.asarray(x).ndim == 1) and (np.asarray(y).ndim == 1)):
        msg = '{0} The arrays `x` and `y` must have dimension of `1`'
        msg = msg.format(file_msg)
        raise LSSUtils_Error(msg)
    # `arr_len`
    if not (arr_len >= 0):
        msg = '{0} `arr_len` ({1}) must be greater or equal than zero!'.format(
            file_msg, arr_len)
        raise LSSUtils_Error(msg)
    # `bin_statval`
    if not (bin_statval in ['average', 'left', 'right', 'center']):
        msg = '{0} `bin_statval` ({1}) is not a valid input! Exiting'.format(
            file_msg, bin_statval)
        raise LSSUtils_Error(msg)
    ##
    ## Converting arrays to numpy arrays
    x       = np.asarray(x)
    y       = np.asarray(y)
    arr_len = int(arr_len - 1.) if arr_len != 0 else int(arr_len)
    ##
    ## Statistics calculations
    x_bins_edges = Bins_array_create(x, base=base)
    x_digits     = np.digitize(x, x_bins_edges) - 1
    # Tuple for `x_bins`
    x_bins = Bins_array_create(x, base=base, return_tuple=True)
    nbins  = len(x_bins)
    ##
    ## Determining which bins to use
    ## These are the bins that meet the criteria of `arr_len`
    x_digits_bins = np.array([int(ii) for ii in range(nbins) if
        len(x_digits[x_digits == ii]) > arr_len])
    # Running only if there is data
    if (len(x_digits_bins) > 0):
        # Elements in each bin
        # `x` values
        x_bins_data = np.array([x[x_digits == ii] for ii in x_digits_bins])
        # `y` values
        y_bins_data = np.array([y[x_digits == ii] for ii in x_digits_bins])
        # Bins that meet the `arr_len` criteria
        x_bins_criteria = x_bins[x_digits_bins]
        ## Selecting data in bins
        if (bin_statval == 'left'):
            x_stat = x_bins_criteria.T[0]
        elif (bin_statval == 'right'):
            x_stat = x_bins_criteria.T[1]
        elif (bin_statval == 'center'):
            x_stat = np.mean(x_bins_criteria, axis=1)
        elif (bin_statval == 'average'):
            x_stat = np.array([np.nanmean(ii) if (len(ii) > arr_len)
                        else failval for ii in x_bins_data])
        # Determining the values in `y`
        # `stat_function`
        y_stat = np.array([statfunc(ii) for ii in y_bins_data])
        # Standard Deviation
        y_std  = np.array([np.nanstd(ii) for ii in y_bins_data])
        # Error in the mean/median
        y_std_err = np.array([np.nanstd(ii)/math.sqrt(len(ii)) for ii in
            y_bins_data])
    else:
        x_bins_data     = np.array([np.nan])
        y_bins_data     = np.array([np.nan])
        x_bins_criteria = np.array([np.nan])
        x_stat          = np.array([np.nan])
        y_stat          = np.array([np.nan])
        y_std           = np.array([np.nan])
        y_std_err       = np.array([np.nan])
    ##
    ## Correcting error inf `statfunc` == `numpy.nanmedian`
    if statfunc == np.nanmedian:
        y_std_err *= 1.253
    ##
    ## Returning percentiles
    perc_arr_lims = sigma_calcs(y_bins_data, type_sigma=type_sigma)
    ##
    # Building dictionary
    xy_dict                  = {}
    xy_dict['x_stat'       ] = x_stat
    xy_dict['y_stat'       ] = y_stat
    xy_dict['y_std'        ] = y_std
    xy_dict['y_std_err'    ] = y_std_err
    xy_dict['perc_arr_lims'] = perc_arr_lims
    xy_dict['x_bins_data'  ] = x_bins_data
    xy_dict['y_bins_data'  ] = y_bins_data
    # Determine entries to return
    if (arr_digit == 'n'):
        return_val = [  'x_stat', 'y_stat', 'y_std', 'y_std_err']
    if (arr_digit == 'y'):
        return_val = [  'x_stat', 'y_stat', 'y_std', 'y_std_err',
                        'x_bins_data', 'y_bins_data']
    if (arr_digit == 'o'):
        return_val = [  'x_bins_data', 'y_bins_data']
    # Aggregating percentage/std info if necessary
    if return_perc:
        return_val.append('perc_arr_lims')
    # Determining object to return
    if return_dict:
        # Initiating dictionary with output values
        return_obj = {}
        # Populating output object
        for key_val in return_val:
            return_obj[key_val] = xy_dict[key_val]
    else:
        # Initiating output object
        return_obj = [[] for x in range(len(return_val))]
        # Populating output object
        for jj, key_val in enumerate(return_val):
            return_obj[jj] = xy_dict[key_val]

    return return_obj

## Function that computes statistics on variables `x` and `y`
def Stats_one_arr_mod(x, y, base=1., arr_len=0, statfunc=np.nanmean,
    bin_statval='average', failval=np.nan, type_sigma='std',
    type_shade='std'):
    """
    Computes a set of statistic on two variables `x` and `y`. The function
    will compute the `statfunc` statistics and errors.

    Parameters
    ------------
    x, y : `numpy.ndarray`, `list`, shape (N,)
        Sets of elements for the 1st and 2nd observables.

    base : `float`, optional
        Bin width in units of `x`. This variable is set to ``1.`` by default.

    arr_len : `int`, optional
        Minimum number of elements in each bin of `x`. For example,
        if ``arr_len == 10``, a statistics is computed only if there
        are a minimum of ``10`` elements in a specified bin of `x`.
        This variable is set ``0`` by default.

    stat_func : {`numpy.nanmean`, `numpy.nanmedian`} statistical function, optional
        Numerical function used to calculate on bins of data. By default,
        this variable is set to `numpy.nanmean`.

    bin_statval : {'average', 'left', 'right', 'center'} `str`, optional
        Option for where to put the bin value of `x` and `y`.
        This variable is set to `average` by default.

        Options:
            - ``average`` : The function returns the mean of `x`.
            - ``left`` : The function returns the points to the `left` edge of the bin of `x` and `statfunc` of `y`.
            - ``right`` : The function returns the points to the `right` edge of the bin of `x` and `statfunc` of `y`.
            - ``center`` : The function returns the point at the `center` of the bin and `statfunc` of `y`.

    failval : `int`, `float`, `NoneType`, or `NaN`, optional
        This is the value used when no data is available for the bin. This
        This variable is set to `numpy.nan` by default.

    type_sigma : {`std``, ``med_abs``} `str`, optional
        Option for calculating either `percentiles`, `standard deviation`,
        or ``error in the median``. This variable is set to ``std``
        by default.

        Options : 
            - ``std`` : Computes the Standard Deviation of bins in `y`
            - ``med_abs`` : Computes the Absolute median absolute deviation of bins in `y`

    type_shade : {``std``, ``perc``}, optional
        Option for which type of statistic to use when determining the
        ranges of errors. This variable is set to ``perc`` by default.

        Options:
            - ``std`` : Computes the 1-, 2-, and 3-St. Dev from the mean/median
            - ``perc`` : Computers the 68th, 95th, and 99.7th percentiles about the median

    Returns
    ------------
    stats_dict : `dict`
        Python dictionary with the necessary statistics for `x` and `y`
        based on the input arguments.
    """
    file_msg = fd.Program_Msg(__file__)
    ## Verifying input values
    # Array dimensions
    if not ((len(x) > 0) and (len(y) > 0)):
        msg = '{0} The arrays `x` ({1}) and `y` ({2}) must have at least one '
        msg += 'value in the array!'
        msg = msg.format(file_msg, len(x), len(y))
        raise LSSUtils_Error(msg)
    if not ((np.asarray(x).ndim == 1) and (np.asarray(y).ndim == 1)):
        msg = '{0} `x` ({1}) and `y` ({2}) must have dimensions of `1`!'
        msg = msg.format(file_msg, np.asarray(x).ndim, np.asarray(y).ndim)
        raise LSSUtils_Error(msg)
    # `base` - Type
    base_type_arr = (float, int)
    if not (isinstance(base, base_type_arr)):
        msg = '{0} `base` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(base), base_type_arr)
        raise TypeError(msg)
    # `base` - Value
    if not (base > 0):
        msg = '{0} `base` ({1}) must be larger than `0`!'
        msg = msg.format(file_msg, base)
        raise ValueError(msg)
    # `arr_len` - Type
    arr_len_type_arr = (float, int)
    if not (isinstance(arr_len, arr_len_type_arr)):
        msg = '{0} `arr_len` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(arr_len), arr_len_type_arr)
        raise TypeError(msg)
    else:
        arr_len = int(arr_len)
    # `arr_len` - Value
    if not (arr_len >= 0):
        msg = '{0} `arr_len` ({1}) must be larger than `0`!'
        msg = msg.format(file_msg, arr_len)
        raise ValueError(msg)
    # `bin_statval` - Type
    bin_statval_type_arr = (str)
    if not (isinstance(bin_statval, bin_statval_type_arr)):
        msg = '{0} `bin_statval` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(bin_statval), bin_statval_type_arr)
        raise TypeError(msg)
    # `bin_statval` - Value
    bin_statval_val_arr = ['average', 'left', 'right', 'center']
    if not (bin_statval in bin_statval_val_arr):
        msg = '{0} `bin_statval` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, bin_statval, bin_statval_val_arr)
        raise ValueError(msg)
    # `type_sigma` - Type
    type_sigma_type_arr = (str)
    if not (isinstance(type_sigma, type_sigma_type_arr)):
        msg = '{0} `type_sigma` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(type_sigma), type_sigma_type_arr)
        raise TypeError(msg)
    # `type_sigma` - Value
    type_sigma_val_arr = ['std', 'med_abs']
    if not (type_sigma in type_sigma_val_arr):
        msg = '{0} `type_sigma` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, type_sigma, type_sigma_val_arr)
        raise ValueError(msg)
    # `type_shade` - Type
    type_shade_type_arr = (str)
    if not (isinstance(type_shade, type_shade_type_arr)):
        msg = '{0} `type_shade` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(type_shade), type_shade_type_arr)
        raise TypeError(msg)
    # `type_shade` - Value
    type_shade_val_arr = ['std', 'perc']
    if not (type_shade in type_shade_val_arr):
        msg = '{0} `type_shade` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, type_shade, type_shade_val_arr)
        raise ValueError(msg)
    ##
    ## Converting to desired types
    base    = float(base)
    arr_len = int(arr_len)
    ## Converting arrays to `numpy` arrays
    x = np.asarray(x)
    y = np.asarray(y)
    # Fixing `arr_len`
    arr_len = int(arr_len - 1.) if arr_len !=0 else int(arr_len)
    #
    # Statistics calculations
    x_bins_edges = Bins_array_create(x, base=base)
    x_digits     = np.digitize(x, x_bins_edges) - 1
    # Tuple for `x_bins`
    x_bins       = Bins_array_create(x, base=base, return_tuple=True)
    nbins        = len(x_bins)
    #
    # Determining which bins to use. These are the bins that meet the
    # criteria of `arr_len`
    x_digits_bins = np.asarray([int(ii) for ii in range(nbins) if
        (len(x_digits[x_digits == ii]) > arr_len)])
    # Computing statistics if there are the necessary number of bins
    if (len(x_digits_bins) > 0):
        # Extracting `x` values
        x_mod = np.asarray([x[x_digits == ii] for ii in x_digits_bins])
        # Extracting `y` values
        y_mod = np.asarray([y[x_digits == ii] for ii in x_digits_bins])
        # Bins that meet the `arr_len` criteria
        x_bins_criteria = x_bins[x_digits_bins]
        # Statics on `x`
        if (bin_statval == 'left'):
            x_stat = x_bins_criteria.T[0]
        elif (bin_statval == 'right'):
            x_stat = x_bins_criteria.T[1]
        elif (bin_statval == 'center'):
            x_stat = np.nanmean(x_bins_criteria, axis=1)
        elif (bin_statval == 'average'):
            x_stat = np.asarray([np.nanmean(xx) for xx in x_mod])
        ## Statistics on `y`
        # Main function on `y`
        y_stat = np.asarray([statfunc(xx) for xx in y_mod])
        # Percentiles
        perc_arr_lims = sigma_calcs(y_mod, type_sigma=type_shade)
        # Error in `y`
        if (type_sigma == 'std'):
            y_err = np.asarray([np.nanstd(xx) for xx in y_mod])
            if (statfunc == np.nanmedian):
                y_err *= 1.253
        elif (type_sigma == 'med_abs'):
            y_err = np.asarray([sstats.median_absolute_deviation(xx)
                for xx in y_mod])
    else:
        x_stat        = np.array([np.nan])
        y_stat        = np.array([np.nan])
        y_err         = np.array([np.nan])
        x_mod         = np.array([np.nan])
        y_mod         = np.array([np.nan])
        perc_arr_lims = dict(zip([0,1,2], [np.array([np.nan]),
                            np.array([np.nan]), np.array([np.nan])]))
    #
    # Saving elements to dictionary
    return_obj = {}
    return_obj['x_stat'] = x_stat
    return_obj['y_stat'] = y_stat
    return_obj['y_err' ] = y_err
    return_obj['x_mod' ] = x_mod
    return_obj['y_mod' ] = y_mod
    return_obj['perc_arr_lims'] = perc_arr_lims

    return return_obj
