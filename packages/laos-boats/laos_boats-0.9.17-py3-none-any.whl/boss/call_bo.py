from .bo import BoMain
from .io import Settings
from .utils import Timer

def call_bo(f, bounds, **kwargs):


    timer = Timer()
    settings = Settings(None, timer, arg_keywds=kwargs) 

    out = None
    rst = None
    
    bo = BoMain(settings, out, rst)

    bo.run_optimization()

    return bo.convergence
