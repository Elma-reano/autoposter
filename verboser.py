#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:01:58 2025

@author: marianoluna
"""
import traceback
import logging
import sys
import asyncio

VERBOSE = 2
APP_NAME = "AutoMariMomos"

logging.basicConfig(filename = f"{APP_NAME}.log",
                    level= logging.DEBUG,
                    format= "%(asctime)s - %(levelname)s - %(message)s",
                    filemode= "a"
                    )

def printL(*args,
           level= logging.INFO,
           **kwargs) -> None:
    text = " ".join(map(str, args))
    print(text, **kwargs)
    logging.log(level, text)
    return

def handle_exception(e, trace_variables):
    _, exc_value, exc_traceback = sys.exc_info()
    last_tb = traceback.walk_tb(exc_traceback)
    last_frame, _ = list(last_tb)[-1]

    printL(f"File: {last_frame.f_code.co_filename}", level= logging.ERROR)
    printL(f"Line: {last_frame.f_lineno}", level= logging.ERROR)

    if trace_variables:
        printL("Trace Variables:", level= logging.ERROR)
        local_vars = last_frame.f_locals

        for var_name in trace_variables:
            value = local_vars.get(var_name, "No encontrada")
            printL(f"{var_name} = {value}", level= logging.ERROR)
    return

def verboser(name: str = "Funcion", *,
             suffix: str = "",
             trace_variables: list = None,
             verbose : int = VERBOSE):
    def decorator(function):
        def wrapper(*args, **kwargs):
            printL(f"{name}{suffix}: Starting: ", end='') if verbose > 0 else None
            try:
                result = function(*args, **kwargs)
                printL("Done") if verbose > 0 else None
            except Exception as e:
                printL(f"Error.\nDescription: {e}", level= logging.ERROR)
                handle_exception(e, trace_variables)    
                return None
            return result
        
        async def async_wrapper(*args, **kwargs):
            printL(f"{name}{suffix}: Starting") if verbose > 0 else None
            try:
                result = await function(*args, **kwargs)
                printL(f"{name}{suffix}: Done") if verbose > 0 else None
            except Exception as e:
                printL(f"Error.\nDescription: {e}", level= logging.ERROR)
                handle_exception(e, trace_variables)
                return None
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(function) else wrapper
        # return wrapper
    return decorator

# @verboser("Funcion que da error", verbose=2, trace_variables= ['a'])
# def funcion_error():
#     a = 2
#     1/0
    
# funcion_error()

# @verboser("Division", trace_variables=["x", "y"], verbose=1)
# def dividir(a, b):
#     x = a
#     y = b
#     return x / y  # Generará error si b == 0

# dividir(10, 2)  # Funciona bien
# dividir(10, 0)  # Generará log con trace_variables

# @verboser("MiAsyncFuncion", trace_variables=["x", "y"], verbose=1)
# async def error_async(a, b):
#     x = a
#     y = b
#     await asyncio.sleep(3)
#     return x / y  # Generará error si b == 0

# asyncio.run(error_async(10, 2))  # Funciona bien
# asyncio.run(error_async(10, 0))  # Generará log con trace_variables

# dividir(10, 2)  # Funciona bien
# dividir(10, 0)  # Generará log con trace_variables



