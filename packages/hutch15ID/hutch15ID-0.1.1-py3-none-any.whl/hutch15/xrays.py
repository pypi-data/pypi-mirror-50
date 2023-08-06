#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import integrate
from uncertainties import ufloat as uf
''' This file includes basic formuli to use in x-ray physics'''

#functions that are methods
__all__ = [
    'fresnel', 'errFunction', 'RRF', 'densityProfile', 'RtoRRf', 'eDensitySolution',
    'muElement','roughness','criticalAngle','penetrateDepth'
]
# global constant
PI = np.pi # PI = 3.1415926...
re = 2.818e-5 # classical electron radius, r_e = 2.818e-15 m
N_A = 6.02e23 # Avogadro's number

def beam(energy):
    '''
    calculate the wavelength and wavevector for a given energy.
    '''
    wavelength = 12400/float(energy)
    wavevector = 2*3.1415926/wavelength
    return (wavelength, wavevector)

def BornApprox(qz,ds,rhos,rough,rho_0=0.333,rho_N=0.2574,qc=0.0103):
    '''
        This model calculates the R/Rf for a given layer profile and for a given
    range of qz. This function utilizes the Eq.S4 in "supporting information"
    for the paper "J.Phys.Chem 8 2014,118,10662-10674".
        Born approximation
        
    Parameters
    ----------
    qz: 1-D array of a range of q's to be considered for.
    ds: 1-D array containing the thickness for each layer, of the order from
        bottom up (does not include water and oil)
    rhos: 1-D array containing the electron density for each layer, of the order
          from bottom up.(does not include water and oil)
    rough: floating number, roughness of interface, all same.
    rho_0: electron density of water, 0.333 by default.
    rho_N: electron density of oil, 0.2574 by default.
    qc: critical angle for water/oil configuration, 0.0103 by default.
    
    Returns
    -------
    RRf_model: 1-D array of calculation of R/Rf, it has the same size as q.
    '''
    qz = np.array(qz)
    # N is the amount of interfaces
    layers = len(rhos)
    N = layers + 1
    # includes upper and bottom phase as first and last layer.
    rhos = np.hstack(([rho_0],rhos,[rho_N]))
    ds = np.hstack(([10000],ds,[10000]))
    # z is the height of each interface, counts from 0 to N-1
    # z[0] is the interface between water and the bottom layer.
    # z[N-1] is the interface between oil and the top layer.
    z = np.zeros(N)
    for i in range(layers): 
        # does not include bulk (ds[0],ds[-1])
        z[i+1] = z[i] + ds[i+1] 
    # d_total is the sum of the thickness of all the layers.
    d_total = z[-1]
    #####################___Equation S4___##########################
    # coefficient ->
    coefficient = np.exp(-rough * qz**2)/(rhos[0]-rhos[-1])**2
    '''
    # first summation ->
    sum1 = sum((x-y)**2 for (x,y) in zip(rhos,rhos[1:]))
    # second summation ->
    sum2 = np.zeros(len(qz))
    for i in range(N):
        for j in range(i+1,N):
            term = (rhos[i]-rhos[i+1])*(rhos[j]-rhos[j+1]) \
                    *np.cos(qz*(z[i]-z[j]))
            sum2 += term
    # result ->
    result = coefficient * (sum1 + sum2)

    
    '''
    # summation
    sum3 = np.zeros(len(qz),'complex')
    for i in range(N):
        term = (rhos[i]-rhos[i+1]) \
             * (np.cos(qz*z[i])-1j*np.sin(qz*z[i]))
        sum3 += term
    # result ->
    result = coefficient * np.absolute(sum3)**2
    
    return result


    
    
def criticalAngle(rho1,rho2):
    '''
    simple formula to calculate the critical angle between two liquid pahses
    using Qc=4*sqrt(PI*re(rho_bottom - rho_top))
    "J. Phys. Chem. B 2014, 118, 12486−12500" page5, shortly after equation(2).
    Parameters
    ----------
    rho1: electron density with larger value, in A^-3 (0.3346 for water)
    rho2: electron density with smaller value, in A^-3 (0.2595 for dodecane)
    
    Notes
    -----
    for 3 HNO3: the electron density is 0.362, critical angle: 0.0122
    print criticalAngle(0.0334,0.2596) -> Qc=0.01026 consistant with Wei's
    print criticalAngle(0.3618,0.2596) -> Qc=0.0120
    print criticalAngle(0.348,0.2672) -> Qc=0.0107
    Returns
    -------
    criticalAngle: critical angle between two phases.
    
    
    '''
    Qc = 4*np.sqrt(PI*re*(rho1-rho2))
    return Qc



    
