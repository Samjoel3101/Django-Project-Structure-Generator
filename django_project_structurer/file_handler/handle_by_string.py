import re 
import os 
from pathlib import Path 

class HandleFileByString:

    def __init__(self, filename):
        self.filename = Path(filename) 
        self.import_modules, self.from_modules  = self.get_import_statements() 

    def get_import_statements(self):
        with open(self.filename, 'r') as f:
            import_statements, from_statements = self.extract_import_statements(f.readlines())
        return import_statements, from_statements
    
    def _get_from_parent(self, module_name):
        if module_name.startswith('.'):
            module_name = f'{self.parent_package}.{module_name[1:]}'
        return module_name 

    def extract_import_statements(self, lines):
        import_lines = []; from_lines = []
        for line in lines:
            split = line.strip().split()
            if line.startswith('import'):
                import_lines.append(split[1])
            if line.startswith('from'):
                from_lines.append((self._get_from_parent(split[1]), split[3]))
        return import_lines, from_lines  

    def _check_parent_package(self):
        parent_dir = self.filename.parent 
        if (parent_dir/'__init__.py').exists():
            return parent_dir  
        else:
            raise ValueError(f'The {parent_dir} directory is not a python package, So . import statements are invalid')
                                         
    @property 
    def parent_package(self):
        return self._check_parent_package().name   

class HandleFileByRegex:
    def __init__(self, filename, regex):
        self.filename = Path(filename)
        self.regex = regex
        self.contents = self.get_contents()
         
    def get_contents(self):
        results = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                result = self._search(line)
                if result is not None:
                    results.append(result.group(0))
        return results 
        
    def _search(self, line):
        match = re.search(self.regex, line)
        return match 


if __name__ == '__main__':
    filename = 'test_files/c.py'
    h = HandleFileByRegex(filename)
    print(h.import_modules, h.from_modules)