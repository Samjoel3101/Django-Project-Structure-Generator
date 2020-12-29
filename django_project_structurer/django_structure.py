from .file_handler.django.file_handler import UrlFileHandler 
from .printer.django.printer import UrlPrinter 
from .printer.core import Merger, lst_flatten, ContentMerger, DummyPrinter

from .generate_structure import Generate_Structure 
from . import config 

from pathlib import Path
import os

ORDER = ['Urls', 'Models', 'Signals', 'Forms', 'Mixins']
API_ORDER = ['Urls', 'Serializers']

class Orchestrator:
    file_config = config.DJANGO_FILENAMES

    def __init__(self, app_dir):
        self.app_dir = Path(app_dir)
        self.django_files = self.get_files()
    
    def get_files(self):
        files = os.listdir(self.app_dir)
        files = self._get_py_files(files)
        files = self._get_django_files(files)
        return files 

    def _get_py_files(self, files):
        py_files = []
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__'):
                py_files.append(filename)
        return py_files 
    
    def _get_django_files(self, py_files):
        filenames = []
        for django_type in self.file_config:
            for filename in py_files:
                if django_type in filename:
                    filenames.append((filename, django_type))
        return filenames
    
    @property 
    def app_name(self):
        app_dir = str(self.app_dir)
        if '/' in app_dir:
            dirs = app_dir.split('/')
        elif '\\' in app_dir:
            dirs = app_dir.split('\\')
        return dirs[-1]

class ApiOrchestrator(Orchestrator):
    file_config = config.API_FILENAMES 

    @property 
    def app_name(self):
        app_name = self.app_dir.name 
        if str(app_name) == 'api' and (self.app_dir.parent/'__init__.py').exists():
            return str(self.app_dir.parent.name)
        else:
            return str(self.app_dir.name)

class App_Structurer:
    orc = Orchestrator
    ref_dict = config.INFO_DICT
    order = ORDER 

    def __init__(self, app_dir, save_path):
        self.orchestrator = self.orc(app_dir)
        self.save_path = save_path
        self.structurers = self.setup_structure_generators()
        self.printers = self._align_printers()

    def setup_structure_generators(self):
        structure_generators = []
        for django_file, django_type in self.orchestrator.django_files:
            handlers, printers = self.ref_dict[django_type]
            structure_generator = Generate_Structure(self.orchestrator.app_dir/django_file, None, '.txt', 
                                    handlers = lst_flatten(handlers), printers = [printers])
            structure_generators.append(structure_generator)
        return structure_generators

    def content(self):
        content = self.header
        for printer in self.printers:
            content += printer.content()
        return content 
    
    def _align_printers(self):
        headers = {}; header_names = []
        for struct in self.structurers:
            header_names += struct.headers()
            headers[struct.headers()[0]] = struct.printer
        missing = self._set_dummy_for_missing([n for n in self.order if n not in header_names])
        headers.update(missing)
        aligned_printers = []
        for key in self.order:
            aligned_printers.append(headers[key])
        return aligned_printers 

    def _set_dummy_for_missing(self, missing):
        return dict(zip([m for m in missing], [DummyPrinter(None, None, '.txt', None, custom_header = m) for m in missing]) )
 
    def print_info(self):
        merger = ContentMerger(None, self.save_path, '.txt', None, self.content, dir_name = self.orchestrator.app_name)
        merger.txt_writer()
    
    @property 
    def header(self):
        name = self.orchestrator.app_name
        return [f'##APP NAME::{name}\n']
        
class ApiStructurer(App_Structurer):
    orc = ApiOrchestrator 
    ref_dict = config.API_DICT
    order = API_ORDER

class DjangoProjectStructurer:
    structurer = App_Structurer
    def __init__(self, project_dir, save_path):
        self.project_dir = Path(project_dir) 
        self.save_path = save_path 
        self.app_dirs    = self._get_app_dirs()
        if len(self.app_dirs) == 0:
            print('No app dirs found pls check your dir path')
        self.app_structs = self._setup_app_structurers()

    def _get_app_dirs(self):
        app_dirs = []
        for filename in os.listdir(self.project_dir):
            path = self.project_dir/filename
            if os.path.isdir(path) and (path/'__init__.py').exists():         
                if 'api' not in str(path):
                    app_dirs.append(path) 
        return app_dirs
    
    def _setup_app_structurers(self):
        app_structurers = []
        for app_dir in self.app_dirs:
            app_struct = self.structurer(app_dir, self.save_path)
            app_structurers.append(app_struct)
        return app_structurers

    def content(self):
        content = []
        for struct in self.app_structs:
            content += struct.content() 
        return content 
    
    def generate_project_info(self):
        merger = ContentMerger(None, self.save_path, '.txt', None, self.content, dir_name = self.project_dir.name)
        merger.txt_writer()

class DjangoApiStructurer(DjangoProjectStructurer):
    structurer = ApiStructurer

    def _get_app_dirs(self):
        api_dir = []
        app_dirs = super()._get_app_dirs()
        for app_dir in app_dirs:
            for filename in os.listdir(app_dir):
                path = app_dir/filename 
                if os.path.isdir(path) and 'api' in filename:
                    api_dir.append(path)
        return api_dir 

