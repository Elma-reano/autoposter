import os
import asyncio
from verboser import verboser
from image_manager import make_square_async
from imgur_api import imgur_upload_async, imgur_delete_async
from graph_api import create_media_container_async, create_media_carousel, publish_media

def get_txt_file_contents(path):
    with open(path, 'r') as file:
        contents = file.read()
    return contents

async def square_images(paths):
    execution = [make_square_async(path) for path in paths]
    await asyncio.gather(*execution)
    return

async def upload_to_imgur(img_paths: list,
                          client_id: str):
    ejecucion = [imgur_upload_async(client_id= client_id,
                                    image_path= path) for path in img_paths]
    return await asyncio.gather(*ejecucion)

async def create_media_containers(imgur_img_url_list: list,
                                  access_token: str,
                                  multiple: bool):
    ejecucion = [create_media_container_async(access_token= access_token,
                                             media_url= url,
                                             multiple= multiple) for url in imgur_img_url_list]
    return await asyncio.gather(*ejecucion) 

async def delete_imgur_images(imgur_delete_hashes: list,
                              client_id: str):
    ejecucion = [imgur_delete_async(delete_hash=hash,
                                    client_id= client_id) for hash in imgur_delete_hashes]
    await asyncio.gather(*ejecucion)
    return                        

async def main():

    IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
    ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")

    MEME_FOLDER_PREFIX = "Memes/"
    paths = [f"{MEME_FOLDER_PREFIX}{path}" for path in os.listdir(MEME_FOLDER_PREFIX) if path.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Checa si es más de una foto
    if len(paths) == 0:
        return 
    multiple = len(paths) > 1

    await square_images(paths)

    imgur_images = await upload_to_imgur(paths, IMGUR_CLIENT_ID)
    print(imgur_images)
    imgur_image_urls, imgur_delete_hashes = zip(*imgur_images)

    images_container_ids = await create_media_containers(
        imgur_image_urls,
        access_token= ACCESS_TOKEN,
        multiple= multiple
    )
    
    media_id: str
    if multiple:
        carousel_id = create_media_carousel(
                            children= images_container_ids,
                            access_token= ACCESS_TOKEN,
                            caption= "Ultima prueba del nuevo backend. Atte: Mariano")
        media_id = carousel_id
    else:
        media_id = images_container_ids[0]

    publish_media(access_token= ACCESS_TOKEN,
                  media_id= media_id)
    
    await delete_imgur_images(imgur_delete_hashes,
                             client_id= IMGUR_CLIENT_ID)    
    

# async def main_but_imgur_has_been_run():
#     IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
#     ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")

#     imgur_images = []
    
#     imgur_image_urls, imgur_delete_hashes = zip(*imgur_images)

#     images_container_ids = await create_media_containers(
#         imgur_image_urls,
#         access_token= ACCESS_TOKEN,
#         multiple= True
#     )

#     multiple = True

#     media_id: str
#     if multiple:
#         carousel_id = create_media_carousel(
#                             children= images_container_ids,
#                             access_token= ACCESS_TOKEN,
#                             caption = "Hey. Estoy probando un backend nuevo que se corre más rápido. También le cambié el color al fill. ¿Qué opinan?")
#         media_id = carousel_id
#     else:
#         media_id = images_container_ids[0]

#     publish_media(access_token= ACCESS_TOKEN,
#                   media_id= media_id)
    
#     await delete_imgur_images(imgur_delete_hashes,
#                              client_id= IMGUR_CLIENT_ID)  

# async def main_but_the_media_containers_have_been_created():

#     IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
#     ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")

#     imgur_images = []
    
#     imgur_image_urls, imgur_delete_hashes = zip(*imgur_images)

#     images_container_ids = [
#                             ]

#     multiple = True

#     media_id: str
#     if multiple:
#         carousel_id = create_media_carousel(
#                             children= images_container_ids,
#                             access_token= ACCESS_TOKEN,
#                             caption = "Parte 2 de los nuevos tests. Ngl me gusta como se ven las tiras con color promedio. Atte: Mariano (el admin!) (no el de la serie de los 90s)")
#         media_id = carousel_id
#     else:
#         media_id = images_container_ids[0]

#     publish_media(access_token= ACCESS_TOKEN,
#                   media_id= media_id)
    
#     await delete_imgur_images(imgur_delete_hashes,
#                              client_id= IMGUR_CLIENT_ID)  


# async def only_the_delete_async_part():
#     IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
#     ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")

#     imgur_images = []
    
#     imgur_image_urls, imgur_delete_hashes = zip(*imgur_images)

#     await delete_imgur_images(imgur_delete_hashes,
#                              client_id= IMGUR_CLIENT_ID)

if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(main_but_imgur_has_been_run())
    # asyncio.run(main_but_the_media_containers_have_been_created())
    # asyncio.run(only_the_delete_async_part())