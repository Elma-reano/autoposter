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

DEFAULT_VERBOSE = 2
APP_NAME = "AutoMariMomos"

logging.basicConfig(filename = f"{APP_NAME}.log",
                    level= logging.DEBUG,
                    format= "%(asctime)s - %(levelname)s - %(message)s",
                    filemode= "a"
                    )

def set_verbose_level(level: int) -> None:
    """
    Sets the logging verbosity level.
    Levels:
        0 - ERROR
        1 - WARNING
        2 - INFO
        3 - DEBUG
    """
    if level == 0:
        logging.getLogger().setLevel(logging.ERROR)
    elif level == 1:
        logging.getLogger().setLevel(logging.WARNING)
    elif level == 2:
        logging.getLogger().setLevel(logging.INFO)
    elif level >= 3:
        logging.getLogger().setLevel(logging.DEBUG)
    return


def print_and_log(*args,
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

    print_and_log(f"File: {last_frame.f_code.co_filename}", level= logging.ERROR)
    print_and_log(f"Line: {last_frame.f_lineno}", level= logging.ERROR)

    if trace_variables:
        print_and_log("Trace Variables:", level= logging.ERROR)
        local_vars = last_frame.f_locals

        for var_name in trace_variables:
            value = local_vars.get(var_name, "No encontrada")
            print_and_log(f"{var_name} = {value}", level= logging.ERROR)
    return

def verboser(*,
             suffix: str = "",
             trace_variables: list | None = None,
             verbose : int | None = None):
    if verbose is None:
        verbose = DEFAULT_VERBOSE
    def decorator(function):
        name = function.__name__
        def wrapper(*args, **kwargs):
            print_and_log(f"{name}{suffix}: Starting: ", end='') if verbose > 0 else None
            try:
                result = function(*args, **kwargs)
                print_and_log("Done") if verbose > 0 else None
            except Exception as e:
                print_and_log(f"Error.\nDescription: {e}", level= logging.ERROR)
                handle_exception(e, trace_variables)    
                return None
            return result
        
        async def async_wrapper(*args, **kwargs):
            print_and_log(f"{name}{suffix}: Starting") if verbose > 0 else None
            try:
                result = await function(*args, **kwargs)
                print_and_log(f"{name}{suffix}: Done") if verbose > 0 else None
            except Exception as e:
                print_and_log(f"Error.\nDescription: {e}", level= logging.ERROR)
                handle_exception(e, trace_variables)
                return None
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(function) else wrapper
    return decorator

if __name__ == "__main__":

    @verboser(verbose=2, trace_variables= ['a'])
    def funcion_error():
        a = 2
        1/0
        
    funcion_error()

    @verboser(trace_variables=["x", "y"], verbose=1)
    def dividir(a, b):
        x = a
        y = b
        return x / y  # Generará error si b == 0

    dividir(10, 2)  # Funciona bien
    dividir(10, 0)  # Generará log con trace_variables

    @verboser(trace_variables=["x", "y"], verbose=1)
    async def error_async(a, b):
        x = a
        y = b
        await asyncio.sleep(3)
        return x / y  # Generará error si b == 0

    asyncio.run(error_async(10, 2))  # Funciona bien
    asyncio.run(error_async(10, 0))  # Generará log con trace_variables

    dividir(10, 2)  # Funciona bien
    dividir(10, 0)  # Generará log con trace_variables



