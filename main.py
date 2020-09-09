from structure_generator.generate_structure import Generate_Structure 
from structure_generator.django_structure import App_Structurer
from printer.tree_printers import * 
from printer.string_printers import ImportStatementPrinter, ImportStatementInlinePrinter
from file_handler.django.file_handler import ModelFileHandler 
from printer.django.printer import ModelPrinter, ModelInlinePrinter
from pathlib import Path
if __name__ == '__main__':
    # filename = 'test_files/a.py'
    # s = Generate_Structure(filename, None, '.txt', printers = [[ImportStatementInlinePrinter], [ClassInlinePrinter, FunctionInlinePrinter]])
    # s.print_info()
    # filename = Path('D:\\Software Structure Generator\\test_files\\app\\api\\models.py')
    # f = ModelFileHandler(filename)
    # printer = ModelInlinePrinter(filename, None, '.txt', f)
    # printer.txt_writer()
    # print(f.class_attrs)

    o = App_Structurer('D:\Deep Learning Websites\InspirAI\website_image_utils', 'D:\\Software Structure Generator\\test_files')
    # for c in o.content():
    #     print(c, end = '')
    o.print_info()