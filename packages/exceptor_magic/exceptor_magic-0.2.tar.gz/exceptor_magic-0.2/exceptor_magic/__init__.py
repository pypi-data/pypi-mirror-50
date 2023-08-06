"""magic to alert on fail or success"""
__version__ = '0.2'


from durbango.send_sms import send_sms
import time
from IPython.core.magic import Magics, magics_class, cell_magic

@magics_class
class Exceptor(Magics):

    @cell_magic
    def exceptor(self, line, cell):
        timeout = 60
        try:
            start = time.time()
            self.shell.ex(cell)
        except:
            if time.time() - start > timeout:
                send_sms("Slow fail!")
        else:
            if time.time() - start > timeout:
                send_sms("done")

def load_ipython_extension(ipython):
    ipython.register_magics(Exceptor)
