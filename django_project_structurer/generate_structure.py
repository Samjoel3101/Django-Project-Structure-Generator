from .file_handler.handle_by_string import HandleFileByString
from .file_handler.handle_by_tree import HandleFileByTree  
from .printer.string_printers import ImportStatementPrinter 
from .printer.tree_printers import * 
from .printer.core import Merger 

from pathlib import Path 
import re

class Generate_Structure:
    def __init__(self, filename, save_path, ext, handlers = [HandleFileByString, HandleFileByTree], 
                                                printers = [[ImportStatementPrinter], [MergePrinter]]):
        self.args = [Path(filename), save_path, ext]
        assert len(handlers) == len(printers)
        self.handlers = self._init_handlers(handlers) 
        self.printer = self._init_printers(printers)

    def _init_handlers(self, handlers):
        return [h(self.args[0]) for h in handlers]

    def _init_printers(self, printers):
        printers_ = []
        for idx, p_grps in enumerate(printers):
            printer_grp = []
            for p in p_grps:
                printer_grp.append(p(*self.args, self.handlers[idx]))
            printers_.append(printer_grp)
        printer = Merger(*self.args, None, printers = printers_)
        return printer 

    def print_info(self):
        self.printer.txt_writer()
    
    def content(self):
        return self.printer.content()

    def headers(self):
        headers = self.printer.headers()
        reg = r'\w+' 
        cleaned_headers = []
        for header in headers:
            cleaned_headers += [re.search(reg, header.strip()).group(0)] 
        return cleaned_headers

if __name__ == '__main__':
    filename = 'test_files/a.py'
    s = Generate_Structure(filename, ext = '.txt')
    s.print_info()
        