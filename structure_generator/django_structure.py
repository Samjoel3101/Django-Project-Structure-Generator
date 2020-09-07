from file_handler.django.file_handler import UrlFileHandler 
from printer.django.printer import UrlPrinter 
from printer.core import Merger 
from pathlib import Path
class DjangoStructureGenerator:
    def __init__(self, filename, save_path, ext, printers = [UrlPrinter]):
        self.args = [Path(filename), save_path, ext]
        self.django_handler = UrlFileHandler(filename)
        self.printer = self._init_printers(printers)
    
    def _init_printers(self, printers):
        printers = [printer(*self.args, self.django_handler) for printer in printers]
        printer = Merger(*self.args, None, printers = printers)
        return printer 

    def print_info(self):
        self.printer.txt_writer()