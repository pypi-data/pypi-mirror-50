"""magic to alert on fail or success"""
__version__ = '0.1'


import time
from IPython.core.magic import Magics, magics_class, cell_magic

@magics_class
class Exceptor(Magics):

    @cell_magic
    def exceptor(self, line, cell):
        timeout = 2
        try:
            start = time.time()
            self.shell.ex(cell)
        except:
            if time.time() - start > timeout:
                print("Slow fail!")
        else:
            if time.time() - start > timeout:
                print("done")

def load_ipython_extension(ipython):
    ipython.register_magics(Exceptor)
