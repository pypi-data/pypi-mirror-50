#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Victor Calderon
# Created      : 2018-05-03
# Last Modified: 2019-08-14
from __future__ import absolute_import, division, print_function
__author__     = ['Victor Calderon']
__copyright__  = ["Copyright 2018 Victor Calderon"]
__email__      = ['victor.calderon@vanderbilt.edu']
__maintainer__ = ['Victor Calderon']
__all__        = [  "flip_angles",
                    "Ang_Distance",
                    "Coord_Transformation",
                    "cartesian_translation",
                    "sph_to_cartesian",
                    "coordinate_transformation",
                    "cart_to_sph_coords",
                    "cart_rotation_matrices",
                    "rotation_matrices_3D",
                    "cartesian_rotation"]
"""
Set of geometrical definitions for translations, coordinate transformations,
etc.
"""

## Import modules
import numpy as np
import pandas as pd
from   cosmo_utils.utils import file_utils as fd
from   cosmo_utils.custom_exceptions import LSSUtils_Error

## Functions

# Restricting angles to be between 0 and 360
def flip_angles(ang, unit='deg'):
    """
    Ensures that an angle is always between 0 and 360 degrees.

    Parameters
    ----------
    ang : float, int, `numpy.ndarray`
        Angle in units of degrees.

    unit : {'deg', 'rad'} str, optional
        Unit of the angle. This variable is set to 'deg' by default.
        If 'rad', the output will be in units of radians.

    Returns
    ----------
    ang_out : float
        Convertions of `ang`, ranging from 0 to 360 degrees.

    Raises
    ----------
    LSSUtils_Error : Exception
        This error gets raised when `ang` is not a digit or a number.

    Examples
    ----------
    >>> flip_angles(-50, unit='deg')
    310.0

    >>> flip_angles(110, unit='deg')
    110.0
    """
    file_msg = fd.Program_Msg(__file__)
    # Checking type of `ang`
    valid_types = (float, int, list, np.ndarray)
    if not (isinstance(ang, valid_types)):
        msg = '{0} `ang` ({1}) is not a number! Exiting!'.format(
            file_msg, ang)
        raise LSSUtils_Error(msg)
    # Checking `unit`
    if not (unit.lower() in ['deg', 'rad']):
        msg = '{0} `unit` ({1}) is not a valid option! Exiting!'.format(
            file_msg, unit)
        raise LSSUtils_Error(msg)
    ##
    ## Converting angle
    if isinstance(ang, float) or isinstance(ang, int):
        ang = float(ang)
        # Converting from radians to degrees, if applicable
        if unit == 'rad':
            ang_converted = np.degrees(ang)
        elif unit == 'deg':
            ang_converted = ang
        # Checking the range of `ang`
        if ang_converted < 0:
            ang_converted += 360
        # Converting back to radians, if applicable
        if unit == 'rad':
            ang_final = np.radians(ang_converted)
        elif unit == 'deg':
            ang_final = float(ang_converted)
    else:
        try:
            ang = np.asarray(ang)
            # Converting to degrees, if applicable
            if unit == 'rad':
                ang_converted = np.degrees(ang)
            elif unit == 'deg':
                ang_converted = ang
            # Checking the range of `ang`
            ang_converted = np.asarray([xx if xx > 0 else xx+360 for xx in
                ang_converted])
            # Converting back to radians, if applicable
            if unit == 'rad':
                ang_final = np.radians(ang_converted)
            elif unit == 'deg':
                ang_final = ang_converted
            # Converting to float
            ang_final = ang_final.astype(float)
        except:
            msg = '{0} `ang` could not be converted!'.format(file_msg)
            raise LSSUtils_Error(msg)

    return ang_final

## Calculates the Angular distance between 2 points
def Ang_Distance(ra1, ra2, dec1, dec2, unit='deg', method='haversine'):
    """
    Calculates angular separation between two sets of points with given
    right ascensions and declinations.

    Taken from: https://en.wikipedia.org/wiki/Haversine_formula

    Parameters
    -----------
    ra1, ra2 : float
        Right Ascension of the 1st and 2nd points. Units in `degrees`
        by default.

    dec1, dec2 : float
        Declination of the 1st and 2nd points. Units in `degrees` by default.

    unit : {'dec','rad'} str, optional
        Unit of `ra1`, `ra2`, `dec1`, and `dec2`.
        This will also determine the final unit that outputs this function.

    method : {'haversine', 'astropy'} str, optional
        Method to use in order to calculate angular separation.
        This variable is to by default to the `haversine` method.
        If `astropy`, it will use the astropy framework to determine the
        angular separation.

    Returns
    -----------
    ang_sep : float
        Angular separation between 1st and 2nd point.
        In units of `degrees`.

    Notes
    -----------
    A = 90. - `dec2`
    B = 90. - `dec1`
    D = `ra1` - `ra2`
    c = Angle between two points
    """
    file_msg = fd.Program_Msg(__file__)
    ## Checking input arguments
    # Valid options
    units_valid   = ['deg', 'rad']
    methods_valid = ['haversine', 'astropy']
    # Units
    if not (unit in units_valid):
        msg = '{0} `unit` ({1}) is not a valid argument'.format(
            file_msg, unit)
        raise LSSUtils_Error(msg)
    # Method
    if not (method in methods_valid):
        msg = '{0} `method` ({1}) is not a valid argument'.format(
            file_msg, method)
        raise LSSUtils_Error(msg)
    ##
    ## Flipping angles
    ra1 = flip_angles(ra1, unit=unit, )
    ra2 = flip_angles(ra2, unit=unit)
    ##
    ## Haversine Method
    if method == 'haversine':
        A = np.radians(90. - dec1)
        B = np.radians(90. - dec2)
        D = np.radians(ra1 - ra2 )
        # Distance
        ang_sep  = (np.sin((A - B) * .5))**2.
        ang_sep += np.sin(A) * np.sin(B) * (np.sin(D * .5))**2.
        ang_sep  = np.degrees(2 * np.arcsin(ang_sep**0.5))
    ##
    ## Astropy Method
    if method == 'astropy':
        # Imports
        from astropy.coordinates import SkyCoord
        from astropy import units as u
        # Converting to `units`
        if unit == 'deg':
            unit_opt = u.degree
        elif unit == 'rad':
            unit_opt = u.radians
        # Calculations
        p1 = SkyCoord(ra=ra1, dec=dec1, unit=(unit_opt, unit_opt))
        p2 = SkyCoord(ra=ra2, dec=dec2, unit=(unit_opt, unit_opt))
        # Angular Separation
        ang_sep = p1.separation(p2)
        # Converting to final units
        if unit == 'deg':
            ang_sep = ang_sep.degree
        elif unit == 'rad':
            ang_sep = ang_sep.radians

    return ang_sep

