from typeCheck import typeCheck
"""
    funcSignature = inspect.signature(func)
    funcParameters = funcSignature.parameters
    actualParameters = inspect.getcallargs(func, *args,**kwargs)

    for el in funcParameters.items(): 
      parName, parClass = el
      actValue = actualParameters[parName]
      actAnnotation = parClass.annotation

      if (
        actAnnotation == inspect.Parameter.empty
        or type(actValue) == actAnnotation
      ): continue
      raise AssertionError(
        'Function signature error: parameters type not respected for: '
        f'{func.__name__}{str(funcSignature)}'
      )
    
    returnValue = func(*args, **kwargs)
    returnAnnotation = funcSignature.return_annotation

    if (actAnnotation == inspect.Parameter.empty): return returnValue

    if ( type(returnValue) != returnAnnotation ):
      raise AssertionError(
        'Function retrun value not respected for:'
        f'{func.__name__}{str(funcSignature)}'
      )
"""

@typeCheck
def funzdecorata(a:int, b:str, c:list, e, d=1) -> int:
  print('flusso per funzdecorata')
  return 987

print('Funzione decorata che riceve parametri corretti:')
funzdecorata(1,'stringaVuota',[],123)
funzdecorata(1,'stringaVuota',[], 123,321)

print('Funzione decorata che riceve parametri scorretti:')
#funzdecorata('stringa1',0 ,[],'e')
#funzdecorata('1',0,{},'e')
#funzdecorata('1',0,{}, '','e')
#funzdecorata('1',0,{}, '','e')

print('Versione di funz decorata che ritorna tipi sbagliati :')
@typeCheck
def funzdecorata1(a:int, b:str, c:list, e, d=1) -> int:
  print('flusso per funzdecorata1')
  return '987'

print('Funzione decorata n1  che riceve parametri corretti ma ritorna sbagliati:')
funzdecorata1(1,'stringaVuota',[],123)
funzdecorata1(1,'stringaVuota',[], 123,321)

print('Funzione decorata che riceve parametri scorretti e li ritorna sbagliati:')
funzdecorata1('stringa1',0 ,[],'e')
funzdecorata1('1',0,{},'e')
funzdecorata1('1',0,{}, '','e')
funzdecorata1('1',0,{}, '','e')