def densityProfile(rhos, ds, roughness, rho_0=0.333003, rho_N=0.2574):
    '''
        Takes in the electron density for each layer and calculate the electron
    density profile. The length of the input arrays is the count of sublayers.
    We use same roughness for all interfaces.
        The arguement "rhos" and "ds" themselves only imply layers between two
    phases, i.e., [rho1,rho2,...,rhoN-1],they are then modified to include the 
    two bulk phase, resulting "rhos" to be: [rho0,rho1,rho2,...,rhoN], and 
    "ds" to be likewise.
    
    Parameters
    ----------
    rhos: array_like
        An array of electron density of the layers, from water side to oil side.
    ds: array_like
         An array of thickness of the layers, from water side to oil side.
    roughsness: floating number
        roughness which is same for all the interfaces.
    rho_0: floating number
        The electron density of bottom phase, 0.333003 for water.
    rho_N: floating number
        The electron density of upper phase, 0.2574 for dodecane.
    See also
    --------
    Wei, Journal of pyical chamistry B, 2014 Equation(1)
    
    Returns
    -------
    densityProfile: electron density along z direction.
    '''
    # N is the number of interfaces
    layers = len(rhos)
    N = layers + 1
    # includes upper and bottom phase as first and last layer. 
    rhos = np.hstack(([rho_0],rhos,[rho_N]))
    ds = np.hstack(([10000],ds,[10000]))
    # z0 is the position of each interface along z directoin.
    z0 = np.zeros(N)
    for i in range(layers): 
        # does not include bulk (ds[0],ds[-1])
        z0[i+1] = z0[i] + ds[i+1] 
    # z0[-1] is the sum of the thickness of all the layers.
    d_total = z0[-1]
    # the range of z is 4 times the thickness of the whole interface.
    z = np.arange(-d_total*2,4*d_total,6*d_total/1500) #length=1500 points.
    # calculate rho(z) (Wei, Journal of pyical chamistry B, 2014 Equation(1))
    rho = np.zeros(len(z))
    sqrt_2 = np.sqrt(2)
    for i in range(N):
        x = (z - z0[i])/(sqrt_2*roughness)
        rho = rho - (rhos[i]-rhos[i+1])*errFunction(x)
    rho = 0.5 * (rho + (rho_0+rho_N))
    
    out = np.vstack((z,rho))
    return out



def eDensity(solvent=(18,10),solute=[],mass_density=(1,0)):
    '''
    Parameters
    ----------
    solute: list of solvents with each component in the form of tuple containing
             molecular weight, electrons per molecule and concentration of that component
             e.g. 10e-4 DHDP (546.85,306,1e-4), 0.5M HEH[EHP] (306.4,170,0.5)...
             the mixture of DHDP and HEH[EHP]: [(546.85,306,1e-4),(306.4,170,0.5)]
             Note: concentration in unit of mole/L
    solvent: tuple of the molecular weight and electrons per molecule for the solvent.
            e.g. water (18,10), dodecane(170.34,98)
    mass_density: mass density of the solution and the uncertainty of the measurement , in g/ml
    
    Notes
    -----
    Calculation, multi-component solutions likewise
    rho_e = (Ne_solute + Ne_solvent)/V # Ne is the number of electrons in the solution
    Ne_solute = N_A * Cons * V * ne_solute # ne is the electrons per mlecule
    Ne_solvent = N_A * (mdens*V-cons*V*mwght1)/mwght2 * ne_solvent
    ==> rho_e = N_A*(cons*ne_solute+(mdens-cons*mwght1)/mwght2*ne_solvent)
    
    10e-4 DHDP in dodecane: -> 0.2596 A^-3
    eDensity(solvent=(170.34,98),solute=[(546.85,306,1e-4)],mass_density=(0.7495,0))
    3M HNO3 in water:  -> 0.3618 A^-3
    eDensity(solvent=(18,10),solute=[(63,32,3)],mass_density=(1.098,0)) 
    0.5M HEH[EHP] and 10mM Eu in dodecane:  -> 0.2672
    eDensity(solvent=(170.34,98),solute=[(306.4,170,0.5),(151.96,63,0.01)],mass_density=(0.7774,0))
    0.5M citrate in water:  -> 0.348
    eDensity(solvent=(18,10),solute=[(192.12,100,0.5)],mass_density=(1.047,0)) 
    Return
    ------
    eDensity: electron density of that solution, in A^-3
    '''
    mdens = uf(mass_density[0]*1e-24,mass_density[1]*1e-24)# convert to g/A^3
    # mdens = mass_density * 1e-24  # convert to g/A^3
    c_n = sum([k[1]*k[2]*1e-27 for k in solute])
    c_m = sum([k[0]*k[2]*1e-27 for k in solute])
    rho_e = N_A*(c_n + (mdens-c_m)/solvent[0]*solvent[1])
    return rho_e
    
     