## Coordinate Transformation function
def Coord_Transformation(ra, dec, dist, ra_cen, dec_cen, dist_cen,
    trans_opt=4, return_dict=False, unit='deg'):
    """
    Transforms spherical coordinates (ra, dec, dist) into Cartesian
    coordinates.

    Parameters
    -----------
    ra, dec, dist : array_like, shape (N,)
        Arrays of Right Ascension, declination, and distance.
        Units are ['degrees', 'degrees', 'distance_units']

    ra_cen, dec_cen, dist_cen : float, int
        Right Ascension, declination, and distance for the center of
        the coordinates. These correspond to where the coordinates
        `ra`, `dec`, and `dist` will be centered.

    trans_opt : {1, 2, 3, 4} int, optional
        Option for Cartesian translation/transformation for elements.
        This variable ist set to `4` by default.

        Options:
            - 1 : No translation involved
            - 2 : Translation to the center point.
            - 3 : Translation `and` rotation to the center point.
            - 4 : Translation and 2 rotations about the center point

    return_dict : {True, False}, `bool`, optional
        If `True`, this functions returns 2 dictionaries with `spherical`
        and `Cartesian` coordinates.
        If `False`, it returns a `pandas.DataFrame` with the columns.
        This variable is set to `False` by default.

    unit : {'dec','rad'} str, optional
        Unit of `ra1`, `ra2`, `dec1`, and `dec2`.
        This will also determine the final unit that outputs this function.
        This variable is set to `deg` by default.

    Returns
    -----------
    coord_dict (coord_pd) : python dictionary
        Dictionary with spherical and Cartesian dictionary of elements
        based on `trans_opt` value. This value is returned if
        `return_dict` is set to `True`. If not, a `pandas.DataFrame` is
        return.
    """
    file_msg = fd.Program_Msg(__file__)
    ## Check types of elements
    # Units
    unit_arr = ['deg', 'rad']
    if not (unit in unit_arr):
        '{0} `unit` ({1}) is not a valid input!'.format(
            file_msg, unit)
    # Valid types
    valid_types = (float, int, np.ndarray, list)
    # Right Ascension
    if not (isinstance(ra, valid_types)):
        msg = '{0} `ra` ({1}) is not a valid type!'.format(
            file_msg, type(ra))
        raise LSSUtils_Error(msg)
    # Declination
    if not (isinstance(dec, valid_types)):
        msg = '{0} `dec` ({1}) is not a valid type!'.format(
            file_msg, type(dec))
        raise LSSUtils_Error(msg)
    # Distance
    if not (isinstance(dist, valid_types)):
        msg = '{0} `dist` ({1}) is not a valid type!'.format(
            file_msg, type(dist))
        raise LSSUtils_Error(msg)
    # trans_opt
    if not (trans_opt in list(range(1, 5))):
        msg = '{0} `trans_opt` ({1}) is not within valid range!'.format(
            file_msg, trans_opt)
        raise LSSUtils_Error(msg)
    ##
    ## Centre's RA, DEC, DIST
    # Right Ascension
    if (isinstance(ra_cen, float)):
        ra_cen = flip_angles(ra_cen)
    else:
        msg = '{0} `ra_cen` ({1}) is not a float!'.format(
            file_msg, type(ra_cen))
        raise LSSUtils_Error(msg)
    # Declination
    if (isinstance(dec_cen, float)):
        dec_cen = flip_angles(dec_cen)
    else:
        msg = '{0} `dec_cen` ({1}) is not a float!'.format(
            file_msg, type(dec_cen))
        raise LSSUtils_Error(msg)
    # Distance
    if (isinstance(dist_cen, float)):
        dist_cen = float(dist_cen)
    else:
        msg = '{0} `dist_cen` ({1}) is not a float!'.format(
            file_msg, type(dist_cen))
        raise LSSUtils_Error(msg)
    ##
    ## Check type of elements
    # Right Ascension
    if (isinstance(ra, float) or isinstance(ra, int)):
        ra = np.array([ra])
    else:
        ra = np.array(ra)
    # Declination
    if (isinstance(dec, float) or isinstance(dec, int)):
        dec = np.array([dec])
    else:
        dec = np.array(dec)
    # Distance
    if (isinstance(dist, float) or isinstance(dist, int)):
        dist = np.array([dist])
    else:
        dist = np.array(dist)
    ##
    ## Converting to desired units
    if unit == 'rad':
        # Right Ascension
        ra_rad     = ra
        ra_cen_deg = np.degrees(ra_cen)
        ra_cen_rad = ra_cen
        # Declination
        dec_rad     = dec
        dec_cen_deg = np.degrees(dec_cen)
        dec_cen_rad = dec_cen
    elif unit == 'deg':
        ra_rad     = np.radians(ra)
        ra_cen_deg = ra_cen
        ra_cen_rad = np.radians(ra_cen)
        # Declination
        dec_rad     = np.radians(dec)
        dec_cen_deg = dec_cen
        dec_cen_rad = np.radians(dec_cen)
    ##
    ## Initializing pandas DataFrame
    dict_keys  = ['ra', 'dec', 'dist']
    coord_dict = dict(zip(dict_keys, np.vstack([ra, dec, dist])))
    ##
    ## Spherical to Cartesian transformation
    ## 1st transformation
    # Centre
    x_cen = dist_cen * np.cos(ra_cen_rad) * np.cos(dec_cen_rad)
    y_cen = dist_cen * np.sin(ra_cen_rad) * np.cos(dec_cen_rad)
    z_cen = dist_cen * np.sin(dec_cen_rad)
    # All galaxies
    x = dist * np.cos(ra_rad) * np.cos(dec_rad)
    y = dist * np.sin(ra_rad) * np.cos(dec_rad)
    z = dist * np.sin(dec_rad)
    ##
    ## Rotations about z- and x-axis by `tau` and `Omega`
    ## Rotating the points, not the axes
    x1 = x - x_cen
    y1 = y - y_cen
    z1 = z - z_cen
    # Angles
    omega = np.radians(90. - ra_cen_deg )
    tau   = np.radians(90. - dec_cen_deg)
    # Rotations about z-axis by `omega`
    x2 = x1 * np.cos(omega) - y1 * np.sin(omega)
    y2 = x1 * np.sin(omega) + y1 * np.cos(omega)
    z2 = z1.copy()
    # Rotations about X-axis by `tau`
    x3 = x2.copy()
    y3 = y2 * np.cos(tau) - z2 * np.sin(tau)
    z3 = z2 * np.sin(tau) + z2 * np.cos(tau)
    ##
    ## Defining which variables to return
    # No Translation
    if trans_opt == 1:
        coord_dict['x'] = x
        coord_dict['y'] = y
        coord_dict['z'] = z
    # Translation
    if trans_opt == 2:
        coord_dict['x'] = x1
        coord_dict['y'] = y1
        coord_dict['z'] = z1
    # Translation + Rotation
    if trans_opt == 3:
        coord_dict['x'] = x2
        coord_dict['y'] = y2
        coord_dict['z'] = z2
    # Translation + 2 Rotation (centered about the centre)
    if trans_opt == 4:
        coord_dict['x'] = x3
        coord_dict['y'] = y3
        coord_dict['z'] = z3
    ##
    ## Checking what object to return, i.e. DataFrame or python dictionary
    if return_dict:
        return coord_dict
    else:
        coord_pd = pd.DataFrame(coord_dict)
        return coord_pd

