import inspect
import sys


def debug_print(*args, _file=sys.stderr, **kwargs):
    frame = inspect.getouterframes(inspect.currentframe())[1].frame
    info = inspect.getframeinfo(frame)
    lineno = inspect.getlineno(frame)
    module_path = inspect.getfile(frame)
    print(f"{module_path}:{lineno} ({info.function})", args, kwargs, sep="\n", file=_file)
