import re

class Response:
    def __init__(self,text="Method is not found",status_code='401 Missing the route'):
        self.status_code = status_code
        self.text = text
        self.headers = []
    def is_wsgi(self,start_res):
        start_res(self.status_code,self.headers)
        return [(self.text).encode()]
    
    
    def send(self,*,text,status_code=200):
        if isinstance(text,dict):
            self.text = str(text)   
        else:
            self.text = text
        self.status_code  = f"{status_code} OK"
    
    def render(self,*,file_name,context={}):
        path = f"{file_name}.html"
        with open( path) as fp:
            template = fp.read()

            for key,val in context.items():
                
                # template = re.sub(r'{{\s*'+re.escape(key)+r"\s}}$",str(val),template)
                template = re.sub(r'{{\s*' + re.escape(key) + r'\s*}}', val, template)
            
            self.status_code = "200 OK"
            self.headers.append(("Content-Type","text/html"))
            self.text = template
                 

        

        