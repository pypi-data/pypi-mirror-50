import periodictable as pdtb

r_e = pdtb.constants.electron_radius * 1e10  # classical electron radius, in A
N_A = pdtb.constants.avogadro_number  # Avogadro number, unitless
k_B = 1.38065e-23  # Boltzman constant, in J/K

import numpy as np
import cmath

import lmfit as lm
import scipy.stats as stat

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('xtick', labelsize=15)
mpl.rc('ytick', labelsize=15)
mpl.rc('axes', labelsize=15)
mpl.rc('axes', titlesize=15)
mpl.rc('font', family='serif')
mpl.rc('mathtext', default='regular', fontset='custom')
ticks_x = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x * 1000))

import .fit_ref as mfit
import .flu_geometry_routines as gm


def updateFluelement(params, flupara_sys, refpara, flu_elements):
    # unwrap fitting parameters
    conupbk = params['upbk'].value  # background linear is borrowed for upper phase concentration, in M
    conbulk = params['lobk'].value  # bulk concentration, in M

    # unwrap system parameters
    E_inc = float(flupara_sys[0])  # energy of incidence, in KeV
    E_emit = float(flupara_sys[1])  # energy of  emission, in KeV
    mu_top_inc = float(flupara_sys[2] / 1e8)  # abs. coef. of top phase for incidence, in 1/A
    mu_top_emit = float(flupara_sys[3] / 1e8)  # abs. coef. of top phase for emission, in 1/A
    mu_bot_inc = float(flupara_sys[4] / 1e8)  # abs. coef. of bot phase for incidence, in 1/A
    mu_bot_emit = float(flupara_sys[5] / 1e8)  # abs. coef. of bot phase for emission, in 1/A
    rho_top = flupara_sys[6]  # electron density of top pahse, in A^-3
    rho_bot = flupara_sys[7]  # electron density of top pahse, in A^-3
    slit = flupara_sys[8] * 1e7  # size of slit1, in A
    detlen = flupara_sys[9] * 1e7  # detector length, in A

    # calculate abosrption parameters.
    k0 = 2 * np.pi * E_inc / 12.3984  # wave vector for incidence, in A^-1
    k1 = 2 * np.pi * E_emit / 12.3984  # wave vector for emission, in A^-1

    # construct elemental parameters
    vol_top, vol_bot = 0, 0  # vol_bot for ions for 1 L subphase
    ne_top, ne_bot = 0, 0  # total number of electrons from 1 L subphase
    bet_top_inc_ele, bet_top_emit_ele = 0, 0  # beta: for top phase at inc.& emit.
    bet_bot_inc_ele, bet_bot_emit_ele = 0, 0  # beta: for bot phase at inc.& emit.
    flupara_ele = {}  # setup dict for all elements in the subphase
    for i, e in enumerate(flu_elements):
        flupara_ele[i] = \
            [e[0], float(e[1]), float(e[2]),  # name, composition, ionic radius
             pdtb.elements.symbol(e[0]).number,
             pdtb.elements.symbol(e[0]).xray.scattering_factors(energy=flupara_sys[0])[1],
             pdtb.elements.symbol(e[0]).xray.scattering_factors(energy=flupara_sys[1])[1]]
    for i, p in flupara_ele.iteritems():
        n_top_density = conupbk * p[1] * N_A / 1e27  # atoms per A^3 in top phase
        n_bot_density = conbulk * p[1] * N_A / 1e27  # atoms per A^3 in bot phase
        vol_top += n_top_density * 4 / 3 * np.pi * p[2] ** 3
        vol_bot += n_bot_density * 4 / 3 * np.pi * p[2] ** 3
        ne_top += n_top_density * p[3]  # electrons per A^3
        ne_bot += n_bot_density * p[3]  # electrons per A^3
        bet_top_inc_ele += n_top_density * 2 * np.pi * r_e * p[4] / k0 ** 2
        bet_top_emit_ele += n_top_density * 2 * np.pi * r_e * p[5] / k1 ** 2
        bet_bot_inc_ele += n_bot_density * 2 * np.pi * r_e * p[4] / k0 ** 2
        bet_bot_emit_ele += n_bot_density * 2 * np.pi * r_e * p[5] / k1 ** 2
    # absorption coefficient and electron density modified by solvent.
    rho_top = ne_top + (1 - vol_top) * rho_top
    rho_bot = ne_bot + (1 - vol_bot) * rho_bot

    mu_top_inc = 2 * k0 * bet_top_inc_ele + (1 - vol_top) * mu_top_inc
    mu_top_emit = 2 * k1 * bet_top_emit_ele + (1 - vol_top) * mu_top_emit
    mu_bot_inc = 2 * k0 * bet_bot_inc_ele + (1 - vol_bot) * mu_bot_inc
    mu_bot_emit = 2 * k1 * bet_bot_emit_ele + (1 - vol_bot) * mu_bot_emit

    bet_top_inc = mu_top_inc / k0 / 2
    bet_top_emit = mu_top_emit / k1 / 2
    bet_bot_inc = mu_bot_inc / k0 / 2
    bet_bot_emit = mu_bot_emit / k1 / 2

    del_top_inc = 2 * np.pi * r_e * rho_top / k0 ** 2  # del=2*PI*re*rho/k^2, unitless #self.flutopdel
    del_top_emit = 2 * np.pi * r_e * rho_top / k1 ** 2
    del_bot_inc = 2 * np.pi * r_e * rho_bot / k0 ** 2
    del_bot_emit = 2 * np.pi * r_e * rho_bot / k1 ** 2

    qc = 2 * k0 * np.sqrt(2 * (del_bot_inc - del_top_inc))

    flu_ele_params = [[E_inc, E_emit],
                      [k0, k1],
                      [rho_top, rho_bot, qc],
                      [mu_top_inc, mu_top_emit, mu_bot_inc, mu_bot_emit],
                      [bet_top_inc, bet_top_emit, bet_bot_inc, bet_bot_emit],
                      [del_top_inc, del_top_emit, del_bot_inc, del_bot_emit],
                      flupara_ele,
                      slit,
                      detlen]

    refpara[2]['rho_t'] = rho_top
    refpara[2]['mu_t'] = mu_top_inc
    refpara[2]['rho_b'] = rho_bot
    refpara[2]['mu_b'] = mu_bot_inc

    return flu_ele_params, refpara


