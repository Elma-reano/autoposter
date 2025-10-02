def get_txt_file_contents(path):
    # TODO leer el archivo en chunks en caso de que sea muy grande
    with open(path, 'r') as file:
        contents = file.read()
    return contents

def save_txt_file_contents(path):
    with open(path, 'w') as file:
        file.write(contents)
    return