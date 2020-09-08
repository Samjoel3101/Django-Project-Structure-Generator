import ast
import re 
from pathlib import Path 
import numpy as np 
from . import styles
import os

def P(pth):
    if '\\' in pth:
        return re.sub(r'\\', r'/', pth)
    return pth         

def get_dir_name(path):
    path = str(path)
    valid_splitters = ['/', '\\']
    for splitter in valid_splitters:
        if splitter in path:
            return path.split(splitter)[-1]
    raise ValueError(f'This is not a Valid Path {path}')
    
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
    def __init__(self, filename, save_path, ext, handler, style = styles.default, **kwargs):
        self.save_path = str(save_path)
        if save_path is not None:
            if not self.save_path.endswith('/'):
                self.save_path += '/' if '/' in self.save_path else '\\'
                self.save_path = Path(self.save_path)
        self.filename = filename 
        self.ext = ext
        if handler is not None:
            self.handler = handler 
        self.style = style
        self.set_styles()
        self.kwargs = kwargs
        self.set_from_kwargs()

    def txt_writer(self, reset = False, *args, **kwargs): 
        mode = 'w+' if not self.path.exists() else 'r+'
        prefix = '\n' if mode == 'r+' else ''
        with open(self.path, mode) as info_file:
            cursor = 0 if reset else calculate_offset(info_file.readlines())
            info_file.seek(cursor)
            info_file.write(prefix)
            info_file.writelines(lst_flatten(self.content(*args, **kwargs)))
    
    def create_content(self, *args, **kwargs): raise NotImplementedError

    def content(self, content):
        content =  [self.prefix + c + self.suffix for c in lst_flatten(content)] 
        content = self.header + content if self.header else content 
        return [self.content_prefix] + content + [self.content_suffix]
    
    @property
    def path(self):
        if self.save_path is None:
            return Path(self.parent + self.name)
        if os.path.isdir(self.save_path):
            dir_name = get_dir_name(self.save_path)
            filename = dir_name + self.verbose_name + self.ext 
            return self.save_path/filename 
                
        return Path(self.save_path) 
            
    @property 
    def name(self): 
        name, _ = self.filename.name.split('.')
        return name + self.verbose_name + self.ext 
    
    @property
    def parent(self): return P(str(self.filename.parent)) + '/'

    @property 
    def header(self):
        name = re.sub('(Inline)?(Printer)?', '', self.__class__.__name__)
        if hasattr(self, 'custom_header'):
            name = self.custom_header
        return [f"{self.header_prefix} {name} {self.header_suffix}\n"]

    def set_styles(self):
        for style in self.style:
            setattr(self, style, self.style[style])

    def set_from_kwargs(self):
        for attr_name, value in self.kwargs.items():
            setattr(self, attr_name, value)

class Merger(Printer):
    verbose_name = '_info'
    def __init__(self, filename, save_path, ext, handler, printers):
        super().__init__(filename, save_path, ext, handler)
        self.printers = printers 

    def content(self):
        content = []
        for printer in lst_flatten(self.printers):
            content += printer.content() 
        return content

class ContentMerger(Printer):
    verbose_name = '_app_info'
    def __init__(self, filename, save_path, ext, handler, content):
        super().__init__(filename, save_path, ext, handler)
        self.content = content 

    def content(self):
        return self.content
if __name__ == '__main__':
    lt = [1, 2, 3, 4, [5, 6,[[7], 8]], [5, 6, 7, 8]]
    print(lst_flatten(lt))

                       
                 