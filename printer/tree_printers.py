from .core import * 

__all__ = ['ClassPrinter', 'FunctionPrinter', 'MergePrinter']

class ClassPrinter(Printer):
    verbose_name = '_class_info'
    def __init__(self, filename, save_path, ext, handler):
        self.args = (filename, save_path, ext, handler)
        super().__init__(*self.args)
        self.func_printer = FunctionPrinter(*self.args, new_file = False)
        
    def create_content(self, class_):
        content = [f'Class Name: {class_.name}\n']
        class_funcs = [o for o in class_.body if isinstance(o, ast.FunctionDef)]
        for func in class_funcs:
            content.append(self.func_printer.create_content(func))
        return content
    
    def content(self):
        content = []
        for clas in self.handler.classes:
            content += self.create_content(clas) 
        return self.header + content
                
class FunctionPrinter(Printer):
    verbose_name = '_function_info'
    def __init__(self, filename, save_path, ext, handler, new_file = True):
        super().__init__(filename, save_path, ext, handler)
        self.new_file = new_file
        self.prefix = '\t' if not self.new_file else ''
        self.suffix = '\n' 

    def create_content(self, func): 
        content = [f'Function Name: {func.name}'] 
        for arg in func.args.args:
            content.append(f'\tParameter Name: {arg.arg}')
        return [self.prefix + o + self.suffix for o in content]
    
    def content(self):
        content = []
        for func in self.handler.functions:
            content += self.create_content(func)
        return self.header + content  

class MergePrinter(Printer):
    verbose_name = '_info'
    def __init__(self, filename, save_path, ext, handler, printers = None):
        self.args = (filename, save_path, ext, handler)
        super().__init__(*self.args)
        if printers is None:
            self.clas_printer = ClassPrinter(*self.args)
            self.func_printer = FunctionPrinter(*self.args)
        else:
            self.clas_printer, self.func_printer = printers 

    def create_content(self, classes, functions):
        class_contents = []; func_contents = []
        for clas in classes:        
            class_contents += self.clas_printer.create_content(clas) + ['\n']
        for func in functions:
            func_contents += self.func_printer.create_content(func) + ['\n']
        return class_contents ,func_contents
    
    def content(self):
        class_contents = self.clas_printer.header 
        func_contents  = self.func_printer.header 
        content1, content2 = self.create_content(self.handler.classes, self.handler.functions)
        class_contents += content1; func_contents += content2 
        return class_contents + func_contents