def ref2min(parameters, x, y, yerr, fit=True, rrf=True, row=2):
    refparaname, refsysparaname, params = parameters
    row = row
    d = [params[refparaname[i * 4 + 3]] for i in range(row - 2)]
    rho = [params[refparaname[i * 4]] for i in range(row - 1)]
    mu = [params[refparaname[i * 4 + 1]] for i in range(row - 1)]
    sigma = [params[refparaname[i * 4 + 2]] for i in range(row - 1)]
    rho.append(params[refparaname[-2]])  # add bottom phase
    mu.append(params[refparaname[-1]])  # add bottom phase
    syspara = [params[refsysparaname[i]] for i in range(3)]
    if rrf == True:  # whether it is a rrf or ref model
        model = lambda xx: mfit.refCalFun(d, rho, mu, sigma, syspara, xx)
    else:
        model = lambda xx: mfit.refCalFun(d, rho, mu, sigma, syspara, xx, rrf=False)

    if fit == True:  # wether it returns the model or the rsiduals.
        return (model(x) - y) / yerr
    else:
        return model


def frsnllCal(dett, bett, detb, betb, mub, k0, alpha, alpha_new):
    eff_d = np.zeros(alpha_new.shape)
    trans = np.zeros(alpha_new.shape)
    for i, a_new in enumerate(alpha_new):
        if np.isinf(a_new): a_new = 0
        f1 = cmath.sqrt(complex(a_new ** 2, 2 * bett))
        fmax = cmath.sqrt(complex(a_new ** 2 - 2 * (detb - dett), 2 * betb))
        mu_a = 2 * k0 * fmax.imag
        # mu_eff = mu_a * (alpha/a_new) + mub
        mu_eff = mu_a + mub
        eff_d[i] = 1 / mu_eff
        trans[i] = 4 * abs(f1 / (f1 + fmax)) * abs(f1 / (f1 + fmax))
    # frsnll=abs((f1-fmax)/(f1+fmax))*abs((f1-fmax)/(f1+fmax))
    return eff_d, trans


