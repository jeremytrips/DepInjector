


class InjectorTypeEnum:
    Base=0
    Singleton=1

class BaseInjector:

    def __init__(self, cls) -> None:
        self.cls = cls

    def get(self):
        raise NotImplementedError();

    @property
    def objectClass(self):
        return self.cls
    
    @property
    def type(self):
        return InjectorTypeEnum.Base

class SingletonInjector(BaseInjector):

    def __init__(self, cls) -> None:
        super().__init__(cls)
        self.instance = None
    
    def get(self):
        if(self.instance == None):
            self.instance = self
        return self.instance
    @property
    def type(self):
        return InjectorTypeEnum.Singleton
    
class FunctionInjector(BaseInjector):
    pass
