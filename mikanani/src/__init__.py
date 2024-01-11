from dotenv import load_dotenv, find_dotenv

# load dotenv file
try:
    load_dotenv(find_dotenv(raise_error_if_not_found=True), override=True)
except Exception as e:
    load_dotenv("/secret/.env", override=True)