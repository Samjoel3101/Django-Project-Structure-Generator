from file_handler.django.file_handler import UrlFileHandler 
from printer.django.printer import UrlPrinter 
from printer.core import Merger, lst_flatten, ContentMerger

from .generate_structure import Generate_Structure 
from . import config 

from pathlib import Path
import os

class Orchestrator:
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
        for django_type in config.DJANGO_FILENAMES:
            for filename in py_files:
                if django_type in filename:
                    filenames.append((filename, django_type))
        return filenames

class App_Structurer:
    def __init__(self, app_dir, save_path):
        self.orchestrator = Orchestrator(app_dir)
        self.save_path = save_path
        self.structurers = self.setup_structure_generators()

    def setup_structure_generators(self):
        structure_generators = []
        for django_file, django_type in self.orchestrator.django_files:
            handlers, printers = config.INFO_DICT[django_type]
            structure_generator = Generate_Structure(self.orchestrator.app_dir/django_file, None, '.txt', 
                                    handlers = lst_flatten(handlers), printers = [printers])
            structure_generators.append(structure_generator)
        return structure_generators

    def content(self):
        content = []
        for s in self.structurers:
            content += s.printer.content()
        return content 

    def print_info(self):
        app_dir = self.orchestrator.app_dir 
        merger = ContentMerger(None, self.save_path, '.txt', None, self.content, dir_name = 'ImageClassification')
        merger.txt_writer()
         