## Cartesian translation function
def cartesian_translation(cart_obj, cart_origin_obj):
    """
    Function that translates a set of points given a new `origin`

    Parameters
    -----------
    cart_obj : `pandas.DataFrame` or `numpy.ndarray`
        Object containing the set of Cartesian Coordinates in the order
        of ['x', 'y', 'z'].

    cart_origin_obj : `pandas.DataFrame` or `numpy.ndarray`
        Object containing the Cartesian coordinates of the new `origin`
        for `cart_obj`

    Returns
    ----------
    cart_tr_obj : `pandas.DataFrame` or `numpy.ndarray`
        Object containing the `translated` Cartesian coordinates of `cart_obj`.
    """
    file_msg = fd.Program_Msg(__file__)
    # Cartesian names array
    cart_names = ['x', 'y', 'z']
    ## Checking input parameters
    #
    # Checking type of `cart_obj` and converting to DataFrame if needed.
    cart_obj_type_arr = (np.ndarray, list, pd.DataFrame, pd.Series)
    if not (isinstance(cart_obj, cart_obj_type_arr)):
        msg = '{0} `cart_obj` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(cart_obj), cart_obj_type_arr)
        raise TypeError(msg)
    else:
        if (isinstance(cart_obj, (np.ndarray))):
            cart_pd = pd.DataFrame(dict(zip(cart_names, cart_obj.T)))
        elif (isinstance(cart_obj, (list))):
            cart_pd = pd.DataFrame(dict(zip(cart_names, np.asarray(cart_obj).T)))
        elif (isinstance(cart_obj, (pd.DataFrame))):
            cart_pd = pd.DataFrame(dict(zip(cart_names, cart_obj.values.T)))
    #
    # Checking type of `cart_obj_cen`
    cart_origin_obj_type_arr = (np.ndarray, list, pd.DataFrame, pd.Series)
    if not (isinstance(cart_origin_obj, cart_origin_obj_type_arr)):
        msg = '{0} `cart_origin_obj` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(cart_origin_obj),
            cart_origin_obj_type_arr)
        raise TypeError(msg)
    else:
        if isinstance(cart_origin_obj, (list)):
            cart_origin_obj = np.asarray(cart_origin_obj).flatten()
        elif isinstance(cart_origin_obj, (pd.DataFrame, pd.Series)):
            cart_origin_obj = pd.Series(dict(zip(cart_names,
                cart_origin_obj.values)))
    #
    # Translating Cartesian coordinates
    # This translation puts the `cart_origin_obj` at the origin of
    # `cart_pd`
    cart_tr_obj = (cart_pd - cart_origin_obj)
    #
    # Returning object with designated type
    if not (isinstance(cart_pd, (pd.Series, pd.DataFrame))):
        cart_tr_obj = cart_tr_obj.values

    return cart_tr_obj

