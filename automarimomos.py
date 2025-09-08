import os
import asyncio
from cache_code import cache_handler
from image_manager import make_square_async
from imgur_api import imgur_upload_async, imgur_delete_async
from graph_api import create_media_container_async, create_media_carousel, publish_media

# TODO: Se podría hacer que las fotos se suban en orden?

async def main():
    """
    This function automatically uploads images from a specified folder to Imgur, creates media containers,
    and publishes them on instagram. It handles both single and multiple image uploads, including creating
    a carousel for multiple images. After publishing, it deletes the images from Imgur.
    TODO: Video support
    """

    # Carga las keys y los paths de las fotos
    IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
    ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")
    MEME_FOLDER_PREFIX = "Memes/"
    paths = [f"{MEME_FOLDER_PREFIX}{path}" for path in os.listdir(MEME_FOLDER_PREFIX) if path.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Checa si es más de una foto
    if len(paths) == 0:
        return 
    multiple = len(paths) > 1

    # Encuadrada las imágenes
    await square_images(paths)

    # Sube las imágenes a imgur
    imgur_images = await upload_to_imgur(paths, IMGUR_CLIENT_ID)
    print(imgur_images)
    imgur_image_urls, imgur_delete_hashes = zip(*imgur_images)


    # Crea los contenedores de las imagenes en Meta
    images_container_ids = await create_media_containers(
        imgur_image_urls,
        access_token= ACCESS_TOKEN,
        multiple= multiple
    )
    
    # Si son varias imágenes, las sube a un carrusel, si no, a un solo contenedor
    # TODO caption dinámica
    media_id: str
    if multiple:
        carousel_id = create_media_carousel(
                            children= images_container_ids,
                            access_token= ACCESS_TOKEN,
                            caption= "AutoMarimomosBot: Marimomos. Atte: AutoMarimomosBot #marimomos")
        media_id = carousel_id
    else:
        media_id = images_container_ids[0]

    # Sube el contenido a marimomos
    publish_media(access_token= ACCESS_TOKEN,
                  media_id= media_id)
    
    # Borra las imágenes de imgur
    await delete_imgur_images(imgur_delete_hashes,
                             client_id= IMGUR_CLIENT_ID)   


def get_txt_file_contents(path):
    # TODO if the file is too big, read it in chunks
    with open(path, 'r') as file:
        contents = file.read()
    return contents

@cache_handler("make_square_images", expect_result=False)
async def square_images(paths):
    execution = [make_square_async(path) for path in paths]
    await asyncio.gather(*execution)
    return

@cache_handler("upload_to_imgur")
async def upload_to_imgur(img_paths: list,
                          client_id: str):
    ejecucion = [imgur_upload_async(client_id= client_id,
                                    image_path= path) for path in img_paths]
    return await asyncio.gather(*ejecucion)

@cache_handler("create_media_containers")
async def create_media_containers(imgur_img_url_list: list,
                                  access_token: str,
                                  multiple: bool):
    ejecucion = [create_media_container_async(access_token= access_token,
                                             media_url= url,
                                             multiple= multiple) for url in imgur_img_url_list]
    return await asyncio.gather(*ejecucion) 

@cache_handler("delete_imgur_images", expect_result= False)
async def delete_imgur_images(imgur_delete_hashes: list,
                              client_id: str):
    ejecucion = [imgur_delete_async(delete_hash=hash,
                                    client_id= client_id) for hash in imgur_delete_hashes]
    await asyncio.gather(*ejecucion)
    return                         


if __name__ == "__main__":
    asyncio.run(main())