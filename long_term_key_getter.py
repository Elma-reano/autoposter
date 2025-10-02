
from graph_api import get_long_term_access_token
from file_operator import get_txt_file_contents, write_txt_file_contents
from cache_code import cache_handler

META_CLIENT_ID = get_txt_file_contents("Keys/meta_client_id.txt")
META_CLIENT_SECRET = get_txt_file_contents("Keys/meta_client_secret.txt")
META_CURRENT_ACCESS_TOKEN = get_txt_file_contents("Keys/meta_current_access_token.txt")

@cache_handler("GetNewLongTermAccessToken main")
def main():
    
    meta_client_id = META_CLIENT_ID
    meta_client_secret = META_CLIENT_SECRET
    current_meta_access_token = META_CURRENT_ACCESS_TOKEN
    new_long_term_access_token = get_long_term_access_token(cliend_id= meta_client_id,
                                                            client_secret= meta_client_secret,
                                                            current_access_token= current_meta_access_token)
    
    write_txt_file_contents("Keys/meta_long_term_access_token.txt", new_long_term_access_token)
    print("New Long Term Access Token Generated and Saved Successfully.")
    return new_long_term_access_token

if __name__ == "__main__":
    main()
    