def eDensitySolution(ne=10,r=0.097,C=1,V=None,flag=1):
    
     '''
     returns the electron density for a given aqueous solution.
     
     Parameters
     ----------
     ne: number of electrons for each salt "molecule"
     r: ionic radius in solution, see:
        "Marcus, Y. Ionic Radii in Aqueous Solutions. Chem. Rev. 1988, 88, 1475−1498"
     C: concentration of the solution(mol/L)
     rho_0: electron density of pure water.rho_0 = 0.33357A^-3
     rho_w: mass density of pure water. rho_w = 0.997g/ml
     rho_sol: electron density of the solution(A^-3)
     V: partial molor volume of the salt(ml)   
     N_A: Avogadro constant. 6.02E23   
     1 ml = 1E24 A^3, 1L = 1E27 A^3
    
     Note:
     -----
     Unit rule:
         volume: ml, electron density: A^-3
     Calculation are based on 1L of water solution. V is the partial volume for 1mol salt, 
     so the real partial volume is CV.
     
     Calculation of partial molar volume (in cm^-3):
         (for 1mole/L solution, sphere packed up)
         v = 2522.5*r^3 (J. Phys. Chem. B 2009, 113, 10285–10291)
         for ErBr3: v = 2522.5*(0.097^3+3*0.198^3) = 61.0441， consistant with Wei's result.
         for YCl3:  v = 2522.5*(0.097^3+3*0.180^3) = 46.4359
         for SrCl2  v = 2522.5*(0.125^3+2*0.180^3) = 34.3492, consistant with Wei's result.
         
     electron density of pure water for arbiturary volume V_0
         rho_0 = (rho_w*V_0/18) * N_A * 10  / V_0
               = rho_w*10/18 * N_A
               where 10 is the electron number for water molecule and 18 is the molar mass for water.

     the amount of electrons from water molecules are:
         N_water = (1000-V)*rho_w*10/18 * N_A 
     where 10 is the electron number for water molecule and 18 is the molar mass for water.

     the amount of electrons from salt are:
         N_salt = C*ne*N_A 

     for C mol/L solution:
         rho_sol = (N_water + N_salt) / 1E27
     plug the equation above you will get:
         rho_sol = rho_0 + (ne*N_A/1E27-V*rho_0/1000)*C
         
    Return
    ------
    eDensitySolution for flag:
    1: coeffecient for : rho_sol = rho_0 + coeffecient * C
    2: rho for solution: rho_sol
    3: mass density of water part
    4: partial molar volume for the specific ion (1M)
    
    For testing
    -----------
    V_Cl = eDensitySolution(r=0.180, flag=4)
    V_Y = eDensitySolution(r=0.097, flag=4)
    V_Sr = eDensitySolution(r=0.125,flag=4)
    V_NO3 = eDensitySolution(r=0.177, flag=4)
    V_Eu = eDensitySolution(r=0.106, flga=4)
    YCl3 = V_Y + 3*V_Cl  #--> 46.4359
    SrCl2 = V_Sr + 2*V_Cl #--> 34.3492
    Eu(NO3)3 = V_Eu + 3 * V_NO3 # --> 44.9679
    
    print eDensitySolution(ne=173,V=61.044, flag=1) #--> 0.08378 for ErBr3
    print eDensitySolution(ne=90,V=46.4359, flag=1) #--> 0.03869 for YCl3
    print eDensitySolution(ne=72,V=34.3492, flag=1) #--> 0.03189 for SrCl2
    print eDensitySolution(ne=156,V=44.9679, flag=1) #--> 0.0789 for Eu(NO3)3
    # edensity for 42mM Eu(NO3)3 is 0.33357 + 0.0789*0.042 = 0.33688
     '''
     rho_0 = 0.33357
      
     N_A = 6.02E23
     if V==None:
         V = 2522.5 * r**3 
     mdensity = (1000-V) * 0.997 / 1000
     coeff = ne*N_A/1E27 - V*rho_0/1000
     rho_sol = rho_0 + coeff * C
     if flag == 1:
         return coeff
     if flag == 2:
         return rho_sol
     if flag == 3:
         return mdensity
     if flag == 4:
         return V


