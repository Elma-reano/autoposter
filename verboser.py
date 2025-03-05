#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:01:58 2025

@author: marianoluna
"""
import traceback
import logging
import sys

# a=1

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

def verboser(name: str = "Funcion", *,
             trace_variables: list = None,
             verbose : int = VERBOSE):
    def decorator(function):
        def wrapper(*args, **kwargs):
            printL(f"{name}: Starting: ", end='') if verbose > 0 else None
            try:
                result = function(*args, **kwargs)
                printL("Done") if verbose > 0 else None
            except Exception as e:
                printL(f"Error.\nDescription: {e}", level= logging.ERROR)
                
                _, exc_value, exc_traceback = sys.exc_info()
                last_tb = traceback.walk_tb(exc_traceback)
                last_frame, _ = list(last_tb)[-1]
                
                if verbose > 0:
                    printL(f"File: {last_frame.f_code.co_filename}", level= logging.ERROR)
                    printL(f"Line: {last_frame.f_lineno}", level= logging.ERROR)
                
                if trace_variables:
                    printL("Trace Variables:", level= logging.ERROR)
                    local_vars = last_frame.f_locals
                    
                    for var_name in trace_variables:
                        value = local_vars.get(var_name, "No encontrada")
                        printL(f"{var_name} = {value}", level= logging.ERROR)
                
                return None
            return result
        return wrapper
    return decorator

# @verboser("Funcion que da error", verbose=2, trace_variables= ['a'])
# def funcion_error():
#     a = 2
#     1/0
    
# funcion_error()

# @verboser("MiFuncion", trace_variables=["x", "y"], verbose=1)
# def dividir(a, b):
#     x = a
#     y = b
#     return x / y  # Generará error si b == 0

# dividir(10, 2)  # Funciona bien
# dividir(10, 0)  # Generará log con trace_variables



