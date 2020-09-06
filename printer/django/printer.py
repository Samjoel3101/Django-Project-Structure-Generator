from printer.core import Printer 

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
        