## Spherical to Cartesian coordinates
def sph_to_cartesian(sph_obj, return_type='df', unit='deg'):
    """
    Function that converts spherical coordinates into Cartesian coordinates.

    Parameters
    -----------
    sph_obj : `numpy.ndarray` or `pandas.DataFrame`
        Object containing the positions of points in spherical coordinates.
        The object must include the `ra`, `dec`, and `distance` to
        each object to the observer.

    return_type : {'df', 'dict'} `str`, optional
        Option for the type of output file to return. This variable is
        set to ``df`` by default.

        Options :
            - ``df`` : `pandas.DataFrame` with transformed coordinates.
            - ``dict`` : Dictionary with transformed coordinates.

    unit : {``deg``, ``rad``} `str`, optional
        Unit of angles provided. This will also determine the final
        unit that outputs this function. This variable is set to `deg`
        by default.

    Returns
    ----------
    cart_obj : `dict` or `pandas.DataFrame`
        Object containing the spherical and Cartesian coordinates of the
        elements from `sph_obj`. 
    """
    file_msg       = fd.Program_Msg(__file__)
    cart_names_arr = ['x', 'y', 'z']
    sph_names_arr  = ['ra', 'dec', 'dist']
    ##
    ## Checking input parameters
    # `sph_obj` - Type
    sph_obj_type_arr = (list, np.ndarray, pd.DataFrame, pd.Series)
    if not (isinstance(sph_obj, sph_obj_type_arr)):
        msg = '{0} `sph_obj` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(sph_obj), sph_obj_type_arr)
        raise TypeError(msg)
    else:
        if isinstance(sph_obj, (list, np.ndarray)):
            sph_pd = pd.DataFrame(dict(zip(sph_names_arr,
                np.asarray(sph_obj).T)))
        elif isinstance(sph_obj, (pd.DataFrame, pd.Series)):
            try:
                sph_pd = pd.DataFrame(dict(zip(sph_names_arr,
                    sph_obj.values.T)))
            except:
                sph_pd = pd.Series(dict(zip(sph_names_arr,
                    sph_obj.values.T)))
    # `unit` - Type
    unit_type_arr = (str)
    if not (isinstance(unit, unit_type_arr)):
        msg = '{0} `unit` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(unit), unit_type_arr)
        raise TypeError(msg)
    # `unit` - Value
    unit_val_arr = ['deg', 'rad']
    if not (unit in unit_val_arr):
        msg = '{0} `unit` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, unit, unit_val_arr)
        raise ValueError(msg)
    ##
    ## Converting spherical to Cartesian coordinates
    if (unit == 'rad'):
        ra_rad  = sph_pd['ra']
        dec_rad = sph_pd['dec']
    elif (unit == 'deg'):
        ra_rad  = np.radians(sph_pd['ra'])
        dec_rad = np.radians(sph_pd['dec'])
    # Distance array
    dist_arr = sph_pd['dist']
    #
    # Converting to Cartesian
    x = dist_arr * np.cos(ra_rad) * np.cos(dec_rad)
    y = dist_arr * np.sin(ra_rad) * np.cos(dec_rad)
    z = dist_arr * np.sin(dec_rad)
    #
    # Constructing output object
    if (return_type == 'df'):
        if isinstance(x, (list, np.ndarray)):
            cart_obj = pd.DataFrame(dict(zip(cart_names_arr,
                np.column_stack(np.asarray([x, y, z]).T))))
        elif isinstance(x, pd.DataFrame):
            cart_obj = pd.DataFrame(dict(zip(cart_names_arr,
                np.vstack(([x.values, y.values, z.values])))))
        else:
            cart_obj = pd.Series(dict(zip(cart_names_arr,
                [x, y, z])))
    else:
        cart_obj = {}
        cart_obj['x'] = x
        cart_obj['y'] = y
        cart_obj['z'] = z

    return cart_obj

