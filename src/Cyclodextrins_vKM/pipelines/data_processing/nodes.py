from ast import Mult
import autode as ade
orca = ade.methods.ORCA()
import numpy as np

def ConvertMol(x):
    Solvent = input('If you got a solvent give us the name here if not just hit enter: ') # configure Solvent
    Name = input('Give a name for the file ending in .xyz: ') # configure name of .xyz file
    Charge = input('Specify charge of the molecule: ') # configure charge
    Multiplicity = input('Specify multiplicity of molecule (if not given it will be 1): ') # configure multiplicity

    if Multiplicity == '':
        Multiplicity = 1
    # make sure that the inputs that need to be integers are integers
    Charge = int(Charge)
    Multiplicity = int(Multiplicity)
    # adjust solvent 
    if Solvent == '':
        Solvent = None
    # decode input file from utf-8 to string
    xnew = x.decode("utf-8")
    # open and write .xyz file with the decoded input
    with open(Name,'w') as XYZfile:
        XYZfile.write(xnew)
    # create molecule
    MoI = ade.Molecule(Name, solvent_name=Solvent, charge=Charge, mult=Multiplicity)
    # close .xyz file
    XYZfile.close()

    return(MoI)
# optimize the molecular structure method can be changed
def OptimizeMol(MoI):
    print(MoI)
    MoI.optimise(method=ade.methods.XTB())
    return(MoI)
# Run Calculation, specify the number of cores for the calculation, and output calculation to files
def CalculateMol(MoI):
    NoC = input('How many cores do you have/want to use if you only have 1 hit enter: ')
    if NoC == '':
        NoC = 1
    CoI = ade.Calculation(name=MoI.name,molecule=MoI,method=orca,keywords=orca.keywords.hess,n_cores=NoC)
    CoI.output.filename = MoI.name+'.out'
    return(CoI)
# get Gibbs free energy using the calc_thermo property
def GetGibbsMol(MoI,CoI):
    NoC = input('How many cores do you have/want to use if you only have 1 hit enter: ')
    if NoC == '':
        NoC = 1
    MoI.calc_thermo(calc=CoI, n_cores=NoC)
    print(f'G = {MoI.free_energy:.6f} Ha')
    GibbsE = MoI.free_energy
    return(GibbsE)
# get delta gibbs free energy
def GetDeltGibbs(GibbsE1, GibbsE2):
    DeltGibbs = np.abs(GibbsE1 - GibbsE2)
    print(DeltGibbs)
    return(DeltGibbs)
# get pKa (there is an error here so result calculation will be done manually)
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