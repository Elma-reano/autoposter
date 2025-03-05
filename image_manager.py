#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:46:55 2025

@author: marianoluna
"""

from PIL import Image
from verboser import verboser

@verboser("Make Square")
def make_square(image_path: str, *,
                fill_color: tuple[int, int, int] = (0,0,0),
                output_path: str = None,
                replace: bool = True):
    
    img = Image.open(image_path)
    width, height = img.size
    
    new_size = max(width, height)
    
    new_img = Image.new("RGB", (new_size, new_size), fill_color)
    
    new_img.paste(img, ( (new_size - width) // 2, (new_size - height) // 2 ) )
    
    if replace:
        output_path = image_path
    else:
        if not output_path:
            raise Exception("Error, no se especificó un output_path.")
        
    new_img.save(output_path)
    
    return True