import ast
import re 

def P(pth):
    if '\\' in pth:
        return re.sub(r'\\', r'/', pth)
    return pth 

class Printer:  
    verbose_name = '_info'
    def __init__(self, filename, save_path, ext):
        self.save_path = save_path
        if save_path is not None:
            if not self.save_path.endswith('/' or '\\'):
                self.save_path += '/' if '/' in self.save_path else '\\'
        self.filename = filename 
        self.ext = ext
    
    def txt_writer(self): 
        raise NotImplementedError

    @property
    def path(self):
        if self.save_path is None:
            return self.parent + self.name
        return self.save_path 
            
    @property 
    def name(self): 
        name, _ = self.filename.name.split('.')
        return name + self.verbose_name + self.ext 
    
    @property
    def parent(self): return P(str(self.filename.parent)) + '/'

class ClassPrinter(Printer):
    verbose_name = '_class_info'
    def txt_writer(self, class_, reset = False):
        class_func_names = [o.name for o in class_.body if isinstance(o, ast.FunctionDef)]
        with open(self.path, 'w+') as info_file:
            info_file.write('Class Name: ' + class_.name + '\n')
            info_file.write('Function Name: \n')
            for name in class_func_names:
                info_file.write(f'\t{name}\n')

                       
                 