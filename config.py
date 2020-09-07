from file_handler.handle_by_string import * 
from file_handler.django.file_handler import * 
from file_handler.handle_by_tree import * 

from printer.django.printer import * 
from printer.string_printers import * 
from printer.tree_printers import * 

INFO_DICT = {
    'models': [[ModelFileHandler], []],
    'forms':    [[HandleFileByTree], []],
    'signals':  [[HandleFileByTree], [ClassPrinter, FunctionInlinePrinter]],
    'mixins':   [[HandleFileByTree], [ClassPrinter]],
    'urls'  :   [[UrlFileHandler], [UrlPrinter]]
}