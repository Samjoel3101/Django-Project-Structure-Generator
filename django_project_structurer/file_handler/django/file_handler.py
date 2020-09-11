import os 
import re 
import inspect 
from pathlib import Path 
from typing import Iterable 

from ..handle_by_string import HandleFileByString, HandleFileByRegex
from ..handle_by_tree import HandleFileByTree, ClassAttributeVisitor


class DjangoFileHandler:
    def __init__(self, filename):
        self.filename = Path(filename)
        self.dirs = []
        self._get_app_name(self.filename)
        self.__class__.extract_get_methods(self)
        
    @classmethod 
    def extract_get_methods(cls, objct):
        for method_name, obj in inspect.getmembers(cls):
            if method_name.startswith('get'):
                obj(objct)                 

    @property
    def parent_path(self):
        return f'{self.app_name}.urls'
    
    def _store_dir(self, path):
         self.dirs.append(path.name) 

    def _get_app_name(self, filename):
        parent = []
        if os.path.isdir(filename.parent):
            if (filename.parent/'__init__.py').exists():
                parent += self._get_app_name(filename.parent)
                self._store_dir(filename.parent)
            else:
                parent += [filename.name] 
        return parent

    @property 
    def app_name(self):
        return self.dirs[-1]
    
    @property 
    def path_to_file(self):
        return '.'.join(self.dirs[1:] + [self.name])
    
    @property 
    def name(self):
        name = (self.filename.name).split('.')
        return name[0]

class UrlFileHandler(DjangoFileHandler):

    def get_urls(self):
        with open(self.filename, 'r') as f:
            urls = self._extract_url(f.readlines())
        self.urls = urls 

    def _extract_url(self, lines):
        urls = []
        name_reg = r"name = ['a-zA-Z0-9_]+"
        url_reg  = r"((<)?[a-zA-Z0-9:/_-]+(>)?/(\w+)?)+" #r"(\w+/)+((<)?[a-zA-Z0-9:/_-]+(>)?)+"
        for line in lines: 
            line = line.strip()
            if line.startswith('path') or line.startswith('re_path'):
                name = re.search(name_reg, line)
                url = re.search(url_reg, line)
                url = url.group(0) if url else '/'
                name = re.sub("'", "", name.group(0)) if name else 'name = name not provided'
                urls.append((url, name))
        return urls 
                
class ModelFileHandler(DjangoFileHandler):
       
    def get_class_attributes(self):
        classes = []
        handler = HandleFileByTree(self.filename)
        for class_ in handler.classes:
            class_attributes = ClassAttributeVisitor(class_).class_attrs
            classes.append([class_.name, class_attributes])
        self.class_attrs = classes
    
    def get_signals_used(self):
        signal_func_re = r'[a-z_]+,'
        sender_re = r'sender = \w+'
        signals_used = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                if line.startswith('pre') or line.startswith('post'):
                    signal_func = re.search(signal_func_re, line)
                    sender = re.search(sender_re, line)
                    signals_used.append((signal_func.group(0), sender.group(0)))
        self.signals_used = signals_used 
     

if __name__ == '__main__':
    a = ModelFileHandler('D:\\Software Structure Generator\\test_files\\app\\api\\models.py')
    print(a.class_attrs)


