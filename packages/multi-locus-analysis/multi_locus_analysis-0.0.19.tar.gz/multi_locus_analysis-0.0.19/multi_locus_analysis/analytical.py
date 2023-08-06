"""For computing analytical results relevant to diffusing loci"""
from bruno_util.mittag_leffler import ml as mittag_leffler

import numpy as np
import scipy
from scipy.special import gamma
from scipy.signal import savgol_filter, savgol_coeffs
from numba import jit
import mpmath

from functools import lru_cache
from pathlib import Path

def frac_msd(t, alpha, kbT=1, xi=1):
    """MSD of fractionally diffusing free particle.

    Weber, Phys Rev E, 2010 (Eq 10)"""
    return 3*kbT/xi*np.sin(alpha*np.pi)*t**alpha \
        /(np.pi*(1-alpha/2)*(1-alpha)*alpha)

def frac_cv(t, alpha, kbT=1, xi=1):
    """Velocity autocorrelation of a fractionally-diffusing particle.
    Weber, Phys Rev E, 2010 (Eq 32)"""
    return -(3*kbT/xi)*np.sin(alpha*np.pi)/(np.pi*(2-alpha))*np.abs(np.power(t, alpha-2))

def frac_discrete_cv(t, delta, alpha, kbT=1, xi=1):
    """Discrete velocity autocorrelation of a fractionally-diffusing particle.
    Weber, Phys Rev E, 2010 (Eq 33)"""
    t = np.atleast_1d(t)
    delta = np.atleast_1d(delta)
    # too many divide by t's to rewrite to avoid these warnings in less than
    # 5min, not worth it.
    with np.errstate(divide='ignore', invalid='ignore'):
        eta = delta/t
        t = t + np.zeros_like(eta) # fix to full size if not already
        delta = delta + np.zeros_like(eta) # fix to full size if not already
        cv_delta_t = frac_cv(t, alpha, kbT, xi)/(eta*eta*alpha*(1 - alpha))
        cv_delta_t[eta<=1] = cv_delta_t[eta<=1] \
            *(2 - np.power(1 - eta[eta<=1], alpha) - np.power(1 + eta[eta<=1], alpha))
        cv_delta_t[eta>1] = cv_delta_t[eta>1] \
            *(2 + np.power(eta[eta>1] - 1, alpha) - np.power(1 + eta[eta>1], alpha)) \
            + frac_msd(delta[eta>1] - t[eta>1], alpha, kbT, xi)/delta[eta>1]/delta[eta>1]
        cv_delta_t[t == 0] = frac_msd(delta[t == 0], alpha, kbT, xi)/np.power(delta[t == 0], 2)
    return cv_delta_t

def frac_discrete_cv_normalized(t, delta, alpha):
    """Normalized discrete velocity autocorrelation of a fractionally-diffusing
    particle. Should be equivalent to

        frac_discrete_cv(t, delta, 1, 1)/frac_discrete_cv(0, delta, 1, 1)

    Lampo, BPJ, 2016 (Eq 5)"""
    return (np.power(np.abs(t - delta), alpha)
        - 2*np.power(np.abs(t), alpha)
        + np.power(np.abs(t + delta), alpha)
        )/(2*np.power(delta, alpha))

@jit
def rouse_mode(p, n, N=1):
    """Eigenbasis for Rouse model.

    Indexed by p, depends only on position n/N along the polymer of length N.
    N=1 by default.

    Weber, Phys Rev E, 2010 (Eq 14)"""
    p = np.atleast_1d(p)
    phi = np.sqrt(2)*np.cos(p*np.pi*n/N)
    phi[p == 0] = 1
    return phi

def rouse_mode_coef(p, b, N, kbT=1):
    """k_p: Weber Phys Rev E 2010, after Eq. 18."""
    # alternate: k*pi**2/N * p**2, i.e. k = 3kbT/b**2
    return 3*np.pi**2*kbT/(N*b**2)*p**2

