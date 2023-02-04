import inspect


def debugStart(modulName, funcName, args = ""):
    print(f"{modulName}.{funcName}() START:{args}")


def debugEnd(modulName, funcName, args = ""):
    print(f"{modulName}.{funcName}() END:{args}")


def getFuncName():
    return inspect.stack()[1][3]