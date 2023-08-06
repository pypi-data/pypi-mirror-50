from __future__ import print_function, division, absolute_import

import numpy as np
import astropy.constants as const
import astropy.units as u
import scipy.integrate as integrate


__all__ = ["ioka2003", "inoue2004", "zhang2018", 
           "builtin_method_functions", "add_method", 
           "available_methods", "reset_methods", "method_functions"]


def _f_integrand(z, cosmo):
    """
    Calculate the integrand for a given redshift and cosmology. This
    the integrand for integral that appears in Zhang2018, Inoue2004
    and Ioka2003.

    Parameters
    ----------
    z : float
        The input redshift.

    cosmo : An instance of :obj:`astropy.cosmology`
        The cosmology to use in the integrand.

    Returns
    -------
    f : float
        The evaluated integrand.

    Notes
    -----
    The integrand is a follows:

    ..math::
        f = \\frac{1 + z}{\\Omega_{m,0}(1 + z)^3 +
        \\Omega_{\\Lambda,0} (1 + z)^{3(1 - w)}}

    """

    w = cosmo.w(z)

    top = 1 + z
    bot = cosmo.Om0 * (1 + z)**3 + cosmo.Ode0 * (1 + z)**(3 + 3 * w)
    return top / np.sqrt(bot)


def ioka2003(z, cosmo, zmin=0):
    """
    Calculate the dispersion measure at a redshift ``z`` given a
    cosmology using the Ioka (2003) relation.

    Parameters
    ----------
    z: float or int
        The input redshift.

    cosmo: An instance of :obj:`astropy.cosmology`
        The cosmology to assume when when calculating the dispersion
        measure at redshift ``z``.

    zmin: float or int, optional
        The minimum redshift to begin the integral. This should
        typically be zero. Default: 0.

    Returns
    -------
    dm : float
        The dispersion measure at the redshift ``z``.
    """
    # Calculate Ioka 2003 DM coefficient
    coeff_top = 3 * const.c * cosmo.H0 * cosmo.Ob0
    coeff_bot = 8 * np.pi * const.G * const.m_p
    coeff = coeff_top / coeff_bot

    coeff = coeff.to("pc cm**-3")

    dm = coeff * integrate.quad(_f_integrand, zmin, z, args=(cosmo))[0]

    return dm.value


def inoue2004(z, cosmo, zmin=0):
    """
    Calculate the dispersion measure at a redshift ``z`` given a
    cosmology using the Inoue (2004) relation.

    Parameters
    ----------
    z: float or int
        The input redshift.

    cosmo: An instance of :obj:`astropy.cosmology`
        The cosmology to assume when when calculating the dispersion
        measure at redshift ``z``.

    zmin: float or int, optional
        The minimum redshift to begin the integral. This should
        typically be zero. Default: 0.

    Returns
    -------
    dm : float
        The dispersion measure at the redshift ``z``.
    """

    # Coefficient from Inoue 2004
    inoue_n_e_0 = 9.2e-10 * ((u.Mpc**2 * u.s**2) / (u.km**2 * u.cm**3))

    coeff = inoue_n_e_0 * const.c * cosmo.Ob0 * cosmo.H0
    coeff = coeff.to("pc cm**-3")

    dm = coeff * integrate.quad(_f_integrand, zmin, z, args=(cosmo))[0]

    return dm.value


def zhang2018(z, cosmo, zmin=0, **kwargs):
    """
    Calculates the dispersion measure at a redshift given a cosmology
    using the Zhang (2018) relation.

    Parameters
    ----------
    z: float or int
        The input redshift.

    cosmo: An instance of :obj:`astropy.cosmology`
        The cosmology to assume when when calculating the dispersion
        measure at redshift ``z``.

    zmin: float or int, optional
        The minimum redshift to begin the integral. This should
        typically be zero. Default: 0.

    Keyword Arguments
    -----------------
    f_igm : float, optional
        The fraction of baryons in the intergalatic medium.
        Default: 0.83

    free_elec : float, optional
        The free electron number per baryon in the intergalactic
        medium. Default: 0.875

    Returns
    -------
    dm : float
        The dispersion measure at the redshift ``z``.

    """

    if "f_igm" in kwargs:
        if kwargs["f_igm"] <= 1 and kwargs["f_igm"] >= 0:
            f_igm = kwargs["f_igm"]
        else:
            raise ValueError("f_igm must be between 0 and 1.")
    else:
        f_igm = 0.83

    if "free_elec" in kwargs:
        if kwargs["free_elec"] <= 1 and kwargs["free_elec"] >= 0:
            free_elec = kwargs["free_elec"]
        else:
            raise ValueError("free_elec must be between 0 and 1.")
    else:
        free_elec = 0.875

    coeff_top = 3 * const.c * cosmo.H0 * cosmo.Ob0
    coeff_bot = 8 * np.pi * const.G * const.m_p
    coeff = coeff_top / coeff_bot

    coeff = coeff.to("pc cm**-3")
    dm = coeff * f_igm * free_elec * integrate.quad(_f_integrand, zmin, z,
                                                    args=(cosmo))[0]
    return dm.value


def builtin_method_functions():
    """
    Returns a dictionary of the builtin methods with keywords and
    corresponding dispersion measure functions.

    Returns
    -------
    methods: dict
        Contains the keywords and function for each method.
    """

    methods = {
        "Ioka2003": ioka2003,
        "Inoue2004": inoue2004,
        "Zhang2018": zhang2018
    }
    return methods


_available = builtin_method_functions()


def add_method(name, func):
    """
    Add a user defined method/DM-z relation to the list of available
    methods.

    Parameters
    ----------
    name : str
        The keyword for the new method.

    func : function
        The function to calculate the dispersion measure at a given
        redshift. The first argument of ``func`` must be ``z``.

    Return
    ------

    Example
    -------
    >>> def simple_dm(z):
            dm = 1200 * z
            return dm
    >>> fruitbat.add_method("simple_dm", simple_dm)
    """

    method = {name: func}
    _available.update(method)


def available_methods():
    """
    Returns the list containing all the keywords for valid methods.
    """
    return list(_available.keys())


def reset_methods():
    """
    Resets the list of available methods to the default builtin methods.
    """

    # Delete all keys that aren't in the list of builtin method functions
    remove = [k for k in available_methods()
              if k not in builtin_method_functions()]

    for key in remove:
        del _available[key]


def method_functions():
    """
    Returns a dictionary containing the valid method keys and their
    corresponding dispersion measure functions.
    """
    return _available
