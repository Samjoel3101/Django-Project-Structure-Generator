from structure_generator.generate_structure import Generate_Structure 
from structure_generator.django_structure import App_Structurer, DjangoProjectStructurer
from printer.tree_printers import * 
from printer.string_printers import ImportStatementPrinter, ImportStatementInlinePrinter
from file_handler.django.file_handler import ModelFileHandler 
from printer.django.printer import ModelPrinter, ModelInlinePrinter
from pathlib import Path

if __name__ == '__main__':

    o = DjangoProjectStructurer('D:\Deep Learning Websites\InspirAI', 'D:\\Software Structure Generator\\test_files')
    o.generate_project_info()