def errFunction(x):
    '''
        Takes a one dimensional array, gives the error functoin of that array.
    numeric approximation comes from wiki, Abramowitz and Stegun. 
    (maximum erroe: 5e-4) (Tested)
    
    Parameters
    ----------
    x : array_like
        The source array
        
    See also
    --------
    http://en.wikipedia.org/wiki/Errorfunction#Approximation_with_elementary_functions
        
    Returns
    -------
    errFunction: ndarray
        The returned array has the same type as "a".
    
    Examples
    --------
        
    '''
    
    a1, a2, a3, a4 = 0.278393, 0.230389, 0.000972, 0.078108
    z = np.zeros(len(x))
    for i,t in enumerate(x):
        if t>0:
            y = 1 + a1*t + a2*t**2 + a3*t**3 + a4*t**4
            z[i] = 1 - 1/y**4
        elif t<0:
            y = 1 - a1*t + a2*t**2 - a3*t**3 + a4*t**4
            z[i] = 1/y**4 - 1
        else: z[i] = 0
    return z

    
def fresnel(q,qc):
    '''
        calculate fresnel reflectivity. (Tested)
    
    Parameters
    ----------
    q : array_like
        An array of Q's, usually [0,0.02,...,0.5]
    qc : floating number
        Critical angle
    
    Returns
    -------
    fresnel: an array containing the resnell reflectivity for each q value.
    '''
    q = q * (q>qc) + qc * (q<qc)
    fre = ((q-np.sqrt(q**2-qc**2))/(q+np.sqrt(q**2-qc**2)))**2
    return fre
    

class muElement():
    '''
    calculate the contribution of given element to mu(inverse of attenuation ) in water solution.
    
    Pamameters
    ----------
    rho_0: the mass density of simple substance of the element, can be found in the database
            in unit (g/cm^3)
    attenul: attenuation length of that element for rho_0 (and a given energy!)
            in unit micron(1 micron=1E-4cm)
    amass: atomic mass for that element
    concentr: concentration in water solution, it is 1M by default.
    
    Returns
    -------
    muElement: the contribution of that element 
    
    Note
    ----
    The mu, inverse attenuation length, is proportional to massdensity
    mu_0/rho_0 = mu_1/rho_1, thus mu_1 can be calculated
    
    For testing
    -----------
    Er = muElement(9.05, 21.71, 167.26)
    print "Er:\n", Er
    Y = muElement(4.46, 32.50, 88.906)
    print "Y:\n", Y
    Br = muElement(3.12, 59.76, 79.9, concentr=3)
    print "Br:\n", Br
    Cl = muElement(0.321E-2, 4.2142E5,35.453,concentr=3)
    print "Cl:\n", Cl
    print "mu for ErBr3: %6.2f" %(Er.mu+Br.mu) #--> mu for ErBr3:  21.37
    print "mu for ErCl3: %6.2f" %(Er.mu+Cl.mu) #--> mu for ErCl3:   9.30
    print "mu for YCl3: %6.2f:" %(Y.mu+Cl.mu)  #--> mu for YCl3:   6.921
    '''
    def __init__(self,rho_0,attenul,amass,concentr=1.):
        self.rho_0 = rho_0
        self.rho_1 = 0 # mass density in solution
        self.amass = amass
        self.mu_0 = 10000/attenul # conversion from micron^-1 to cm^-1
        self.mu = 0
        self.concentration = concentr
        self.rho_w = 0
        self.calculate()
    def __str__(self):
        print_str = \
        "atomic mass %6.2f,\
         \nRaw material: mass density %6.3fg/cm^3, mu %6.2fcm^-1, \
         \nCconcentration %4.2fM in water: mass density %6.3fg/cm^3, mu %6.2fcm^-1\n"\
          %(self.amass,self.rho_0,self.mu_0,self.concentration,self.rho_1,self.mu)
        return print_str
    def calculate(self):
        self.rho_1 = float(self.concentration)/1000 * self.amass 
        self.mu = self.mu_0 * (self.rho_1/self.rho_0)
        #self.rho_w = 


