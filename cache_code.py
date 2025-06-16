import pickle as pkl
import os
import asyncio

"""
    Este proyecto se ejecuta en mi celular; y a veces suele detenerse la ejecución antes de que sea completada.
    Es por eso que este sistema de cacheo es útil para evitar perder el progreso de las funciones que tardan mucho en ejecutarse.
    Por el momento, el cacheo no verifica que los inputs de las funciones sean los mismos, pero de momento no parece que sea necesario de implementar.

    El decorador `cacher` permite cachear el resultado de una función en un archivo pickle.
    Si el archivo de cacheo ya existe, se carga el resultado desde ahí; si no, se ejecuta la función y se guarda el resultado en el archivo.
"""

def cache_handler(name: str = "Funcion",
                  expect_result: bool = True) -> None:
    def decorator(function):
        def wrapper(*args, **kwargs):
            file_path = f"cache/{name}_cache.pkl"
            if os.path.exists(file_path):
                print(f"Cache found for {name}. Loading from cache...")
                result = read_cache(file_path)
            else:
                try:
                    result = function(*args, **kwargs)
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
        async def async_wrapper(*args, **kwargs):
            file_path = f"cache/{name}_cache.pkl"
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
               result: any) -> None:
    if result:
        try:
            with open(file_path, "wb") as file:
                pkl.dump(result, file)
        except Exception as e:
            print(f"Error saving cache for {file_path}.\nDescription: {e}")
    else:
        print("No result to cache.")
    return

if __name__ == "__main__":
    @cache_handler("MiFuncion")
    def mi_funcion(a, b):
        return a + b

    result = mi_funcion(5, 10)
    print(f"Resultado: {result}")


# @verboser("Funcion que da error", verbose=2, trace_variables= ['a'])
# def funcion_error():
#     a = 2
#     1/0