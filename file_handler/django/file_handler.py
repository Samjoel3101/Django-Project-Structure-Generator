from pathlib import Path 
import os 
import re 
import inspect 
import importlib 
from ..handle_by_string import HandleFileByString, HandleFileByRegex
from ..handle_by_tree import HandleFileByTree 
from typing import Iterable

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
        url_reg  = r"(\w+/)+((<)?[a-zA-Z0-9:/_-]+(>)?)+"
        for line in lines: 
            line = line.strip()
            if line.startswith('path') or line.startswith('re_path'):
                name = re.search(name_reg, line)
                url = re.search(url_reg, line)
                urls.append((url.group(0), re.sub("'", "", name.group(0))))
        return urls 
                
class ModelFileHandler(DjangoFileHandler):
       
    def get_class_attributes(self):
        classes = []
        handler = HandleFileByTree(self.filename)
        for class_ in handler.classes:
            model_class = getattr(importlib.import_module(self.path_to_file), class_.name)
            class_attrs =  self._extract_class_attrs(model_class)
            class_asc   =  self._extract_associations(model_class, class_attrs)
            assert len(class_asc) == len(class_attrs)
            classes.append([class_.name, [[a, asc] for a, asc in zip(class_attrs, class_asc)]])
        self.class_attrs = classes

    def _extract_associations(self, model, attr_list):
        associations = []
        for a in attr_list:
            attr = getattr(model, a)
            if inspect.isclass(type(attr)):
                name = attr.__class__.__name__ + '(Class)' 
                associations.append(name)
        return associations

    def _extract_class_attrs(self, clas):
        class_attrs = []
        for attr in dir(clas):
            if not callable(getattr(clas, attr)):
                if not attr.startswith('__') and not attr.startswith('_'):
                    class_attrs.append(attr) 
        return class_attrs
    
    def get_signals_used(self):
        signal_func_re = r'[a-z_],'
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


