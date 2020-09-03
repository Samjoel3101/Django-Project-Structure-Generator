import inspect 
import re 
import ast 
from pathlib import Path 
from printers import ClassPrinter, FunctionPrinter
filename = 'test_files/a.py'
 
class StructureGenerator:

    def __init__(self, filename, save_path = None, ext = '.txt'):
        self.filename = Path(filename)
        self.ext = ext 
        self.save_path = save_path 
        self.class_printer = ClassPrinter(self.filename, self.save_path, self.ext) 
        self.func_printer  = FunctionPrinter(self.filename, self.save_path, self.ext) 
        self.get_members() 

    def get_members(self):
        with open(self.filename, 'r') as module:
            self.node = ast.parse(module.read())
        self.functions = [n for n in self.node.body if isinstance(n, ast.FunctionDef)]
        self.classes   = [n for n in self.node.body if isinstance(n, ast.ClassDef)] 
    
    def print_info(self):
        for class_ in self.classes:
            self.class_printer.txt_writer(class_)
        for func in self.functions:
            self.func_printer.txt_writer(func)

if __name__ == '__main__':
    s = StructureGenerator(filename)
    s.print_info()
        
                