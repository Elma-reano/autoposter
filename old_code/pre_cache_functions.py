
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