def rouse_mode_corr(p, t, alpha, b, N, kbT=1, xi=1):
    """Weber Phys Rev E 2010, Eq. 21."""
    kp = rouse_mode_coef(p, b, N, kbT)
    return (3*kbT/kp)*mittag_leffler((-kp*t**alpha)/(N*xi*gamma(3-alpha)), alpha, 1)

def simple_rouse_mid_msd(t, b, N, kbT=1, xi=1, num_modes=1000):
    """
    modified from Weber Phys Rev E 2010, Eq. 24.
    """
    rouse_corr = 0
    for p in range(1, num_modes+1):
        k2p = rouse_mode_coef(2*p, b, N, kbT)
        rouse_corr += 12*kbT/k2p*(1 - np.exp(-k2p*t/(N*xi)))
    return rouse_corr + 6*kbT/xi/N*t

def rouse_mid_msd(t, alpha, b, N, kbT=1, xi=1, num_modes=1000):
    """
    Weber Phys Rev E 2010, Eq. 24.
    """
    if alpha == 1:
        return simple_rouse_mid_msd(t, b, N, kbT, xi, num_modes)
    rouse_corr = 0
    for p in range(1, num_modes+1):
        k2p = rouse_mode_coef(2*p, b, N, kbT)
        rouse_corr += 12*kbT/k2p*(1 - mittag_leffler(-k2p*t**alpha/(N*xi*gamma(3-alpha)),
                alpha, 1))
    return rouse_corr + frac_msd(t, alpha, kbT, xi)/N

def tR(alpha, b, N, kbT=1, xi=1):
    """Lampo et al, BPJ, 2016, eq 8"""
    return np.power(N*N*b*b*xi/kbT, 1/alpha)

def tDeltaN(n1, n2, alpha, b, kbT, xi):
    """Lampo et al, BPJ, 2016, eq 11"""
    delN = np.abs(n2 - n1)
    return np.power(delN*delN*b*b*xi/kbT, 1/alpha)

def rouse_cv_mid(t, alpha, b, N, kbT=1, xi=1, min_modes=1000):
    """Velocity autocorrelation of midpoint of a rouse polymer.

    Weber Phys Rev E 2010, Eq. 33."""
    t = np.atleast_1d(t)
    psum = np.zeros_like(t)
    for p in range(1, min_modes+1):
        k2p = rouse_mode_coef(2*p, b, N, kbT)
        coef = -k2p/(N*xi*gamma(3-alpha))
        psum += mittag_leffler(coef*np.power(t, alpha), alpha, alpha-1)
    gam = 1
    return frac_cv(t, alpha, kbT, xi)*(1 + 2*gam*(alpha - 1)*psum)

def rouse_cvv_ep(t, delta, p, alpha, b, N, kbT=1, xi=1):
    """Term in parenthesis in Lampo, BPJ, 2016 Eq. 10."""
    t = np.atleast_1d(t)
    delta = np.atleast_1d(delta)
    p = np.atleast_1d(p)
    tpdelta = np.power(np.abs(t + delta), alpha)
    tmdelta = np.power(np.abs(t - delta), alpha)
    ta = np.power(np.abs(t), alpha)
    kp = rouse_mode_coef(p, b, N, kbT)
    z = -kp/(N*xi*gamma(3 - alpha))
    return -mittag_leffler(z*tpdelta, alpha, 1) \
        + 2*mittag_leffler(z*ta, alpha, 1) \
        - mittag_leffler(z*tmdelta, alpha, 1)

