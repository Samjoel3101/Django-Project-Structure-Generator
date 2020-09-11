from printer.core import Printer
from functools import partial  
from .. import styles 

class UrlPrinter(Printer):
    verbose_name = '_url_info'
    def create_content(self, url_tup, parent_path = ['']):
        url, name = url_tup 
        spacing = '\t'*6
        content = parent_path + [f"{url}{spacing}{name}\n"]
        return content 

    def content(self, *args, **kwargs):
        content = []
        for url_tup in self.handler.urls:
            content += self.create_content(url_tup, *args, **kwargs)
        return super().content(content) 
        
class ModelPrinter(Printer):
    verbose_name = '_model_info'
    def __init__(self, filename, savepath, ext, handler, **kwargs):
        self.args = (filename, savepath, ext, handler)
        super().__init__(*self.args, **kwargs)
        self.signal_printer = SignalsUsedPrinter(*self.args, style = styles.inline, custom_header = 'Signals Used')

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
        return super().content(content) + self.signal_printer.content()

class SignalsUsedPrinter(Printer):
    verbose_name = '_signals_used_info'
    def content(self):
        content = []
        for signal_name, sender in self.handler.signals_used:
            spacing = '\t'*3
            content += [f'Signal Func:{signal_name}{spacing}Sender:{sender}\n']
        return super().content(content)

class ModelInlinePrinter(ModelPrinter):
    def create_content(self, attr_list):
        return [] 

ModelInlinePrinter = partial(ModelInlinePrinter, style = styles.inline) 
UrlInlinePrinter   = partial(UrlPrinter, style = styles.inline)