## Coordinate Transformation - Spherical to Cartesian
def coordinate_transformation(sph_obj, sph_cen_obj, translation_first=False,
    trans_opt=2, return_type='df', unit='deg'):
    """
    Transforms spherical coordinates (ra, dec, dist) into Cartesian
    coordinates.

    Parameters:
    -------------
    sph_obj : `numpy.ndarray` or `pandas.DataFrame`
        Object containing the positions of points in spherical coordinates.
        The object must include the `ra`, `dec`, and `distance` to
        each object to the observer.

    sph_cen_obj : `numpy.ndarray` or `pandas.DataFrame`
        Object containing the position of the `origin` or `center` of
        the points. It contains the `ra`, `cen`, and `dist` to main
        object. This variable is used when translating the set of points.

    translation_first : `bool`, optional    
        If `True`, the new origin of the Cartesian coordinates is set
        to `sph_cen_obj`. If `False`, no translation is performed at the
        beginning of the transformation. This variable is set to `False`
        by default.

    trans_opt : {``1``, ``2``}, `int`, optional
        Option for how the Cartesian coordinates are translated and/or
        transformed. This variable is set to ``2`` by default.

        Option :
            - ``0`` : No rotations
            - ``1`` : Rotation along the `z`-axis.
            - ``2`` : Rotation along the `x`-axis.

    return_type : {'df', 'dict'} `str`, optional
        Option for the type of output file to return. This variable is
        set to ``df`` by default.

        Options :
            - ``df`` : `pandas.DataFrame` with transformed coordinates.
            - ``dict`` : Dictionary with transformed coordinates.

    unit : {``deg``, ``rad``} `str`, optional
        Unit of angles provided. This will also determine the final
        unit that outputs this function. This variable is set to `deg`
        by default.

    Returns
    ------------
    coord_obj : `dict` or `pandas.DataFrame`
        Object containing the spherical and Cartesian coordinates of the
        elements from `sph_obj`. 
    """
    file_msg = fd.Program_Msg(__file__)
    cart_names_arr = ['x', 'y', 'z']
    sph_names_arr  = ['ra', 'dec', 'dist']
    cart_rot_dict  = dict(zip([1, 2], ['z', 'zx']))
    ##
    ## Checking input parameters
    # `sph_obj` - Type
    sph_obj_type_arr = (list, np.ndarray, pd.DataFrame, pd.Series)
    if not (isinstance(sph_obj, sph_obj_type_arr)):
        msg = '{0} `sph_obj` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(sph_obj), sph_obj_type_arr)
        raise TypeError(msg)
    else:
        if isinstance(sph_obj, (list, np.ndarray)):
            sph_pd = pd.DataFrame(dict(zip(sph_names_arr,
                np.asarray(sph_obj).T)))
        elif isinstance(sph_obj, (pd.DataFrame, pd.Series)):
            try:
                sph_pd = pd.DataFrame(dict(zip(sph_names_arr,
                    sph_obj.values.T)))
            except:
                sph_pd = pd.Series(dict(zip(sph_names_arr,
                    sph_obj.values.T)))
    # `sph_cen_obj` - Type
    sph_cen_obj_type_arr = (list, np.ndarray, pd.DataFrame, pd.Series)
    if not (isinstance(sph_cen_obj, sph_cen_obj_type_arr)):
        msg = '{0} `sph_cen_obj` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(sph_cen_obj), sph_cen_obj_type_arr)
        raise TypeError(msg)
    else:
        if isinstance(sph_cen_obj, (list, np.ndarray)):
            sph_cen_pd = pd.Series(dict(zip(sph_names_arr,
                np.asarray(sph_cen_obj).T)))
        elif isinstance(sph_cen_obj, (pd.DataFrame, pd.Series)):
            sph_cen_pd = pd.Series(dict(zip(sph_names_arr,
                sph_cen_obj.values.T)))
    # `translation_first` - Type
    translation_first_type_arr = (bool)
    if not (isinstance(translation_first, translation_first_type_arr)):
        msg = '{0} `translation_first` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(translation_first),
            translation_first_type_arr)
        raise TypeError(msg)
    # `trans_opt` - Type
    trans_opt_type_arr = (int, float)
    if not (isinstance(trans_opt, trans_opt_type_arr)):
        msg = '{0} `trans_opt` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(trans_opt), trans_opt_type_arr)
        raise TypeError(msg)
    # `trans_opt` - Value
    trans_opt_val_arr = [0, 1, 2]
    if not (trans_opt in trans_opt_val_arr):
        msg = '{0} `trans_opt` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, trans_opt, trans_opt_val_arr)
        raise ValueError(msg)
    else:
        trans_opt = int(trans_opt)
    # `return_type` - Type
    return_type_type_arr = (str)
    if not (isinstance(return_type, return_type_type_arr)):
        msg = '{0} `return_type` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(return_type), return_type_type_arr)
        raise TypeError(msg)
    # `return_type` - Value
    return_type_val_arr = ['df', 'dict']
    if not (return_type in return_type_val_arr):
        msg = '{0} `return_type` ({2}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, return_type, return_type_val_arr)
        raise ValueError(msg)
    # `unit` - Type
    unit_type_arr = (str)
    if not (isinstance(unit, unit_type_arr)):
        msg = '{0} `unit` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(unit), unit_type_arr)
        raise TypeError(msg)
    # `unit` - Value
    unit_val_arr = ['deg', 'rad']
    if not (unit in unit_val_arr):
        msg = '{0} `unit` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, unit, unit_val_arr)
        raise ValueError(msg)
    ##
    ## Converting spherical to Cartesian coordinates
    cart_pd     = sph_to_cartesian(sph_obj, return_type='df', unit=unit)
    cart_cen_pd = sph_to_cartesian(sph_cen_obj, return_type='df', unit=unit)
    # Translating coordinates, if necessary
    if translation_first:
        cart_pd_mod = cartesian_translation(cart_pd, cart_cen_pd)
    else:
        cart_pd_mod = cart_pd
    # Angles, by which to rotate
    if (unit == 'rad'):
        omega_z = np.radians(90. - np.degrees(cart_cen_pd['ra']))
        tau_x   = np.radians(90. - np.degrees(cart_cen_pd['dec']))
    elif (unit == 'deg'):
        omega_z = np.radians(90. - cart_cen_pd['ra'])
        tau_x   = np.radians(90. - cart_cen_pd['dec'])
    ##
    ## Specifying rotations
    if (trans_opt == 0):
        # No rotations
        cart_rot_pd = cart_pd_mod
    else:
        cart_rot_pd = cartesian_rotation(   cart_pd_mod,
                                            x_ang=tau_x,
                                            z_ang=omega_z,
                                            rot_order=cart_rot_dict[trans_opt],
                                            return_pd=True)
    #
    # Returning object
    if (return_type == 'df'):
        coord_obj = cart_rot_pd
    elif (return_type == 'dict'):
        coord_obj = dict(zip(coord_obj.columns.values,
                        cart_pd_mod.values.T))

    return coord_obj

