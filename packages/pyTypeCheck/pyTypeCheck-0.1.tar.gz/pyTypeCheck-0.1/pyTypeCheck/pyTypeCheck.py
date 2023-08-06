import functools
import inspect

def __typeCheck_parameterTypeAreOk(func, *args,**kwargs):
  funcParameters = inspect.signature(func).parameters
  actualParameters = inspect.getcallargs(func, *args,**kwargs)

  for el in funcParameters.items(): 
    parName, parClass = el
    actValue = actualParameters[parName]
    actAnnotation = parClass.annotation
    if (
      actAnnotation != inspect.Parameter.empty
      and type(actValue) != actAnnotation
    ): return False
  return True

def __typeCheck_retrunTypeOk(func, returnValue):
  returnAnnotation = inspect.signature(func).return_annotation
  if (
    returnAnnotation != inspect.Parameter.empty
    and type(returnValue) != returnAnnotation 
  ): return False
  return True

def typeCheck(func):
  @functools.wraps(func)
  def wrapper(*args,**kwargs):
    if not __typeCheck_parameterTypeAreOk(func, *args,**kwargs):
      raise AssertionError(
        'Function signature error: parameters type not respected for: '
        f'{func.__name__}{str(inspect.signature(func))}'
      )
    returnValue = func(*args, **kwargs)
    if not __typeCheck_retrunTypeOk(func, returnValue):
      raise AssertionError(
        'Function signature error: return type not respected for:'
        f'{func.__name__}{str(inspect.signature(func))}'
      )
    return returnValue
  return wrapper
