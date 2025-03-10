#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:50:30 2025

@author: marianoluna
"""

import os
import sys
import asyncio
from verboser import verboser
from image_manager import make_square
from imgur_api import imgur_upload, imgur_delete
from graph_api import create_media_container, create_media_carousel, publish_media

def get_txt_file_contents(path):
    with open(path, 'r') as file:
        contents = file.read()
    return contents


@verboser("AutoMariMomos Main")
def main():
    
    IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
    ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")
    
    MEME_FOLDER_PREFIX = "Memes/"

    paths = [f"{MEME_FOLDER_PREFIX}{path}" for path in os.listdir(MEME_FOLDER_PREFIX)]
    
    # Checa si es más de una foto
    if len(paths) == 0:
        return
    
    multiple = len(paths) > 1
    
    images_info = []
    
    # Cada imagen la hace square
    for path in paths:
        
        upload_image = imgur_upload(
                client_id = IMGUR_CLIENT_ID,
                image_path= path
            )
        images_info.append(upload_image)
        
    # Obtener los urls y hashes para borrar
    image_urls, delete_hashes = zip(*images_info)

    # Crear los contenedores en insta
    images_creation_ids = []
    
    for img_url in image_urls:
        
        creation_id = create_media_container(
                access_token= ACCESS_TOKEN,
                media_url= img_url,
                multiple= multiple
            )
        images_creation_ids.append(creation_id)
        
    # Si es más de una imagen, crea un carrusel
    # Si no, obtiene el unico url de los creation_ids
    media_id: str
    if multiple:
        carousel_id = create_media_carousel(
                access_token= ACCESS_TOKEN,
                children= images_creation_ids,
                caption= "AutoMarimomos. Atte: AutoMariMomosBot #marimomos"
            )
        media_id = carousel_id
        
    else:
        media_id = images_creation_ids[0]
        
    
    # Publica la publicacion publicandola para el publico
    media_publish = publish_media(
            access_token= ACCESS_TOKEN,
            media_id= media_id
        )
    
    # Borra las fotos del imgur
    for del_hash in delete_hashes:
        imgur_delete(
                client_id= IMGUR_CLIENT_ID,
                delete_hash= del_hash
            )
        
    return 0
        
main()
        
        
        
        
        
        
        