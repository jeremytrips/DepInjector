from DepInjector.exceptions import DependencyNotFoundException, SingletonAccessException
from typing import Type
import inspect
import DepInjector.registration_type as injectors
import typing

class Container: 
    setup = False
    instance = None

    def __init__(self) -> None:
        if(Container.setup):
            raise SingletonAccessException() 
        self.dependencies: typing.Dict[object, injectors.BaseInjector] = {}
        Container.setup = True
        Container.instance = self

    @staticmethod
    def get():
        if(not Container.setup):
            Container()
        return Container.instance

    def register(self, injector: injectors.BaseInjector):
        self.dependencies[injector.objectClass] = injector
    
    def resolve(self, cls):
        if not cls in self.dependencies.keys():
            raise DependencyNotFoundException(f"Unable to resolve class name {cls.__name__}")
        
        target = self.dependencies[cls]
        if(target.type == injectors.InjectorTypeEnum.Base):
            return self._resolve_base_object(target.objectClass)
        elif(target.type == injectors.InjectorTypeEnum.Singleton):
            return target.get()

    def _resolve_base_object(self, target):
        constructor_params = inspect.signature(target.__init__).parameters
        args = []
        for param_name, param_info in constructor_params.items():
            if param_name == "self":
                continue
            if param_info.default != inspect.Parameter.empty:
                args.append(param_info.default)
            elif ( param_info.annotation != inspect.Parameter.empty):
                arg = self.resolve(param_info.annotation)
                args.append(arg)
            else:
                raise DependencyNotFoundException(f'Unable to resolve argument called {param_name}')
        return target(*args)

    def get_args(self, class_method):
        constructor_params = inspect.signature(class_method).parameters
        args = []
        for param_name, param_info in constructor_params.items():
            if param_name == "self":
                continue
            if param_info.default != inspect.Parameter.empty:
                args.append(param_info.default)
            elif ( param_info.annotation != inspect.Parameter.empty):
                arg = self.resolve(param_info.annotation)
                args.append(arg)
            else:
                raise DependencyNotFoundException(f'Unable to resolve argument called {param_name}')
        return args

instance = Container()