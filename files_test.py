import os

with open("Keys.nosync/imgur_client_id.txt", "r") as file:
    imgur = file.read()
    
print(imgur)

print(os.listdir("Memes.nosync/"))