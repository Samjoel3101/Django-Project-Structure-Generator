from structure_generator.generate_structure import Generate_Structure 
from structure_generator.django_structure import DjangoStructureGenerator
from printer.tree_printers import * 
from printer.string_printers import ImportStatementPrinter

if __name__ == '__main__':
    filename = 'test_files/a.py'
    s = Generate_Structure(filename, None, '.txt', printers = [[ImportStatementPrinter], [ClassPrinter, FunctionPrinter]])
    s.print_info()