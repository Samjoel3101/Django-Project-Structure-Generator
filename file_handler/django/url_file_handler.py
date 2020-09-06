from pathlib import Path 
import os 
import re 
import inspect 

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
        return '.'.join(self.dirs[1:])

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
                
     

if __name__ == '__main__':
    a = UrlFileHandler('D:\\Software Structure Generator\\test_files\\app\\api\\urls.py')
    print(a.extract_urls(), a.app_name, a.path_to_file)