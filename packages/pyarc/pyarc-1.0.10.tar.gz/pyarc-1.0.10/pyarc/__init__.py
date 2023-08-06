from .CBA import *
from .data_structures import TransactionDB

try:
    import fim
except ModuleNotFoundError:
    raise Exception("Before using pyARC, the fim package must be installed first." + 
    " For installation guide, refer to http://www.borgelt.net/pyfim.html")