## Coordinate Transformation - Cartesian to Spherical coordinates
def cart_to_sph_coords(cart_obj, unit='deg', return_type='df'):
    """
    Transforms Cartesian coordinates (x, y, z) into spherical coordinates
    (ra, dec).

    Parameters
    -------------
    cart_obj : `numpy.ndarray`, `pandas.DataFrame`, or `pandas.Series`
        Object containing the set of Cartesian coordinates of the points,
        along with the distance to each object.

    unit : {``deg``, ``rad``}, optional
        Variable that determines the final value of the spherical coordinates.
        This variable is set to ``deg`` by default.

    return_type : {``df``, ``array``}, optional
        Option for the output type of `sph_obj`. This variable is set to
        ``df`` by default.

        Options :
             - ``df`` : Returns a `pandas.DataFrame` with spherical coords.
             - ``array`` : Returns a `numpy.ndarray`.

    Returns
    ----------
    sph_obj : `numpy.ndarray`, `pandas.DataFrame`, or `pandas.Series`
        Spherical coordinates for a given set of points from `cart_obj`
    """
    file_msg       = fd.Program_Msg(__file__)
    cart_names_arr = ['x', 'y', 'z']
    sph_names_arr  = ['ra', 'dec', 'dist']
    ## Checking types of elements
    # `cart_obj` - Type
    cart_obj_type_arr = (list, np.ndarray, pd.DataFrame, pd.Series)
    if not (isinstance(cart_obj, cart_obj_type_arr)):
        msg = '{0} `cart_obj` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(cart_obj), cart_obj_type_arr)
        raise TypeError(msg)
    else:
        if isinstance(cart_obj, (np.ndarray, list)):
            cart_pd = pd.DataFrame(dict(zip(cart_names_arr,
                            cart_obj.T)))
        elif isinstance(cart_obj, (pd.DataFrame, pd.Series)):
            cart_pd = pd.DataFrame(dict(zip(cart_names_arr,
                            cart_obj.values.T)))
    # `unit` - Type
    unit_type_arr = (str)
    if not (isinstance(unit, unit_type_arr)):
        msg = '{0} `unit` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(unit), unit_type_arr)
        raise TypeError(msg)
    # `unit` - Value
    unit_val_arr = ['deg', 'rad']
    if not (unit in unit_val_arr):
        msg = '{0} `unit` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, unit, unit_val_arr)
        raise ValueError(msg)
    # `return_type` - Type
    return_type_type_arr = (str)
    if not (isinstance(return_type, return_type_type_arr)):
        msg = '{0} `return_type` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(return_type), return_type_type_arr)
        raise TypeError(msg)
    # `return_type` - Value
    return_type_val_arr = ['df', 'array']
    if not (return_type in return_type_val_arr):
        msg = '{0} `return_type` ({1}) is not a valid input value ({2})!'
        msg = msg.format(file_msg, return_type, return_type_val_arr)
        raise ValueError(msg)
    ##
    ## Computing distance
    dist_arr = np.sum(cart_pd.values.T**2, axis=0)**0.5
    # Normalizing coordinates
    cart_norm_pd = cart_pd.divide(dist_arr, axis='rows')
    ##
    ## Declination
    dec_arr = 90. - np.degrees(np.arccos(cart_norm_pd['z']))
    ##
    ## Right Ascension
    ra_arr = [[] for x in range(len(cart_norm_pd))]
    for ii, cart_ii in cart_norm_pd.iterrows():
        # Extracting coordinates
        x_ii, y_ii, z_ii = cart_ii.values
        # Determining RA values
        if (x_ii == 0):
            if (y_ii > 0.):
                ra_ii = 90.
            elif (y_ii < 0.):
                ra_ii = -90.
        else:
            ra_ii = np.degrees(np.arctan(y_ii / x_ii))
        #
        # Seeing on which quadrant the point is
        if (x_ii < 0.):
            ra_ii += 180.
        elif ((x_ii >= 0.) and (y_ii < 0.)):
            ra_ii += 360.
        # Saving RA value
        ra_arr[ii] = ra_ii
    #
    # Creating DataFrame with Spherical coordinates
    sph_pd = pd.DataFrame(dict(zip(sph_names_arr, [ra_arr, dec_arr, dist_arr])))
    # Converting to final output
    if (return_type == 'array'):
        sph_obj = sph_pd.values
    elif (return_type == 'df'):
        sph_obj = sph_pd

    return sph_obj