def rouse_large_cvv_g(t, delta, deltaN, b, kbT=1, xi=1):
    """Cvv^delta(t) for infinite polymer.

    Lampo, BPJ, 2016 Eq. 16."""
    k = 3*kbT/b**2
    ndmap = lambda G, arr: np.array(list(map(G, arr)))
    G = lambda x: float(mpmath.meijerg([[],[3/2]], [[0,1/2],[]], x))
    gtmd = ndmap(G, np.power(deltaN, 2)*xi/(4*k*np.abs(t-delta)))
    gtpd = ndmap(G, np.power(deltaN, 2)*xi/(4*k*np.abs(t+delta)))
    gt = ndmap(G, np.power(deltaN, 2)*xi/(4*k*np.abs(t)))
    return 3*kbT/(np.power(delta, 2)*np.sqrt(xi*k))* (
        np.power(np.abs(t - delta), 1/2)*gtmd
      + np.power(np.abs(t + delta), 1/2)*gtpd
      - 2*np.power(np.abs(t), 1/2)*gt
    )

def rouse_cvv(t, delta, n1, n2, alpha, b, N, kbT=1, xi=1, min_modes=500,
              rtol=1e-5, atol=1e-8, force_convergence=True):
    """Velocity cross-correlation of two points on fractional Rouse polymer

    rtol/atol specify when to stop adding rouse modes. a particle (t,delta)
    pair is considered to have converged when np.isclose returns true give
    rtol/atol and p is even (p odd contributes almost nothing)

    Lampo, BPJ, 2016 Eq. 10."""
    t = np.atleast_1d(t)
    delta = np.atleast_1d(delta)
    tpdelta = np.power(np.abs(t + delta), alpha)
    tmdelta = np.power(np.abs(t - delta), alpha)
    ta = np.power(np.abs(t), alpha)
    # center of mass velocity correlation
    c0 = 3*kbT/(delta*delta*N*xi*gamma(3-alpha)*gamma(1+alpha)) \
            * (tpdelta + tmdelta - 2*ta)
    # correction factor due to being on a polymer is an expansion in terms of
    # the normal modes of the polymer
    rouse_corr = np.zeros_like(tpdelta)
    # because the rouse modes are cos(p*pi*(n/N)), then the number of p's to
    # include per pass before checking for convergence again should be
    theta_eps = min(n1/N/2, n2/N/2)
    chunk_size = int(np.ceil(2*np.pi/theta_eps))
    # first include the first min_modes for all values of t
    for p in range(1, min_modes+1):
        kp = rouse_mode_coef(p, b, N, kbT)
        z = -kp/(N*xi*gamma(3-alpha))
        pdiff = 3*kbT/kp*rouse_mode(p, n1, N)*rouse_mode(p, n2, N) \
                *(2*mittag_leffler(z*ta, alpha, 1)
                - mittag_leffler(z*tpdelta, alpha, 1)
                - mittag_leffler(z*tmdelta, alpha, 1))
        rouse_corr = rouse_corr + pdiff
    counts = min_modes*np.ones_like(rouse_corr)
    if not force_convergence:
        return c0 + rouse_corr
    # now include more terms in chuck_size number of p's at a time until
    # convergence.
    p += 1
    old_rouse_corr = rouse_corr.copy() # force alloc
    tol_i = np.ones_like(rouse_corr).astype(bool) # always at least one correction term
    while np.any(tol_i):
        tpd = tpdelta[tol_i]
        tmd = tmdelta[tol_i]
        tai = ta[tol_i]
        old_rouse_corr[:] = rouse_corr # force memmove
        for i in range(chunk_size):
            kp = rouse_mode_coef(p, b, N, kbT)
            z = -kp/(N*xi*gamma(3-alpha))
            pdiff = 3*kbT/kp*rouse_mode(p, n1, N)*rouse_mode(p, n2, N) \
                    *(2*mittag_leffler(z*tai, alpha, 1)
                        - mittag_leffler(z*tpd, alpha, 1)
                        - mittag_leffler(z*tmd, alpha, 1))
            rouse_corr[tol_i] = rouse_corr[tol_i] + pdiff
            counts[tol_i] += 1
            p += 1
        tol_i = ~np.isclose(rouse_corr, old_rouse_corr, rtol, atol)
    return c0 + rouse_corr, counts

