import inspect
import types
from response import Response
from method_type import MethodType
from request import Request
from parse import parse



method_names = {"GET",'POST','DELETE'}


class SlowAPI:
    def __init__(self,middlewares=[]):
        self.routes = dict()
        self.middlewares = middlewares
        self.local_middleware = dict()

    
    def __call__(self, environ, start_response):
        response = Response()
        request = Request(env=environ)

        for global_midd in self.middlewares:
            if isinstance(global_midd,types.FunctionType):
                global_midd(request)
            else:
                raise ValueError("Only you can pass functions")

        
        for path,handler_fn in self.routes.items():
            res = parse(path,request.path_info)
            for method_name,fn in handler_fn.items():
                if method_name == request.request_method and res:

                    middle_ls = self.local_middleware[path][method_name]

                    for mw in middle_ls:
                        if isinstance(mw,types.FunctionType):
                            mw(request)

                
                    fn(request,response,**res.named)
                   
                    return response.is_wsgi(start_response)
        return response.is_wsgi(start_response)
        
    

    def common_route(self,*,route_name,method_name,handler,middleware):
        route_name = route_name or f"/{handler.__name__}"
            
        if route_name not in self.routes:
            self.routes[route_name] = {}
        self.routes[route_name][method_name] = handler

        middleware_name = route_name or f"/{handler.__name__}"
        if middleware_name not in self.local_middleware:
            self.local_middleware[middleware_name] = {}
        self.local_middleware[middleware_name][method_name] = middleware

                    
                    
    def get(self,path=None,middleware=[]):
        def wrapper(handler):
           return self.common_route(route_name=path,method_name=MethodType.GET.value,handler=handler,middleware=middleware)
        return wrapper
    

    def post(self,path=None,middleware=[]):
        def wrapper(handler):
            return self.common_route(route_name=path,method_name=MethodType.POST.value,handler=handler,middleware=middleware)
        return wrapper
    
    def route(self,path=None,middleware=[]):
        def wrapper(handler):
            if isinstance(handler,type):
                fn_names = inspect.getmembers(handler,lambda x: inspect.isfunction(x) and  not (x.__name__.startswith("__") and x.__name__.endswith("__")) and x.__name__.upper() in method_names)

                for method_name,fn in fn_names:
                    self.common_route(route_name=path,middleware=middleware,method_name=method_name.upper(),handler=fn)
            else:
                raise ValueError("@only can accept the class based routing")

                

        return wrapper



 

def fn(request):
    print("This is global middleware")
slowapi = SlowAPI(middlewares=[fn])


# @slowapi.get("/users/{id}")
# def get_api(req,res,id):
    
#     res.send(text=id,status_code = 201)


def another_fun(request):
    print("This middlware is local middleware3",request.path_info)


@slowapi.post('/users',middleware=[another_fun])
def post_api(req,res):
    res.send(text={
        "name":"","age": "21"
    },status_code = 200)
   

def f(request):
    print("This is about middleware")
@slowapi.get('/about',middleware=[f])
def post_api(req,res):
    res.send(text={
        "name":"vijay kumar","age": "21"
    },status_code = 200)
    
@slowapi.get('/home')
def post_api(req,res):
    res.send(text={
        "name":"vijay kumar","age": "21"
    },status_code = 200)




@slowapi.route("/category")
class Book:


    def post(req,res):
        print("this ")
        res.send(text="This is class based route post method")
    def get(req,res):
        res.send(text="this is class based route")


@slowapi.get("/")
def html_page(req,res):
    res.render(file_name="example",context={"name":"This is Vijay","context":"This is context of the html page"})