from config.common import settings
from exte.Logger import log


def command(name):
    def decorator(func):
        settings.registered_functions[name] = func
        async def wrapper(*args, **kw):
            return await func(*args, **kw)
        return wrapper
    return decorator




def flash_resgister():
    import inspect
    import importlib
    
    try:
        module_name = inspect.getmodulename(settings.register_file[0])
        spec = importlib.util.spec_from_file_location(module_name, settings.register_file[0])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        log.debug(f"注册函数:{settings.registered_functions}")
        return True
    except Exception:
        log.debug(Exception)
        return False
