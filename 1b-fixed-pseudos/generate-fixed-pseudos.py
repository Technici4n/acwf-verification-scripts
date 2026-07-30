from aiida_pseudo.data.pseudo import UpfData
from aiida_pseudo.groups.family import CutoffsPseudoPotentialFamily
import os
from pathlib import Path
import shutil
import tarfile
import tomllib
import urllib.request as ureq

URL_v0_5_1_FIX = r"https://github.com/JuliaMolSim/PseudoLibrary/releases/download/v0.2.1/dojo.nc.sr.pbe.v0_5_1-fix.standard.upf.tar.gz"
URL_v0_4_1 = r"https://github.com/JuliaMolSim/PseudoLibrary/releases/download/v0.2.1/dojo.nc.sr.pbe.v0_4_1.standard.upf.tar.gz"

tar_v0_5_1_fix = Path("dojo-v0_5_1-fix.tar.gz")
tar_v0_4_1 = Path("dojo-v0_4_1.tar.gz")
path_v0_5_1_fix = Path("dojo-v0_5_1-fix")
path_v0_4_1 = Path("dojo-v0_4_1")

ureq.urlretrieve(URL_v0_5_1_FIX, tar_v0_5_1_fix)
ureq.urlretrieve(URL_v0_4_1, tar_v0_4_1)

with tarfile.open(tar_v0_5_1_fix, "r:gz") as f:
    f.extractall(path_v0_5_1_fix)
with tarfile.open(tar_v0_4_1, "r:gz") as f:
    f.extractall(path_v0_4_1)

elements = [f[:-len(".upf")] for f in os.listdir(path_v0_5_1_fix) if f.endswith(".upf")]
print(f"Found {len(elements)} elements")

recommended_cutoffs = {}
HINTS = ["low", "normal", "high"]
for hint in HINTS:
    rec = {}
    for el in elements:
        fix_file = path_v0_5_1_fix / f"{el}.toml"
        extra_ecut = 0
        with open(fix_file) as f:
            if f"cutoffs_{hint}" not in f.read():
                fix_file = path_v0_4_1 / f"{el}.toml"
                extra_ecut = 20
        with open(fix_file, "rb") as f:
            toml_data = tomllib.load(f)
        recommended_ecut = (toml_data[f"cutoffs_{hint}"]["Ecut"] + extra_ecut)
        rec[el] = {
                "cutoff_wfc": recommended_ecut,
                "cutoff_rho": recommended_ecut * 4,
        }
    recommended_cutoffs[hint] = rec

# Remove toml files
for el in elements:
    (path_v0_5_1_fix / f"{el}.toml").unlink()

family = CutoffsPseudoPotentialFamily.create_from_folder(path_v0_5_1_fix, "PseudoDojo/0.5.1-fix/PBE/SR/standard/upf", pseudo_type=UpfData)

for k, v in recommended_cutoffs.items():
    family.set_cutoffs(v, k, unit="Eh")

tar_v0_5_1_fix.unlink()
tar_v0_4_1.unlink()
shutil.rmtree(path_v0_5_1_fix)
shutil.rmtree(path_v0_4_1)