def fluCalFun(flupara, flupara_sys, refpara, qz, shscan=False, beam_profile='uniform'):
    'takes in flupara, qz, return fluorescence data.'

    # unwrap fitting parameters
    qoff = flupara['qoff'].value  # q offset, in A^-1
    yscale = flupara['cali'].value  # y scale, unitless
    bgcon = flupara['bg'].value  # background constant, unitless.
    R = flupara['curv'].value * 1e10  # surface curvature, in A
    if R == 0: R = 10000 * 1e10  # radius set to very big when curvature is "zero".
    conupbk = flupara['upbk'].value  # background linear is borrowed for upper phase concentration, in M
    surden = flupara['surd'].value  # surface density, in A^-2
    conbulk = flupara['lobk'].value  # bulk concentration, in M
    sh = flupara['sh'].value
    lambda_ = flupara['lamb'].value

    # unwrap system parameters
    k0 = flupara_sys[1][0]
    mu = flupara_sys[3]
    bet = flupara_sys[4]
    del_ = flupara_sys[5]
    fluelepara = flupara_sys[6]
    slit = flupara_sys[7]  # size of slit1, in A
    detlen = flupara_sys[8]  # detector length, in A
    mu_top_inc, mu_top_emit, mu_bot_inc, mu_bot_emit = tuple(mu)
    bet_top_inc, bet_top_emit, bet_bot_inc, bet_bot_emit = tuple(bet)
    del_top_inc, del_top_emit, del_bot_inc, del_bot_emit = tuple(del_)

    # calculate reflectivity and footprint
    span = 75.6 * 1e7  # dimession of the sample call.
    qz = qz + qoff

    # deviation of sh is Qz dependent if sh=0, i.e.
    if sh == 0: sh = lambda_ * (qz - 0.006)

    refModel = ref2min(refpara, None, None, None, fit=False, rrf=False)
    alpha = qz / k0 / 2  # incident angles

    # define the beam profile as a gaussian beam up to +/-3 standard deviation
    steps = 500
    if beam_profile == 'uniform':
        weight = np.ones(steps + 1)
        fprint = slit / np.sin(alpha)  # beamsize is slit for a uniform profile.
    elif beam_profile == 'gaussian':
        stdev = slit / 2.355  # slit size is the FWHM of the beam, i.e. 2.355 sigma
        beamsize = 2 * (3 * stdev)  # keep the beam up to +/-3 standard deviation, or 99.73% of intensity.
        rays = np.linspace(-beamsize / 2, beamsize / 2, steps + 1)  # devide the beam into 500 rays
        weight = stat.norm(0, stdev).pdf(rays) * slit  # weight normalized to the total intensity
        fprint = beamsize / np.sin(alpha)  # get the footprints in unit of /AA
    else:
        print
        "Error: please choose the right beam profile: uniform/gaussian"

    center = - sh * 1.0e7 / alpha

    # initialize fluorescence data, rows: total, aqueous, organic, interface
    absorb = lambda x: np.nan_to_num(np.exp(x))
    flu = np.zeros((6, len(alpha)))
    for i, a0 in enumerate(alpha):

        stepsize = fprint[i] / steps

        # get the position of single ray hitting the surface
        x0 = np.linspace(center[i] - fprint[i] / 2, center[i] + fprint[i] / 2, steps + 1)
        surface = np.array([gm.hit_surface([xx, 0], -a0, R, span) for xx in x0])
        miss = np.isinf(surface[:, 1])  # number of rays that miss the interface
        x_s = surface[~miss][:, 0]  # x' for rays that hit on the interface
        z_s = surface[~miss][:, 1]  # z' for rays that hit on the interface
        wt_s = weight[~miss]  # weight for rays that hit on the interface

        # (x,z) and other surface geometry for points where beam hit at the interface.
        theta = -x_s / R  # incline angle
        a_new = a0 + theta  # actual incident angle w.r. to the surface
        # a1 = a0 + 2 * theta
        a1 = a0
        x_inc = x_s + z_s / a0  # x position where the inc. xray passes z=0 line
        x_ref = x_s - z_s / a1  # x position where the inc. xray passes z=0 line.

        mu_eff_inc = mu_top_emit + mu_top_inc / a0  # eff.abs.depth for incident beam in oil phase
        mu_eff_ref = mu_top_emit - mu_top_inc / a1  # eff.abs.depth for reflected beam in water phase

        # z coordinate of the intersection of ray with following:
        z_inc_l = (x_inc + detlen / 2) * a0  # incidence with left det. boundary: x=-l/2
        z_inc_r = (x_inc - detlen / 2) * a0  # incidence with right det. boundary: x=l/2
        z_ref_l = -(x_ref + detlen / 2) * a1  # reflection with left det. boundary: x=-l/2
        z_ref_r = -(x_ref - detlen / 2) * a1  # reflection with right det. boundary: x=l/2

        # two regions: [-h/2a0,-l/2] & [-l/2,l/2]
        x_region = [(x_s <= -detlen / 2), (x_s > -detlen / 2) * (x_s < detlen / 2)]

        ################### for region x>= l/2  ########################
        x0_region1 = x0[surface[:, 0] > detlen / 2]  # choose x0 with x'>l/2
        wt_region1 = weight[surface[:, 0] > detlen / 2]  # choose weight with x'>l/2
        upper_bulk1 = wt_region1 * \
                      absorb(-x0_region1 * mu_top_inc) / mu_eff_inc * \
                      (absorb((x0_region1 + detlen / 2) * a0 * mu_eff_inc) -
                       absorb((x0_region1 - detlen / 2) * a0 * mu_eff_inc))

        if len(x_s) != 0:
            ref = refModel(2 * k0 * a_new)  # calculate the reflectivity at incident angle alpha_prime.
            effd, trans = frsnllCal(del_top_inc, bet_top_inc, del_bot_inc, bet_bot_inc,
                                    mu_bot_emit, k0, a0, a_new)

            # flootprint (in mm)  weighted by reflection used as sample height scan
            eff_stepsize = stepsize / (1 - theta / a0)  # stepsize corrected by curvature
            # flu[5,i] = np.sum(ref * eff_stepsize) * 1e-7
            flu[5, i] = np.sum(eff_stepsize) * 1e-7

        if shscan == False:  # if shscan is true, flurescence is skipped
            # if beam miss the surface entirely, do the following:
            if len(x_s) == 0:  # the entire beam miss the interface, only incidence in upper phase.
                # sh_offset_factor = absorb(-mu_top_emit * center[i] * a0)
                usum_inc = stepsize * np.sum(upper_bulk1)
                flu[2, i] = yscale * usum_inc * N_A * conupbk * fluelepara[0][1] / 1e27  # oil phase incidence only
                flu[0, i] = flu[2, i]  # total intensity only contains oil phase
                continue

            ################### for region -l/2 < x < l/2  #################
            lower_bulk2 = x_region[1] * wt_s * absorb(-x_s * mu_top_inc - z_s / effd) * trans * effd * \
                          (absorb(z_s / effd) - absorb(z_inc_r / effd))
            surface = x_region[1] * wt_s * trans * absorb(-mu_top_inc * x_s)
            upper_bulk2_inc = x_region[1] * wt_s * \
                              (absorb(-x_inc * mu_top_inc) / mu_eff_inc * (
                                      absorb(z_inc_l * mu_eff_inc) - absorb(z_s * mu_eff_inc)))
            upper_bulk2_inc[np.isnan(upper_bulk2_inc)] = 0  # if there is nan, set to 0
            upper_bulk2_ref = x_region[1] * wt_s * \
                              (absorb(-x_ref * mu_top_inc) / mu_eff_ref * ref * (
                                      absorb(z_ref_r * mu_eff_ref) - absorb(z_s * mu_eff_ref)))
            upper_bulk2_ref[np.isnan(upper_bulk2_ref)] = 0  # if there is nan, set to 0

            ###################### for region x<=-l/2 ########################
            lower_bulk3 = x_region[0] * wt_s * absorb(-x_s * mu_top_inc - z_s / effd) * trans * effd * \
                          (absorb(z_inc_l / effd) - absorb(z_inc_r / effd))
            upper_bulk3 = x_region[0] * wt_s * absorb(-x_ref * mu_top_inc) / mu_eff_ref * ref * \
                          (absorb(mu_eff_ref * z_ref_r) - absorb(mu_eff_ref * z_ref_l))

            # combine the two regions and integrate along x direction by performing np.sum.
            bsum = stepsize * np.sum(lower_bulk3 + lower_bulk2)
            ssum = stepsize * np.sum(surface)
            usum_inc = stepsize * (np.sum(upper_bulk1) + np.sum(upper_bulk2_inc))
            usum_ref = stepsize * (np.sum(upper_bulk3) + np.sum(upper_bulk2_ref))

            # vectorized integration method is proved to reduce the computation time by a factor of 5 to 10.
            int_bulk = yscale * bsum * N_A * conbulk * fluelepara[0][1] / 1e27
            int_upbk_inc = yscale * usum_inc * N_A * conupbk * fluelepara[0][1] / 1e27  # metal ions in the upper phase.
            int_upbk_ref = yscale * usum_ref * N_A * conupbk * fluelepara[0][1] / 1e27  # metal ions in the upper phase.
            int_sur = yscale * ssum * surden
            int_tot = int_bulk + int_sur + int_upbk_inc + int_upbk_ref + bgcon
            flu[:5, i] = np.array([int_tot, int_bulk, int_upbk_inc, int_upbk_ref, int_sur])

    return flu


