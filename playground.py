import asyncio 

import inspect 
import DepInjector.container as container
import DepInjector.registration_type as injectors

class B:
    def __init__(self) -> None:
        pass


class A:
    
    def __init__(self, test: B, c: int=-1, b: str="",) -> None:
        self. a = 1
        self.b = b
        self.c = c
        self.text= test

def resolved_service(cls):

    class ResolvedService(cls):
        def __init__(self) -> None:
            self.container = container.Container.get()
            args = self.container.get_args(cls.__init__)
            super().__init__(*args)

    return ResolvedService
    
@resolved_service
class Service():

    def __init__(self, a: A, b: B) -> None:
        super().__init__()
        self.b = b
        self.a = a

    def run(self):
        while(True):
            print(self.a) 
            print(self.b) 

if __name__ == "__main__":
    a = container.Container.get()
    a.register(injectors.BaseInjector(A))
    a.register(injectors.SingletonInjector(B))

    ser = Service()
    ser.run()