def penetrateDepth():
    '''
    pepetration depth in the aqueous phase, given by lmd(a)=1/[2k0*Im(sqrt(a**2-ac**2+2*i*bet))]
    '''
    pass


def roughness(t,gamma,kappa=1,Qz=0.5,db=0.67,r=4.8,qmax=1.2566,rho=1,flag=1):
    '''
        calculate the interfacial roughness using capillary wave theory.
    Paramerers
    ----------
    t: temperature, in C
    gamma: interfacial tension, in mN/m
    kappa: bending rigidity
    Qz: maximam Qz in reflectivity data, usually ~0.45 in inverse A.
    db: detector acceptence, in Rad. db=v3/L3, v3 is the vertical width of electronic
        slit, while L3 is the distance between sample and the detector. If flag=1,db 
        is in unit "mrad", for YAP detector, L3~670. For Pilatus1M detector, each
        pixel is 172um*172um, usually v3=0.172*11=1.892mm; for CCD detector, each
        picxel is 60um*60um, usually v3=0.06*31=1.86mm.
        L3 can be found in "SD Dist" under "Apex" tab in MW_XR software.
    r: average distance between molecules, r=4.8 for DHDP.
    qmax: defaul 2pi/5=1.2566 in Glenn's code, see more in eq1.26 in Mark's book
    rho: mass density difference between lower phase and upper fhase, in g/cm^3
         for system like 1E-7YCl3(water)/1E-4DHDP(dodecane), rho=1-0.78
    flag: choose which equation to use.
    Returns
    -------
    roughness:the interfacial roughness in A.
        flag = 1: reference equation(2) in J.Phys. Chem B 2014, 118, 10662-10674.
        flag = 2: reference eq 3.135 in Mark's book,and in Glenn's mathematica code.
        flag = 3: include kappa(bending regidity in the calculation)
        flag = 4: same as flag=3,except that quadratic term in the integrant is omitted...
    For testing
    -------
    rf = roughness(301-273.5,38,Qz=0.45,db=0.58e-3,r=4.8,flag=1) #->3.72, data in the reference, tested.
    r = roughness(25,51.5,Qz=0.25, db=0.6/676, rho=1-0.78,flag=2) #->3.4452, data in Glenn's code, tested.
    r = roughness(25,25.2,Qz=0.2, db=0.3/638, rho=1.203-1,flag=2) #->5.1466, nitrobenzene/water,tested.
    r = roughness(23.3,47.52,kappa=1,qmax=2*np.pi/8.9,Qz=0.5,db=0.8/672,rho=1.01,flag=3)
        #->3.0987, (3.0833 in Glenn's code:roughness_bending_rigidity.nb),tested.
    r = roughness(23.3,47.52,kappa=1,qmax=2*np.pi/8.9,Qz=0.5,db=0.8/672,rho=1.01,flag=4)
        #->3.3820, (3.2632 in Glenn's code:roughness_bending_rigidity.nb),tested.
    r = roughness(22.5,17.86,kappa=1,Qz=0.3,db=1.0/1695,r=4.8,rho=1.047-0.7774,flag=2)
    r = roughness(22,45.84,Qz=0.38,db=1.892/2745,flag=1) #->3.38, (0.5Mcitrate/dodecane)
    '''
    kBT = 1.38e-23 * (273.15+t) * 1e7 #1e7: convert from N*m into dyne*cm
    PI = np.pi # pi=3.1415926...
    qmax = 2*PI/5 # qmax = 2pi/5=1.2566... see more in eq 1.26 in Mark's book
    g = 981.0 # gravitational acceleration in cm/s^2
    qg = np.sqrt(g*rho/gamma)*1e-8 # inverse capillary length in A^-1
    C = kBT/(2*PI*gamma) * 1e16 # some coefficient; 1e16:convert cm^2 into A^2
    if flag==1:
        sigma_square = C * np.log(4/(Qz*db*r)) 
    elif flag==2:
        sigma_square = C * np.log(qmax/(Qz*db/4+np.sqrt(qg**2+(Qz*db/4)**2)))
    elif flag==3:
        q2 = gamma/kappa/kBT*1e-16 # in A^-2
        integrant = lambda q: q/(q**2+qg**2+q**4/q2)
        sigma_square = C * integrate.quad(integrant,Qz*db/2,qmax)[0] # quad returns a tuple: (result,error)
    elif flag==4:
        q2 = gamma/kappa/kBT*1e-16
        integrant = lambda q: q/(q**2+qg**2)
        sigma_square = C * integrate.quad(integrant,Qz*db/2,qmax)[0] # quad returns a tuple: (result,error)
    return np.sqrt(sigma_square)
 

