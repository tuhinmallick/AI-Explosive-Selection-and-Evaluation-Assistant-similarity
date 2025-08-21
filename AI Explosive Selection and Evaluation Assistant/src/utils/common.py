import os
class Paths:
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATA = os.path.join(ROOT, "data")
    REPORTS = os.path.join(ROOT, "reports")
def ensure_dirs():
    os.makedirs(Paths.DATA, exist_ok=True); os.makedirs(Paths.REPORTS, exist_ok=True)