def rouse_nondim_(t, delta, n1, n2, alpha, b, N, kbT=1, xi=1):
    """uses parameters defined by Lampo et al, BPJ, 2016, eq 12"""
    tOverDelta = t/delta
    deltaOverTDeltaN = delta/tR(alpha, b, N, kbT, xi) \
            *np.power(np.abs(n2-n1)/N, -2/alpha)
    return tOverDelta, deltaOverTDeltaN, alpha
rouse_nondim = np.vectorize(rouse_nondim_)

def un_rouse_nondim(tOverDelta, deltaOverTDeltaN, alpha, delN=0.001):
    """Takes a requested choice of parameters to compare to Tom's calculated
    values and generates a full parameter list that satisfies those
    requirements.

    uses approximation defined by Lampo et al, BPJ, 2016, eq 12

    In Tom's paper, delN is non-dimensinoalized away into deltaOverTDeltaN, but
    that only works in the case where the chain is infinitely long. Otherwise,
    where exactly we choose n1,n2 will affect the velocity correlation because
    of the effects of the chain ends. While other choices are truly arbitrary
    (e.g. kbT, N, b, etc), delN can be used to specify the size of the segment
    (relative to the whole chain) used to compute the cross correlation."""
    # get arbitrary choices out of the way first
    N = 1
    b = 1
    kbT = 1
    xi = 1
    n1 = N/2
    n2 = N/2 + delN
    # now the computed quantities
    tr = tR(alpha, b, N, kbT, xi)
    delta = deltaOverTDeltaN*tr*np.power(delN/N, 2/alpha)
    t = tOverDelta*delta
    return t, delta, n1, n2, alpha, b, N, kbT, xi

def vc(t, delta, beta):
    """velocity correlation of locus on rouse polymer. beta = alpha/2."""
    return ( np.power(np.abs(t - delta), beta)
           + np.power(np.abs(t + delta), beta)
           - 2*np.power(np.abs(t), beta)
           )/( 2*np.power(delta, beta) )

def vcp(t, delta, beta):
    return ( np.power(np.abs(t + delta), beta)
           - np.power(np.abs(t), beta) )*np.power(delta, beta)

# precomupted velocity cross-correlation for rouse polymer
# from Lampo et al, was pre-computed on a grid...
deltas_ = np.linspace(-3, 3, 25) # placeholders for corresponding values in logspace
alphas_ = np.linspace(0.25, 1, 31) # steps of 0.025
tOverDeltas_ = np.linspace(0, 5, 501) # steps of 0.01
vvcf_table_ = np.reshape(np.loadtxt(Path(__file__).parent / Path('vvcf_table.csv'),
        delimiter=','), (31, 25, 501))
def calc_vel_corr_fixed_(tOverDelta, deltaOverTDeltaN, alpha):
    # this performs interpolation in logspace for "delta"/deltaOverTDeltaN
    deltaOverTDeltaN = np.log10(deltaOverTDeltaN)
    return scipy.interpolate.interpn((alphas_, deltas_, tOverDeltas_),
                                     vvcf_table_,
                                     (alpha, deltaOverTDeltaN, tOverDelta))
calc_vel_corr_fixed_.vvcf = None
calc_vel_corr_fixed = np.vectorize(calc_vel_corr_fixed_)

def vvc_unscaled_theory(t, delta, beta, A, tDeltaN):
    """velocity cross correlation of two points on rouse polymer."""
    return 2*(vc(t*delta, delta, beta) - calc_vel_corr_fixed(t, delta/tDeltaN, 2*beta))

def vvc_rescaled_theory(t, delta, beta, A, tDeltaN):
    """velocity cross correlation of two points on rouse polymer."""
    return 2*A*np.power(delta, beta)*(vc(t*delta, delta, beta) - calc_vel_corr_fixed(t, delta/tDeltaN, 2*beta))

def vvc_normalized_theory(t, delta, beta, A, tDeltaN):
    return vvc_unscaled_theory(t, delta, beta, A, tDeltaN) \
         / vvc_unscaled_theory(0, delta, beta, A, tDeltaN)