## Set of rotation matrices
def cart_rotation_matrices(angle=45, ax='x'):
    """
    Set of rotation matrices along some axis `ax` by some angle `angle`.

    Parameters
    ------------
    angle : `float`, optional
        Angle, by which to rotate the points. This variable is set to
        ``45`` by default.

    ax : {'x', 'y', 'z'} `str`, optional
        Axis, along which to rotate the points. This variable is set to
        ``x`` by default.
    
    Returns
    ----------
    rot_matr : `numpy.ndarray`
        Rotation matrix for a given axis 'x'
    """
    file_msg = fd.Program_Msg(__file__)
    # Checking type of `angle`
    angle_type_arr = (float, int)
    if not (isinstance(angle, angle_type_arr)):
        msg = '{0} `angle` ({1}) is not a valid input type ({2})'
        msg = msg.format(file_msg, type(angle), angle_type_arr)
        raise TypeError(msg)
    else:
        angle = float(angle)
    # Checking range of `angle`
    if not ((angle >= 0) and (angle <= 360.)):
        msg = '{0} `angle` ({1}) must be between `0` and `360` degrees!'
        msg = msg.format(file_msg, angle)
        raise ValueError(msg)
    # Checking type of `ax`
    ax_type = (str)
    if not (isinstance(ax, ax_type)):
        msg = '{0} `ax` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(ax), ax_type)
        raise TypeError(msg)
    # Checking value of `ax`
    ax_val_arr = ['x', 'y', 'z']
    if not (ax in ax_val_arr):
        msg = '{0} `ax` ({1}) is not a valid input values ({2})!'
        msg = msg.format(file_msg, ax, ax_val_arr)
        raise ValueError(msg)
    ##
    ## Angle to rad
    a_rad = np.radians(angle)
    cos_a = np.cos(a_rad)
    sin_a = np.sin(a_rad)
    ## Defining rotation matrices
    rot_dict = {}
    # x-axis
    rot_dict['r_x'] = np.array([(1, 0, 0),
                                (0, cos_a, -sin_a),
                                (0, sin_a, cos_a)])
    # y-axis
    rot_dict['r_y'] = np.array([(cos_a, 0, sin_a),
                                (0, 1, 0),
                                (-sin_a, 0, cos_a)])
    # z-axis
    rot_dict['r_z'] = np.array([(cos_a, -sin_a, 0),
                                (sin_a, cos_a, 0),
                                (0, 0, 1)])

    return rot_dict['r_{0}'.format(ax)]

## Computes the dot product of a series of rotation matrices
def rotation_matrices_3D(x_ang=0, y_ang=0, z_ang=0, rot_order='xyz'):
    """
    Computes the value of the rotation matrix for 3 different rotations.

    Parameters
    -------------
    x_ang : `float`, optional
        Angle, by which the points are rotated around the `x` axis.
        This variable is set to ``0`` by default.

    y_ang : `float`, optional
        Angle, by which the points are rotated around the `y` axis.
        This variable is set to ``0`` by default.

    z_ang : `float`, optional
        Angle, by which the points are rotated around the `z` axis.
        This variable is set to ``0`` by default.

    rot_order : `str`, optional
        Type of rotation to make. `rot_order` is expected to have THREE
        letters from {'x', 'y', 'z'} element. This variable is set to
        ``xyz`` by default.

    Returns
    ---------
    rot_prod : `numpy.ndarray`
        Array containing the product of the dot product of the
        rotation matrices, based on the order of `rot_order` and the
        designated angles for each axes.
    """
    file_msg = fd.Program_Msg(__file__)
    # Checking type of `angle`
    ang_dict = {}
    cart_arr = ['x', 'y', 'z']
    ang_arr  = [x_ang, y_ang, z_ang]
    angle_type_arr = (float, int)
    for (cart_ii, ang_ii) in zip(cart_arr, ang_arr):
        if not (isinstance(ang_ii, angle_type_arr)):
            msg = '{0} `{1}_ang` ({2}) is not a valid input type ({3})'
            msg = msg.format(file_msg, cart_ii, type(ang_ii), angle_type_arr)
            raise TypeError(msg)
        else:
            ang_dict[cart_ii] = float(ang_ii)
    # Checking type for `rot_order`
    rot_order_type_arr = (str)
    if not (isinstance(rot_order, rot_order_type_arr)):
        msg = '{0} `rot_order` ({1}) is not a valid input type ({2})'
        msg = msg.format(file_msg, type(rot_order), rot_order_type_arr)
        raise TypeError(msg)
    # Checking that `rot_order` is only composed of ['x', 'y', 'z']
    rot_order_join = rot_order.lower().replace(' ', '').replace('', ' ').split()
    rot_order_unq  = set(rot_order_join)
    if not (all(xx in cart_arr for xx in rot_order_unq)):
        msg = '{0} `rot_order` ({1}) is not a valid choice!'
        msg = msg.format(file_msg, rot_order)
        raise ValueError(msg)
    else:
        # Defining order of 
        rot_order_arr = rot_order_join
    ##
    ## Determining the order of rotation matrices
    rot_matrix_arr = [cart_rotation_matrices(angle=ang_dict[xx], ax=xx)
                        for xx in rot_order_arr]
    # Taking the dot product of all matrices
    if len(rot_matrix_arr) == 1:
        dot_rot_matrix = rot_matrix_arr[0]
    elif len(rot_matrix_arr) > 1:
        dot_rot_matrix = np.linalg.multi_dot(rot_matrix_arr)

    return dot_rot_matrix