def flu2min(params, x, y, yerr, other_params):
    flupara_sys, refpara = other_params
    model = fluCalFun(params, flupara_sys, refpara, x)
    residual = (model[0] - y) / yerr
    return residual


if __name__ == '__main__':

    # file_dir = '/Users/zhuzi/work/data/201703Mar/'
    # file_name = 'sample6_42mM_Eu(NO3)3_pure_dodecane_scan364_flu.txt'
    # file_dir = '/Users/zhuzi/work/data/201811Nov/'
    # file_name = 'sample01_water_10mMHDEHP_1mMEu_RT_scan140_peak1_flu.txt'
    file_dir = '/Users/zhuzi/work/data/201907Jul/'
    file_name = 'sample4_50mMEu(NO3)3_scan474-481_flu.txt'
    data = np.loadtxt(file_dir + file_name)
    x, y, yerr = data[:, 0], data[:, 1], data[:, 2]

    fit = 1
    params = lm.Parameters()
    # add tuples:   (NAME    VALUE   VARY MIN  MAX  EXPR BRUTE_STEP)
    params.add_many(('qoff', 1.54e-4, 1, None, None, None, None),  # q offset, in A^-1
                    ('cali', 2.14e-10, 1, None, None, None, None),  # Calibration factor, unitless
                    ('bg', 4.70e-3, 0, 0, None, None, None),  # background constant, unitless.
                    ('curv', 500.0, 1, -100, 220, None, None),  # surface curvature, in A
                    ('upbk', 0.00e-3, 0, 0, None, None, None),  # upper phase concentration, in M
                    ('surd', 0.0e-3, 0, 0, None, None, None),  # surface density, in A^-2
                    ('lobk', 50.e-3, 0, None, None, None, None),  # lower phase concentration, in M
                    ('sh', -0.00, 0, None, None, None, None),  # sh value
                    ('lamb', 0.5, 1, -0.5, None, None, None))  # lambda value for sh=lambda(Qz-0.006)

    # parameters for reflectivity
    refparaname = ['rho_t', 'mu_t', 'sigma0', 'rho_b', 'mu_b']
    refsysparaname = ['q_off', 'y_scale', 'q_res']
    refparameter = {'rho_t': 0.2591,
                    'mu_t': 0.0,
                    'sigma0': 3.0,
                    'rho_b': 0.333,
                    'mu_b': 0.0,
                    'q_off': 0,  # this value shoulb be kept 0
                    'y_scale': 1.0,
                    'q_res': 0.0}
    refpara = (refparaname, refsysparaname, refparameter)

    # parameters for x-ray
    flupara_sys_raw = [20,  # energy of incidence, in KeV
                       5.842,  # energy of emission, in KeV
                       0.2730,  # abs.coef. of top phase for incidence, in cm^-1
                       7.451,  # abs.coef. of top phase for emission, in cm^-1
                       0.7018,  # abs.coef. of bot phase for incidence, in cm^-1
                       26.58,  # abs.coef. of bot phase for emission, in cm^-1
                       0.2591,  # electron density of top pahse, in A^-3
                       0.333,  # electron density of bot pahse, in A^-3
                       0.015,  # size of slit1, in mm
                       12.7]  # detector length, in mm

    # flupara_sys modified by the presence of elements
    flu_elements = [['Eu', 1, 0.947]]  # name, composition, Ionic Radius(A)
    flupara_sys, refpara_sys = updateFluelement(params, flupara_sys_raw, refpara, flu_elements)
    for p in flupara_sys: print
    p
    qz = np.linspace(0.005, 0.016, 100)
    refModel = ref2min(refpara_sys, None, None, None, fit=False, rrf=False)
    ref = refModel(qz + params['qoff'].value)
    qc = qz[np.sum(ref > 0.9999) - 1]

    # flu_uniform = fluCalFun(params, flupara_sys, refpara_sys, qz, beam_profile='uniform')
    guess = fluCalFun(params, flupara_sys, refpara_sys, qz, beam_profile='uniform')

    #########################################################
    fig = plt.figure(figsize=(8, 10), dpi=100)
    ax1 = fig.add_subplot(211)
    ax1.xaxis.set_major_formatter(ticks_x)
    ax1.set_xlabel(r'$Qz\ (\times 10^{-3} {\AA}^{-1})$', fontsize=15)
    ax1.set_ylabel('Fluorescence Intensity', fontsize=15)
    ax1.set_xlim([qz[0] * 0.8, qz[-1] * 1.1])
    # ax1.set_ylim([-0.00, 0.02])
    ax1.grid(1)

    ax1.axvline(qc, color='black', alpha=0.5)
    # ax1.plot(qz, flu_uniform[0], ls='-', label='uniform profile')
    ax1.plot(qz, guess[0], ls='-', label='guess')
    ax1.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2],
                 marker='o', ls='', color='r', label='data')
    ax1.legend(loc='best')

    if fit == True:
        fit_range = [0e-3, 16e-3]
        data_to_fit = data[(x >= fit_range[0]) * (x <= fit_range[1])]

        other_params = (flupara_sys, refpara)
        result = lm.minimize(flu2min, params,
                             args=(data_to_fit[:, 0], data_to_fit[:, 1], data_to_fit[:, 2], other_params))
        print
        lm.fit_report(result)
        fit_flu = fluCalFun(result.params, flupara_sys, refpara_sys, qz)

        ax2 = fig.add_subplot(212)
        ax2.xaxis.set_major_formatter(ticks_x)
        ax2.set_xlabel(r'$Qz\ (\times 10^{-3} {\AA}^{-1})$', fontsize=15)
        ax2.set_ylabel('Fluorescence Intensity', fontsize=15)
        ax2.set_xlim([qz[0] * 0.8, qz[-1] * 1.1])
        # ax1.set_ylim([-0.001, 0.013])
        ax2.grid(1)

        ref = refModel(qz + result.params['qoff'].value)
        qc = qz[np.sum(ref > 0.9999) - 1]

        ax2.axvline(qc, color='black', alpha=0.5)
        ax2.plot(qz, fit_flu[0], ls='-', color='b', label='fit')
        ax2.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2],
                     marker='o', ls='', color='r', label='data')
        ax2.legend(loc='best')

    plt.show()



