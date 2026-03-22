import os
import asyncio
from notificator import notify
from cache_code import cache_handler
from image_manager import make_square_async
from file_operator import get_txt_file_contents
# from imgur_api import imgur_upload_async, imgur_delete_async
from cloudinary_api import (
    upload_image as cloudinary_upload_image,
    delete_image as cloudinary_delete_image,
    upload_image_async as cloudinary_upload_image_async,
    delete_image_async as cloudinary_delete_image_async
    )
from graph_api import create_media_container_async, create_media_carousel, publish_media


global DEBUG
DEBUG = False

global IMGUR_CLIENT_ID, ACCESS_TOKEN, MEDIA_FOLDER_PREFIX
IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")
MEDIA_FOLDER_PREFIX = "media/"

DEFAULT_CAPTION = "AutoMarimomosBot: Marimomos. Atte: AutoMarimomosBot #memes #momos #marimomos #shitpost #funny #humor #memesdaily"

# TODO: Se podría hacer que las fotos se suban en orden?

# Step 1: Make images square
@cache_handler(expect_result=False)
async def square_images(paths):
    execution = [make_square_async(path) for path in paths]
    await asyncio.gather(*execution)
    return

# # Step 2: Upload the images to Imgur
# @cache_handler()
# async def upload_to_imgur(img_paths: list,
#                           client_id: str) -> list[tuple[str, str]]:
#     ejecucion = [imgur_upload_async(client_id= client_id,
#                                     image_path= path) for path in img_paths]
#     return await asyncio.gather(*ejecucion)

# New Step 2: Upload the images to Cloudinary
@cache_handler()
async def upload_to_cloudinary(img_paths: list, folder: str) -> list[tuple[str, str]]:
    sem = asyncio.Semaphore(5)  # Limita a 5 uploads simultáneos

    tasks = [
        cloudinary_upload_image_async(sem, img_path, folder)
        for img_path in img_paths
    ]
    results = await asyncio.gather(*tasks)
    return results

# Step 3: Create media containers in Meta
@cache_handler()
async def create_media_containers(cloudinary_img_url_list: list[str],
                                  access_token: str,
                                  multiple: bool) -> list[str]:
    ejecucion = [create_media_container_async(access_token= access_token,
                                             media_url= url,
                                             multiple= multiple) for url in cloudinary_img_url_list]
    return await asyncio.gather(*ejecucion) 

# Step 4: Create carousel if multiple images
@cache_handler()
def create_carousel(children: list,
                    access_token: str,
                    caption: str | None = None):
    return create_media_carousel(access_token= access_token,
                                 children= children,
                                 caption= caption)

# Step 5: Publish the content on instagram
@cache_handler()
def create_post(access_token: str,
                         media_id: str):
    post_id = publish_media(access_token= access_token,
                            media_id= media_id)
    return post_id

# # Step 6: Delete the images from Imgur
# @cache_handler(expect_result= False)
# async def delete_imgur_images(imgur_delete_hashes: list,
#                               client_id: str):
#     ejecucion = [imgur_delete_async(delete_hash=hash,
#                                     client_id= client_id) for hash in imgur_delete_hashes]
#     await asyncio.gather(*ejecucion)
#     return  

# New Step 6: Delete the images from Cloudinary
@cache_handler(expect_result= False)
async def delete_cloudinary_images(public_ids: list):
    sem = asyncio.Semaphore(5)  # Limita a 5 deletes simultáneos

    tasks = [
        cloudinary_delete_image_async(sem, public_id)
        for public_id in public_ids
    ]
    await asyncio.gather(*tasks)
    return
                       


async def main():
    """
    This function automatically uploads images from a specified folder to Cloudinary, creates media containers,
    and publishes them on instagram. It handles both single and multiple image uploads, including creating
    a carousel for multiple images. After publishing, it deletes the images from Cloudinary.
    TODO: Video support on cloudinary
    """

    # Carga las keys y los paths de las fotos

    paths = [f"{MEDIA_FOLDER_PREFIX}{path}" for path in os.listdir(MEDIA_FOLDER_PREFIX) if path.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Checa si es más de una foto
    if len(paths) == 0:
        return 
    multiple = len(paths) > 1

    # Encuadrada las imágenes
    await square_images(paths)

    if DEBUG:
        notif_text = "Images Squared"
        notify(notif_text)

    # Sube las imágenes a cloudinary
    cloudinary_images: list[tuple[str, str]] = await upload_to_cloudinary(paths, IMGUR_CLIENT_ID)
    print(cloudinary_images)
    cloudinary_images = [x for x in cloudinary_images if x is not None]
    cloudinary_image_urls: list[str]
    cloudinary_public_ids: list[str]
    cloudinary_image_urls, cloudinary_public_ids = zip(*cloudinary_images) # type: ignore

    if DEBUG:
        notif_text = '\n'.join([
            "Images Uploaded to Cloudinary",
            f"Image URLs: {cloudinary_image_urls}",
            f"Public IDs: {cloudinary_public_ids}"
        ])
        notify(notif_text)

    # Crea los contenedores de las imagenes en Meta
    images_container_ids = await create_media_containers(
        cloudinary_image_urls,
        access_token= ACCESS_TOKEN,
        multiple= multiple
    )

    if DEBUG:
        notif_text = '\n'.join([
            "Containers Created",
            f"Container IDs {images_container_ids}"
        ])
        notify(notif_text)
    
    # Si son varias imágenes, las sube a un carrusel, si no, a un solo contenedor
    # TODO caption dinámica
    media_id: str
    if multiple:
        carousel_id = create_carousel(
                            children= images_container_ids,
                            access_token= ACCESS_TOKEN,
                            caption= DEFAULT_CAPTION)
        media_id = carousel_id

        if DEBUG:
            notif_text = '\n'.join([
                "Carousel Created",
                f"Carousel ID {carousel_id}"
            ])
            notify(notif_text)

    else:
        media_id = images_container_ids[0]

    # Sube el contenido a instagram
    post_id = create_post(access_token= ACCESS_TOKEN,
                          media_id= media_id)
    # No debug?
    # No se hace la notificación aquí porque quiero que me notifique 
    # siempre que se suba o se intente subir algo
    # La notificacion está dentro de la función en graph_api.py
    
    # Borra las imágenes de cloudinary
    await delete_cloudinary_images(cloudinary_public_ids)   




if __name__ == "__main__":
    notify("Starting")
    asyncio.run(main())