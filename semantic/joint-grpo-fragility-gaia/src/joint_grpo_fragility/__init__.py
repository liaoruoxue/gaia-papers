import sys, os, importlib
_here = os.path.dirname(os.path.abspath(__file__))
_semantic = os.path.abspath(os.path.join(_here, "..", "..", ".."))
for dep in ("2602-00994-gaia", "2604-06159-gaia", "2604-23747-gaia"):
    p = os.path.join(_semantic, dep, "src")
    if p not in sys.path and os.path.isdir(p):
        sys.path.insert(0, p)

for pkg in ("2602_00994", "2604_06159", "2604_23747"):
    for sub in ("motivation", "priors"):
        importlib.import_module(f"{pkg}.{sub}")

from . import claims, priors
__all__ = ["claims", "priors"]
