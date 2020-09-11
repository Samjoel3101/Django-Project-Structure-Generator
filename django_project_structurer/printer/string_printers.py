from .core import * 
from functools import partial 
from . import styles
class ImportStatementPrinter(Printer):
    verbose_name = '_import_info'

    def create_content(self, import_modules, from_modules):
        content = []
        for import_line in import_modules:
            content.append(f'{import_line}\n')
        for parent_name, module in from_modules:
            content.append(f'{parent_name} -> {module}\n')
        return content 
    
    def content(self):
        content = self.create_content(self.handler.import_modules, self.handler.from_modules)
        content = super().content(content)
        return content 

ImportStatementInlinePrinter = partial(ImportStatementPrinter, style = styles.inline)