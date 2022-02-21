from unicodedata import name
from black import out
from kedro.pipeline import Pipeline, node
from .nodes import ConvertMol1, OptimizeMol1, CalculateMol1, GetGibbsMol1,ConvertMol2, OptimizeMol2, CalculateMol2, GetGibbsMol2, GetDeltGibbs, GetPka
def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(func=ConvertMol1, inputs='aBiCyDNH_xyz', outputs='Molecule1', name='Create_Molecule1'),
            node(func=OptimizeMol1, inputs='Molecule1', outputs='Molecule_opt1', name='Optmize_Molecule1'),
            node(func=CalculateMol1, inputs='Molecule_opt1', outputs='Calculation1',name='Single_Point_Calc1'),
            node(func=GetGibbsMol1, inputs=['Molecule_opt1','Calculation1'], outputs='GibbsE1', name='Get_Gibbs1'),
            node(func=ConvertMol2, inputs='aBiCyDNH2_xyz', outputs='Molecule2', name='Create_Molecule2'),
            node(func=OptimizeMol2, inputs='Molecule2', outputs='Molecule_opt2', name='Optimize_Molecule2'),
            node(func=CalculateMol2, inputs='Molecule_opt2', outputs='Calculation2', name='Single_Point_Calc2'),
            node(func=GetGibbsMol2, inputs=['Molecule_opt2','Calculation2'], outputs='GibbsE2', name='Get_Gibbs2'),
            node(func=GetDeltGibbs, inputs=['GibbsE1', 'GibbsE2'], outputs='DeltGibbs', name='Get_DeltGibbs'),
            node(func=GetPka, inputs='DeltGibbs', outputs='pKa',name='Get_pKa')
        ]
    )