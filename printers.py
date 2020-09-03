import ast
import re 
from pathlib import Path 
import numpy as np 

def P(pth):
    if '\\' in pth:
        return re.sub(r'\\', r'/', pth)
    return pth         

def lst_flatten(lst):
    l = []
    for i in lst:
        if isinstance(i, list):
            l += lst_flatten(i)
        else:
            l += [i]   
    return l 

def calculate_offset(lines_list):
    offset = 0
    for line in lines_list:
        offset += len(line) + 1
    return offset 

class Printer:  
    verbose_name = '_info'
    def __init__(self, filename, save_path, ext):
        self.save_path = save_path
        if save_path is not None:
            if not self.save_path.endswith('/' or '\\'):
                self.save_path += '/' if '/' in self.save_path else '\\'
        self.filename = filename 
        self.ext = ext
    
    def txt_writer(self, type_object, reset = False): 
        mode = 'w+' if not self.path.exists() else 'r+'
        prefix = '\n' if mode == 'r+' else ''
        with open(self.path, mode) as info_file:
            cursor = 0 if reset else calculate_offset(info_file.readlines())
            info_file.seek(cursor)
            info_file.write(prefix)
            info_file.writelines(lst_flatten(self.create_content(type_object)))
    
    def create_content(self): raise NotImplementedError

    @property
    def path(self):
        if self.save_path is None:
            return Path(self.parent + self.name)
        return Path(self.save_path) 
            
    @property 
    def name(self): 
        name, _ = self.filename.name.split('.')
        return name + self.verbose_name + self.ext 
    
    @property
    def parent(self): return P(str(self.filename.parent)) + '/'

class ClassPrinter(Printer):
    verbose_name = '_class_info'
    def __init__(self, filename, save_path, ext):
        super().__init__(filename, save_path, ext)
        self.func_printer = FunctionPrinter(filename, save_path, ext, new_file = False)
        
    def create_content(self, class_):
        content = [f'Class Name: {class_.name}\n']
        class_funcs = [o for o in class_.body if isinstance(o, ast.FunctionDef)]
        for func in class_funcs:
            content.append(self.func_printer.create_content(func))
        return content  
                
class FunctionPrinter(Printer):
    verbose_name = '_function_info'
    def __init__(self, filename, save_path, ext, new_file = True):
        super().__init__(filename, save_path, ext)
        self.new_file = new_file
        self.prefix = '\t' if not self.new_file else ''
        self.suffix = '\n' 

    def create_content(self, func): 
        content = [f'Function Name: {func.name}'] 
        for arg in func.args.args:
            content.append(f'\tParameter Name: {arg.arg}')
        return [self.prefix + o + self.suffix for o in content] 

if __name__ == '__main__':
    lt = [1, 2, 3, 4, [5, 6,[[7], 8]], [5, 6, 7, 8]]
    print(lst_flatten(lt))

                       
                 