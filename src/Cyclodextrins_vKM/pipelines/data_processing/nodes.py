import autode as ade
orca = ade.methods.ORCA()
import numpy as np

def ConvertMol(x):
    Solvent = input('If you got a solvent give us the name here if not just hit enter: ')
    Name = input('Give a name for the file ending in .xyz: ')
    Charge = input('Specify charge of the molecule: ')

    Charge = int(Charge)

    if Solvent == '':
        Solvent = None
    xnew = x.decode("utf-8")

    with open(Name,'w') as XYZfile:
        XYZfile.write(xnew)

    MoI = ade.Molecule(Name, solvent_name=Solvent, charge=Charge)

    XYZfile.close()

    ade.methods.get_lmethod()
    ade.methods.get_hmethod()

    return(MoI)

def OptimizeMol(MoI):
    print(MoI)
    MoI.optimise(method=ade.methods.XTB())
    return(MoI)

def CalculateMol(MoI):
    NoC = input('How many cores do you have/want to use if you only have 1 hit enter: ')
    if NoC == '':
        NoC = 1
    CoI = ade.Calculation(name=MoI.name,molecule=MoI,method=orca,keywords=orca.keywords.hess,n_cores=NoC)
    CoI.output.filename = MoI.name+'.out'
    return(CoI)

def GetGibbsMol(MoI,CoI):
    MoI.calc_thermo(calc=CoI)
    print(f'G = {MoI.free_energy:.6f} Ha')
    GibbsE = MoI.free_energy
    return(GibbsE)

def GetDeltGibbs(GibbsE1, GibbsE2):
    DeltGibbs = np.abs(GibbsE1 - GibbsE2)
    return(DeltGibbs)

def GetPka(DeltGibbsE):
    DeltGibbsEkJpM = 2600*DeltGibbsE
    R = 0.008314
    T = input("What's the Temperature(if you give nothing it will be 273.15K): ")
    if T == '':
        T = 273.15
    LnK = DeltGibbsEkJpM/(-1*R*T)
    K = np.exp(LnK)
    pKa = -1*np.log10(K)
    print(f'pKa = {pKa}')
    return(pKa)