## Rotation of points in the Cartesian coordinates
def cartesian_rotation(cart_obj, x_ang=0, y_ang=0, z_ang=0, rot_order='xyz',
    return_pd=True):
    """
    Function to rotate a set of points in Cartesian coordinates by
    some `angle` along the `ax` axis.

    Parameters
    ------------
    cart_obj = `numpy.ndarray` or `pandas.DataFrame`
        Set of Cartesian coordinates for a given set of points.
        This variable has three coordinates.

    x_ang : `float`, optional
        Angle, by which the points are rotated around the `x` axis.
        This variable is set to ``0`` by default.

    y_ang : `float`, optional
        Angle, by which the points are rotated around the `y` axis.
        This variable is set to ``0`` by default.

    z_ang : `float`, optional
        Angle, by which the points are rotated around the `z` axis.
        This variable is set to ``0`` by default.

    rot_order : `str`, optional
        Type of rotation to make. `rot_order` is expected to have THREE
        letters from {'x', 'y', 'z'} element. This variable is set to
        ``xyz`` by default.

    return_pd : `bool`, optional
        If `True`, the function returns a DataFrame with the transformed
        Cartesian coordinates of the points. If `False, the function
        returns a (N,3) `numpy.ndarray`. This variable is set to `True`
        by default.

    Returns
    -----------
    cart_tr : `numpy.ndarray` or `pandas.DataFrame`
        Transformed set of Cartesian coordinates for each of the points
        given.
    """
    file_msg = fd.Program_Msg(__file__)
    # Checking type of `cart_obj`
    cart_obj_type = (np.ndarray, pd.DataFrame)
    if not (isinstance(cart_obj, cart_obj_type)):
        msg = '{0} `cart_obj` ({1}) is not a valid input type ({2})'
        msg = msg.format(file_msg, type(cart_obj), cart_obj_type)
        raise TypeError(msg)
    else:
        if isinstance(cart_obj, (cart_obj_type[0])):
            cart_arr = ['x', 'y', 'z']
            cart_pd  = pd.DataFrame(dict(zip(cart_arr, cart_obj.T)))
        elif isinstance(cart_obj, (cart_obj_type[1])):
            cart_arr = ['x', 'y', 'z']
            cart_pd  = pd.DataFrame(dict(zip(cart_arr, cart_obj.values.T)))
    cart_arr = ['x', 'y', 'z']
    ang_arr  = [x_ang, y_ang, z_ang]
    angle_type_arr = (float, int)
    for (cart_ii, ang_ii) in zip(cart_arr, ang_arr):
        if not (isinstance(ang_ii, angle_type_arr)):
            msg = '{0} `{1}_ang` ({2}) is not a valid input type ({3})'
            msg = msg.format(file_msg, cart_ii, type(ang_ii), angle_type_arr)
            raise TypeError(msg)
    # Checking type for `rot_order`
    rot_order_type_arr = (str)
    if not (isinstance(rot_order, rot_order_type_arr)):
        msg = '{0} `rot_order` ({1}) is not a valid input type ({2})'
        msg = msg.format(file_msg, type(rot_order), rot_order_type_arr)
        raise TypeError(msg)
    # Checking type of 'return_pd'
    return_pd_type_arr = (bool)
    if not (isinstance(return_pd, return_pd_type_arr)):
        msg = '{0} `return_pd` ({1}) is not a valid input type ({2})!'
        msg = msg.format(file_msg, type(return_pd), return_pd_type_arr)
        raise TypeError(msg)
    ##
    ## Extracting Cartesian coordinates
    nelem = len(cart_pd['x'])
    if (nelem == 1):
        pos_arr = cart_pd.values[:, np.newaxis]
    else:
        pos_arr = cart_pd.values.T
    # Computing Rotation matrices
    rot_prod = rotation_matrices_3D(x_ang=x_ang,
                                    y_ang=y_ang,
                                    z_ang=z_ang,
                                    rot_order=rot_order)
    # Multiplying by the Cartesian Coordinates
    cart_tr_arr = np.dot(rot_prod, pos_arr)
    # Choosing what to return
    if return_pd:
        cart_tr = pd.DataFrame(dict(zip(['x', 'y', 'z'], cart_tr_arr)))
    else:
        cart_tr = cart_tr_arr

    return cart_tr
