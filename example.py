from main import SlowAPI

slowapi = SlowAPI()


 

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