import re 
import ast 
import inspect 
from pathlib import Path 

 
class HandleFileByTree:

    def __init__(self, filename):
        self.filename = Path(filename)
        self.functions, self.classes = self.get_members() 

    def get_members(self):
        with open(self.filename, 'r') as module:
            self.node = ast.parse(module.read())
        functions = [n for n in self.node.body if isinstance(n, ast.FunctionDef)]
        classes   = [n for n in self.node.body if isinstance(n, ast.ClassDef)] 
        return functions, classes 

class ClassAttributeVisitor:
    def __init__(self, class_node):
        self.class_attrs = self.visit_ClassDef(class_node)

    def visit_ClassDef(self, node):
        lst = []
        body = node.body 
        for statement in body:
            if isinstance(statement, ast.Assign):
               if len(statement.targets) == 1:
                   value = statement.value
                   value = self._check_type(value)
                   lst.append((statement.targets[0].id, value))
        return lst
    
    def _check_type(self, value):
        if isinstance(value, ast.Call):
            if isinstance(value.func, ast.Attribute):
                value = value.func.attr
            elif isinstance(value.func, ast.Name):
                value = value.func.id
        elif isinstance(value, ast.List):
            value = [e.s for e in value.elts]
        elif isinstance(value, ast.Constant):
            value = value.s
        elif isinstance(value, ast.Name):
            value = value.id
        return value


if __name__ == '__main__':
    f = ast.parse(open('D:\\Software Structure Generator\\test_files\\app\\api\\models.py', 'r').read())
    # print(dir(ast.Call))
    class_def = [n for n in f.body if isinstance(n, ast.ClassDef)]
    print(ClassAttributeVisitor().visit_ClassDef(class_def[0]))
  
        
                