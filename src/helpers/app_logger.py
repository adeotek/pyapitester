from colorama import just_fix_windows_console
from typing import Any
from termcolor import colored, cprint, COLORS

just_fix_windows_console()


class Logger:
    __verbose = False

    def __init__(self, verbose: bool = False) -> None:
        self.__verbose = verbose

    def set_verbose(self, value: bool):
        self.__verbose = value
        return self

    def is_verbose(self) -> bool:
        return self.__verbose

    def new_line(self):
        print()
        return self

    def log(self, *values: object, **kwargs: Any):
        print(*values, sep='', **kwargs)
        return self

    def debug(self, *values: object, **kwargs: Any):
        if self.__verbose:
            self.log(*values, **kwargs)
        return self

    def clog(self, *values: object, **kwargs: Any):
        cvalues = []
        for v in values:
            if isinstance(v, tuple) and len(v) == 2 and isinstance(v[1], str) and v[1] in COLORS:
                cvalues.append(colored(v[0], v[1]))
            else:
                cvalues.append(v)
        self.log(*tuple(cvalues), **kwargs)
        return self

    def cdebug(self, *values: object, **kwargs: Any):
        if self.__verbose:
            self.clog(*values, **kwargs)
        return self

    def cprint(
        self,
        text: str,
        color=None,
        on_color=None,
        attrs=None,
        **kwargs: Any,
    ):
        cprint(text=text, color=color, on_color=on_color, attrs=attrs, **kwargs)
        return self
