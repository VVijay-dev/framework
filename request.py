class Request:
    def __init__(self,env):
        for key,val in env.items():
            setattr(self,key.replace(".","_").lower(),val)
        
        # print(env)