import time
from urllib.parse import urlparse, parse_qs
import requests

class File: 
  def __init__(self, *, url, name=None, image=None): 
    self.url = url # model file url to download
    self.name = name # model file name
    self.image = image # preview image url

def parse_civitai_url(url):
  parsed_url = urlparse(url)
  parsed_query = parse_qs(parsed_url.query)
  if parsed_query.get('modelVersionId'): # For URLs like https://civitai.com/models/20282?modelVersionId=58992
    endpoint = f'https://civitai.com/api/v1/model-versions/{parsed_query.get("modelVersionId")[0]}'
    get_model = lambda result: result
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
    get_model = lambda result: result['modelVersions'][0] # get a model of specific(the latest) version
  response = requests.get(endpoint)
  time.sleep(0.5) # for rate limiting
  response.raise_for_status()
  # access JSON content
  result = response.json()
  model = get_model(result)
  image_url = model['images'][0]['url']
  return File(url=model['files'][0]['downloadUrl'], 
              name=model['files'][0]['name'],
              image=image_url)

# e.g. When url is 'https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/v1-5-pruned-emaonly.safetensors',
# Download_url is 'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors'
def parse_huggingface_url(url):
    parsed_url = urlparse(url)
    dirs = parsed_url.path.split('/') # dirs[0] is '' empty string
    dirs[3] = 'resolve'
    file_url = f'{parsed_url.scheme}://{parsed_url.netloc}{"/".join(dirs)}'
    return FileUrl(url=file_url,)

def parse_url(url):
  parsed_url = urlparse(url)
  if 'civitai.com' in parsed_url.netloc:
    return parse_civitai_url(url)
  elif 'huggingface.co' in parsed_url.netloc:
    return parse_huggingface_url(url)
  else:
    return File(url=url,)