def RRF(q, ref, err, q_off=0, qc=0.0103):
    ''' 
        Cauculate the ratio R/R_f for a given set of data. (Tested)
        
    Parameters
    ----------
    q : array_like
       An array of Q's, usually [0,0.02,...,0.5]
    q_off: floating number
        q offset. 
    qc : floating number
        Critical angle, is 0.0103 for water and dodecane interface.
    ref: array_like
        an array of raw reflectivity data for each q value.
    err: array_like
        an array of error for each raw reflectivity data
        
    Returns
    -------
    RRF: ndarray    
        Returns a 2-D array with rows: q+q_off, ref/frsnell, err/fresnell
        '''
    # convert input into nparray, q_off set included ->
    (q,ref,err) = map(np.array, (q+q_off,ref,err))
    #calculate fresnel reflectivity ->
    frs = fresnel(q,qc)
    # calculate the ratio for signal and error ->
    refFresnelRatio = np.divide(ref,frs)
    errFresnelRatio = np.divide(err,frs)
    # pack the data into 3 columns ->
    out = np.vstack((q,refFresnelRatio,errFresnelRatio))
    out = np.transpose(out)
    return out



def RtoRRf(openfile, q_off=0, qc=0.0103, save=None):
    '''
        Read reflectivity raw data from a file, and convert it to R/Rf. The
    return value of this function is optimized for saving the result directly
    into a file (see more in Reurns). 
    
    Parameters
    ----------
    openfile: the file containing the raw data
    q_off: q offset is zero if not specified.
    q_c: critical qz is 0.0103 if not specified.
    save: (if specified) the file to which converted data is saved.
    
    Returns
    -------
    convert: always return a 2-D array with columns 
             qz+q_off, R/Rf, err/Rf
    '''
    #load the raw reflectivity data ->
    ref_data = np.loadtxt(openfile)

    # split the raw data into three numpy arrays ->
    q = ref_data[:,0]
    ref = ref_data[:,1]
    err = ref_data[:,2]
    # calculate R/Rf, and transpose it into columns(q,ref,err) ->
    R_Rf = np.transpose(RRF(q,ref,err,q_off=q_off,qc=qc))
    print("data converted with q_off=%6.4f,qc=%6.4f" %(q_off,qc))
    # save R_Rf to file ->
    if save != None:
        np.savetxt(save, R_Rf,fmt="%.4f\t%.8f\t%.8f")
        print("Saved to file:", save)
    return R_Rf
  
  
def sldCalFun(d,y,sigma,x):
    pos=[]
    erfx=[]
    pos.append(0)
    erfx.append(x/sigma[0]/math.sqrt(2))
    for i in range(len(d)):
        pos.append(pos[i]+d[i])
        erfx.append((x-pos[i+1])/sigma[i+1]/math.sqrt(2))
    sld=0
    for i in range(len(sigma)):
        sld=sld+math.erf(erfx[i])*(y[i+1]-y[i])
    return (sld+y[0]+y[-1])/2


         
if __name__ == "__main__":
    

    
    
    