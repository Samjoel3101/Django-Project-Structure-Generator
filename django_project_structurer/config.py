from .file_handler.handle_by_string import * 
from .file_handler.django.file_handler import * 
from .file_handler.handle_by_tree import * 

from .printer.django.printer import * 
from .printer.string_printers import * 
from .printer.tree_printers import * 
from .printer.styles import inline
from .printer.core import lst_flatten 

from copy import deepcopy
from functools import partial 


INFO_DICT = {
    'models': [[ModelFileHandler], [partial(ModelPrinter, style = inline)]],
    'forms':    [[HandleFileByTree], [ClassInlinePrinter]],
    'signals':  [[HandleFileByTree], [FunctionInlinePrinter]],
    'mixins':   [[HandleFileByTree], [ClassInlinePrinter]],
    'urls'  :   [[UrlFileHandler], [UrlInlinePrinter]]
}

def init_info_dict(info_dict):
    for name, (handlers, printers) in zip(info_dict.keys(), info_dict.values()):
        for idx, p in enumerate(printers): 
            printers[idx] = partial(p, custom_header = name.title())
    return info_dict 

INFO_DICT = init_info_dict(INFO_DICT)
# print(INFO_DICT)

DJANGO_FILENAMES = ['models', 'forms', 'signals', 'mixins', 'urls']