from typing import TypeVar, Generic, Callable, Any, Dict, Optional, List, Self
import json

T = TypeVar('T')

class ConfigValue(Generic[T]):
    def __init__(self, key: str, default: T, init: Callable[[T], Any] = lambda x: x):
        self.key = key
        self.default = default
        self.init = init
        
    def parse(self, data: Dict[str, T]) -> T:
        if self.key in data:
            rawValue = data[self.key]
            
            if isinstance(self.default, BaseConfig):
                return self.default.fromData(rawValue)
            
            return rawValue
        
        return self.default

class BaseConfig():
    values: List[ConfigValue] = []
    
    @classmethod
    def fromPath(clx: Self, path: Optional[str]) -> Self:
        try: 
            data = json.load(open(path, 'r'))
            return clx.fromData(data)
        except:
            print("")
            return clx()
    
    @classmethod
    def fromData(clx: Self, data: Dict[str, Any]) -> Self:
        config = { value.key : value.parse(data) for value in clx.values }
        return clx(**config)

    def __init__(self, **kwargs):
        for config in self.values:
            key = config.key
            
            rawValue = kwargs[key] if key in kwargs else config.default
            value = config.init(rawValue)
            setattr(self, key, value)