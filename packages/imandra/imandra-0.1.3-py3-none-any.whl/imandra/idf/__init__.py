import os.path 
import requests
import urllib

from .decomposition import Decomposition
from .exception import process_errors

API = "https://www.imandra.ai/"
TOKEN = "~/.imandra/login_token"

def decompose(code, api_url=None, auth_token_file=None):
    # Get auth token
    if auth_token_file == None:
        auth_token_file = os.path.expanduser(TOKEN)
    with open(auth_token_file, "r") as f:
        headers = {'X-Auth': f.read().strip()}

    if api_url == None:
        api_url = API

    r = requests.post\
      ( os.path.join(api_url, "api/ipl-worker/enqueue_py")
      , data = code
      , headers = headers
      )
    job_hash = process_errors(r)

    return Decomposition(job_hash, api_url, headers)
   


