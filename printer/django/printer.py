from printer.core import Printer
from functools import partial  

class UrlPrinter(Printer):
    verbose_name = '_url_info'
    def create_content(self, url_tup, parent_path = None):
        url, name = url_tup 
        content = parent_path + [f'{url}\t\t{name}\n']
        return content 

    def content(self, *args, **kwargs):
        content = []
        for url_tup in self.handler.urls:
            content += self.create_content(url_tup, *args, **kwargs)
        return super().content(content) 
        
class ModelPrinter(Printer):
    verbose_name = '_model_info'
    def create_content(self, attr_list):
        content = ['\tFields Defined\n']
        for attr, value in attr_list:
            content += [f'\t\t{attr} -> {value}\n']
        return content 

    def content(self):
        content = []
        for model_name, attr_list in self.handler.class_attrs:
            content += [f'{model_name}\n']
            content += self.create_content(attr_list)    
        return super().content(content)

class ModelInlinePrinter(ModelPrinter):
    def create_content(self, attr_list):
        return [] 

ModelInlinePrinter = partial(ModelInlinePrinter, prefix = '\t', header = False) 

