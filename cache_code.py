import pickle as pkl
import os
import asyncio
from typing import Callable as function, Any
from functools import wraps

"""
    Este proyecto se ejecuta en mi celular; y a veces suele detenerse la ejecución antes de que sea completada.
    Es por eso que este sistema de cacheo es útil para evitar perder el progreso de las funciones que tardan mucho en ejecutarse.
    Por el momento, el cacheo no verifica que los inputs de las funciones sean los mismos, pero de momento no parece que sea necesario de implementar.

    El decorador `cache_handler` permite cachear el resultado de una función en un archivo pickle.
    Si el archivo de cacheo ya existe, se carga el resultado desde ahí; si no, se ejecuta la función y se guarda el resultado en el archivo.
"""

DEFAULT_CACHE_FOLDER = "cache"

def cache_handler(expect_result: bool = True,
                  cache_folder: str | None = None) -> function:
    """
    Decorator to cache the result of a function in a pickle file.
    Args:
        expect_result (bool, optional): Checks if the function returns a value. Defaults to True.
        TODO: Add option for a cache to be refreshed after a certain time.
        TODO: Add option for an expected result to be a certain value or type.

    Returns:
        The result of the function, either from cache or from execution.
    """
    def decorator(function):
        """
        This decorator wraps the function on an async or regular wrapper depending if the 
            function is a coroutine or not.
        """
        nonlocal cache_folder
        if cache_folder is None:
            cache_folder = DEFAULT_CACHE_FOLDER

        name = function.__name__
        module = function.__module__
        file_path = f"{cache_folder}/{module}_{name}_cache.pkl"

        @wraps(function)
        def wrapper(*args, **kwargs):
            if os.path.exists(file_path):
                print(f"Cache found for {name}. Loading from cache...")
                result = read_cache(file_path)
            else:
                try:
                    result = function(*args, **kwargs)
                    if not expect_result and result is None:
                        result = None  # Default value if no result is expected
                    elif not expect_result and result is not None:
                        print(f"Warning: {name} returned a result when none was expected.")
                    print(f"{name}: Done")
                    save_cache(file_path, result)
                except Exception as e:
                    print(f"Error in {name}.\nDescription: {e}")
                    return None
            return result
        
        async def async_wrapper(*args, **kwargs):
            if os.path.exists(file_path):
                print(f"Cache found for {name}. Loading from cache...")
                result = read_cache(file_path)
            else:
                try:
                    result = await function(*args, **kwargs)
                    if not expect_result and result is None:
                        result = 1  # Default value if no result is expected
                    elif not expect_result and result is not None:
                        print(f"Warning: {name} returned a result when none was expected.")
                    print(f"{name}: Done")
                    save_cache(file_path, result)
                except Exception as e:
                    print(f"Error in {name}.\nDescription: {e}")
                    return None
            return result
        return async_wrapper if asyncio.iscoroutinefunction(function) else wrapper
    return decorator

def read_cache(file_path: str):
    try:
        with open(file_path, "rb") as file:
            return pkl.load(file)
    except FileNotFoundError:
        print(f"No cache found for {file_path}.")
        return None
    except Exception as e:
        print(f"Error reading cache for {file_path}.\nDescription: {e}")
        return None
    
def save_cache(file_path: str,
               result: Any) -> None:
    if result:
        try:
            with open(file_path, "wb") as file:
                pkl.dump(result, file)
        except Exception as e:
            print(f"Error saving cache for {file_path}.\nDescription: {e}")
    else:
        print("No result to cache.")
    return

def delete_cache(cache_folder: str | None = None) -> None:
    """
    Deletes all cache files in the cache directory.
    """
    if cache_folder is None:
        cache_folder = DEFAULT_CACHE_FOLDER
    
    assert os.path.exists(cache_folder), f"Cache folder {cache_folder} does not exist."

    for file_name in os.listdir(cache_folder):
        file_path = os.path.join(cache_folder, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted cache file: {file_name}")
        except Exception as e:
            print(f"Error deleting cache file {file_name}.\nDescription: {e}")
    return

if __name__ == "__main__":
    @cache_handler()
    def test_function(a, b):
        return a + b

    result = test_function(5, 10)
    print(f"Resultado: {result}")

