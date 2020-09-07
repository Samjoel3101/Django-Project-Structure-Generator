import inspect 
import re 
import ast 
from pathlib import Path 
from printer.tree_printers import ClassPrinter, FunctionPrinter, MergePrinter 
 
class HandleFileByTree:

    def __init__(self, filename):
        self.filename = Path(filename)
        self.functions, self.classes = self.get_members() 

    def get_members(self):
        with open(self.filename, 'r') as module:
            self.node = ast.parse(module.read())
        functions = [n for n in self.node.body if isinstance(n, ast.FunctionDef)]
        classes   = [n for n in self.node.body if isinstance(n, ast.ClassDef)] 
        return functions, classes 

if __name__ == '__main__':
    s = HandleFileByTree(filename)
    s.print_info(merge = True)
        
                