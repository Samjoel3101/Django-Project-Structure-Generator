from structure_generator.generate_structure import Generate_Structure 


if __name__ == '__main__':
    filename = 'test_files/a.py'
    s = Generate_Structure(filename, None, ext = '.txt')
    s.print_info()