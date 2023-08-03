import requests
from urllib.parse import urlparse, parse_qs
import time

def parse_civitai_url(url):
  parsed_url = urlparse(url)
  parsed_query = parse_qs(parsed_url.query)
  if parsed_query.get('modelVersionId'): # For URLs like https://civitai.com/models/20282?modelVersionId=58992
    endpoint = f'https://civitai.com/api/v1/model-versions/{parsed_query.get("modelVersionId")[0]}'
    get_file = lambda result: result['files'][0]
  else: # e.g. For URLs like https://civitai.com/models/20282
    is_models_dir_reached = False
    model_id = None
    for dir in parsed_url.path.split('/'): 
      if dir == 'models':
        is_models_dir_reached = True
        continue
      if is_models_dir_reached:
        model_id = dir
        break
    endpoint = f'https://civitai.com/api/v1/models/{model_id}'
    get_file = lambda result: result['modelVersions'][0]['files'][0]
  response = requests.get(endpoint)
  time.sleep(0.5) # for rate limiting
  response.raise_for_status()
  # access JSOn content
  result = response.json()
  file = get_file(result)
  download_url = file['downloadUrl']
  return download_url

# e.g. When url is 'https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/v1-5-pruned-emaonly.safetensors',
# Download_url is 'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors'
def parse_huggingface_url(url):
    parsed_url = urlparse(url)
    dirs = parsed_url.path.split('/') # dirs[0] is '' empty string
    dirs[3] = 'resolve'
    download_url = f'{parsed_url.scheme}://{parsed_url.netloc}{"/".join(dirs)}'
    return download_url

def parse_url(url):
  parsed_url = urlparse(url)
  if 'civitai.com' in parsed_url.netloc:
    return parse_civitai_url(url)
  elif 'huggingface.co' in parsed_url.netloc:
    return parse_huggingface_url(url)
  else:
    return url

