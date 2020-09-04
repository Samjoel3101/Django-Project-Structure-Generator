from file_handler.handle_by_string import HandleFileByString
from file_handler.handle_by_tree import HandleFileByTree  
from printer.string_printers import ImportStatementPrinter 
from printer.tree_printers import * 
from printer.core import Merger 

from pathlib import Path 

class Generate_Structure:
    def __init__(self, filename, save_path, ext, printers = [[ImportStatementPrinter], [MergePrinter]]):
        self.args = [Path(filename), save_path, ext]
        self.string_handler = HandleFileByString(filename)
        self.tree_handler = HandleFileByTree(filename)
        self.printer = self._init_printers(printers)
    
    def _init_printers(self, printers):
        string_printers, tree_printers = printers 
        string_printers = [p(*self.args, self.string_handler) for p in string_printers]
        tree_printers = [p(*self.args, self.tree_handler) for p in tree_printers]
        printer = Merger(*self.args, None, printers = [string_printers, tree_printers])
        return printer 

    def print_info(self):
        self.printer.txt_writer()

if __name__ == '__main__':
    filename = 'test_files/a.py'
    s = Generate_Structure(filename, ext = '.txt')
    s.print_info()
        