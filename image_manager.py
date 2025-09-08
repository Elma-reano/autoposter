#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:46:55 2025

@author: marianoluna
"""

import cv2 as cv
import numpy as np
from verboser import verboser
import asyncio

@verboser("Make Square")
def make_square(image_path: str, *,
                fill_color: tuple[int, int, int] = None,
                output_path: str = None,
                replace: bool = True):
    """
    Convierte una imagen en cuadrada, rellenando los espacios vacíos con un color
    El color por defecto es el promedio de los colores de la imagen original.

    Args:
        image_path (str): Ruta de la imagen a convertir.
        fill_color (tuple[int, int, int], optional): Color con el que se rellenan los espacios de la imagen. Defaults to None.
        output_path (str, optional): Ruta de la imagen. Defaults to None.
        replace (bool, optional): Reemplazar la imagen original con la cuadrada. Defaults to True.

    Raises:
        Exception: TODO

    Returns:
        None
    """

    img = cv.imread(image_path)
    height, width, _ = img.shape
    side = max(height, width)

    if not fill_color:
        fill_color = cv.mean(img)[:3]
        fill_color = tuple(map(int, fill_color))

    new_img = np.full((side, side, 3), fill_color, dtype=np.uint8)

    initial_x = (side - width) // 2
    initial_y = (side - height) // 2

    new_img[initial_y:initial_y + height, initial_x:initial_x + width] = img

    # TODO que se pueda elegir el formato de salida
    # TODO que se pueda poner solamente un sufijo al output_path, en vez de especificarlo por completo
    if replace:
        output_path = image_path
    else:
        if not output_path:
            raise Exception("Error, no se especificó un output_path.")
        
    cv.imwrite(output_path, new_img)
    return 0

async def make_square_async(image_path: str, *,
                            fill_color: tuple[int, int, int] = None,
                            output_path: str = None,
                            replace: bool = True):
    """
    Esto es un wrapper para poder llamar a la función make_square de forma asíncrona.
    """
    make_square(image_path, fill_color=fill_color, output_path=output_path, replace=replace)
    return

if __name__ == "__main__":
    import os

    async def main():
        test_imgs_folder_path = "tests/images"
        test_imgs_paths = [f"{test_imgs_folder_path}/{path}" for path in os.listdir(test_imgs_folder_path)]

        ejecucion = [make_square_async(path, output_path=f"{path}_square", replace=False) 
                     for path in test_imgs_paths]
        await asyncio.gather(*ejecucion)
    asyncio.run(main())



# from PIL import Image
# from verboser import verboser

# @verboser("Make Square")
# def make_square(image_path: str, *,
#                 fill_color: tuple[int, int, int] = (0,0,0),
#                 output_path: str = None,
#                 replace: bool = True):
    
#     img = Image.open(image_path)
#     width, height = img.size
    
#     new_size = max(width, height)
    
#     new_img = Image.new("RGB", (new_size, new_size), fill_color)
    
#     new_img.paste(img, ( (new_size - width) // 2, (new_size - height) // 2 ) )
    
#     if replace:
#         output_path = image_path
#     else:
#         if not output_path:
#             raise Exception("Error, no se especificó un output_path.")
        
#     new_img.save(output_path)
    
#     return True

# def main():
#     import os
#     images = [f"Memes/{image}" for image in os.listdir("Memes/")]
#     for image in images:
#         make_square(image, output_path=f"{image}_square.jpeg", replace=False)
#     return

# main()