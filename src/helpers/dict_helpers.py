from typing import List


def get_dict_attr(data: dict, key: str, default=None):
    if key in data.keys():
        return data[key]
    else:
        return default
    

def get_dict_bool(data: dict, key: str, default: bool = False) -> bool:
    if key in data.keys() and isinstance(data[key], bool):
        return data[key]
    else:
        return default
    
    
def get_dict_list(data: dict, key: str, default: List = ()) -> List:
    if key in data.keys() and isinstance(data[key], List):
        return data[key]
    else:
        return default
