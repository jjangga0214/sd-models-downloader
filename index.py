import ipywidgets as widgets
from utils import parse_url 

class Item:
  def __init__(self, *, display_name, url, dest, filename = None):
    self.display_name = display_name
    self.url = url # download url
    self.dest = dest # dir 
    self.filename = filename

def section(*, title, description, store, items = [], textarea_desc='', textarea_placeholder='', textarea = False,  check_all = False):
  display(widgets.HTML(f'<h2>{title}</h2>'))
  display(widgets.HTML(f'<p>{description}</p>'))
  if items:
    check_all_box = widgets.Checkbox(
        value = check_all,
        description = 'Check All',
        disabled = False,
      )
    display(check_all_box)

  check_boxes = []

  def checkbox(item):
    checkbox = widgets.Checkbox(
      value = False,
      layout = widgets.Layout(width="100%"),
      description = item.display_name,
      disabled = False,
    )
    def on_click(event):
      if event['new'] is True: # Do not refactor to `if event['new']:`. It will fail.
        store.add(item)
        for box in check_boxes:
          if box.value is False:
            return
        check_all_box.value = True
      elif event['new'] is False:
        check_all_box.value = False
        store.remove(item)
    checkbox.observe(on_click)
    display(checkbox)
    return checkbox
  
  for item in items:
    box = checkbox(item)
    if check_all:
      box.value = True
    check_boxes.append(box)
  if items:
    def check_all_on_click(event):
      # Do not refactor to `item.value = event['name'] == '_property_lock' and event['new'].get('value') is True`.
      # event occurs multiple times with different values per click.
      if event['name'] == '_property_lock' and event['new'].get('value') is True:
        for box in check_boxes:
          box.value = True
      elif event['name'] == '_property_lock' and event['new'].get('value') is False:
        for box in check_boxes:
          box.value = False
    check_all_box.observe(check_all_on_click)

  if textarea:
    display(widgets.HTML(f'<h4>Custom URLs</h4>'))
    if textarea_desc:
      display(widgets.HTML(f'<p>{textarea_desc}</p>'))
    textarea_box = widgets.Textarea(
      layout=widgets.Layout(width="100%", height='125px'),
      placeholder=textarea_placeholder,
      disabled=False)
    display(textarea_box)
    return textarea_box

def render(store):

  checkpoint_list = [
    Item(display_name = 'v1-5-pruned-emaonly (4.27 GB)',
         url = f'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors',
         dest = 'models/Stable-diffusion/'),
    Item(display_name = 'v1-5-pruned (7.7 GB)',
         url = f'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors',
         dest = 'models/Stable-diffusion/'),
    Item(display_name = 'sd-v1-5-inpainting (4.27 GB)',
         url = f'https://huggingface.co/runwayml/stable-diffusion-inpainting/resolve/main/sd-v1-5-inpainting.ckpt',
         dest = 'models/Stable-diffusion/'),
    Item(display_name = 'sd_xl_base_1.0 (6.94 GB)',
         url = f'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors',
         dest = 'models/Stable-diffusion/'),
    Item(display_name = 'sd_xl_refiner_1.0 (6.08 GB)',
         url = f'https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors',
         dest = 'models/Stable-diffusion/'),
  ]

  textarea_desc = 'You can also paste multiple model URLs into textarea below from civitai.com or huggingface.co. '
  textarea_desc += 'For example, <a href="https://civitai.com/models/20282" target="_blank" style="color: blue; text-decoration:underline;">https://civitai.com/models/20282</a> means the latest version of "Henmix_Real" model. '
  textarea_desc += 'On the other hand, <a href="https://civitai.com/models/20282?modelVersionId=58992" target="_blank" style="color: blue; text-decoration:underline;">https://civitai.com/models/20282?modelVersionId=58992</a> means v3.0 of "Henmix_Real" model. '
  textarea_desc += 'From civitai.com or huggingface.co, just copy and paste the model url from browser. '
  textarea_desc += 'You can also list url not from civitai.com or huggingface.co, but you should input the url of raw file. '
  textarea_desc += 'Multiple URLs should be separated by newlines (not comma). '
  textarea_desc += 'Note that any sentence following after "##" is treated as comment.'
  textarea_desc += 'So ignored when parsing URL, but useful for taking memo (e.g. model name).'

  checkpoint_textarea = section(title = 'Checkpoints', 
                                description = 'This downloads checkpoints into models/Stable-diffusion/',
                                items = checkpoint_list, 
                                textarea = True,
                                textarea_desc = textarea_desc,
                                textarea_placeholder = '''Example:
https://civitai.com/models/20282?modelVersionId=58992 ## Henmix_Real v3.0
https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/blob/main/sd-v1-4-full-ema.ckpt
https://civitai.com/models/33918 ## Shampoo Mix latest version''',
                                store = store)
  checkpoint_textarea.dest = 'models/Stable-diffusion/'

  vae_list = [
    Item(display_name = 'vae-ft-ema-560000-ema-pruned (335 MB)',
         url = 'https://huggingface.co/stabilityai/sd-vae-ft-ema-original/resolve/main/vae-ft-ema-560000-ema-pruned.safetensors',
         dest = 'models/VAE/'),
    Item(display_name = 'vae-ft-mse-840000-ema-pruned (335 MB)',
         url = 'https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors',
         dest = 'models/VAE/'),
    Item(display_name = 'kl-f8-anime2 (405 MB)',
         url = 'https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt',
         dest = 'models/VAE/'),     
    Item(display_name = 'sdxl_vae (335 MB)',
         url = 'https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors',
         dest = 'models/VAE/'),
  ]

  vae_textarea = section(title = 'VAEs', 
                         description = 'This downloads models into models/VAE/',
                         items = vae_list, 
                         textarea = True,
                         textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
                         store = store)
  vae_textarea.dest = 'models/VAE/'
  
  textual_inversion_list = [
    Item(display_name = 'bad_prompt.pt',
         url = 'https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt.pt',
         dest = 'embeddings/'),
    Item(display_name = 'bad_prompt_version2.pt',
         url = 'https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt',
         dest = 'embeddings/'),
    Item(display_name = 'EasyNegative.safetensors',
         url = 'https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors',
         dest = 'embeddings/'),
    Item(display_name = 'badhandv4',
         url = 'https://civitai.com/api/download/models/20068',
         dest = 'embeddings/'),
    Item(display_name = 'negative_hand-neg.pt',
         url = 'https://civitai.com/api/download/models/60938',
         dest = 'embeddings/'),
    Item(display_name = 'ng_deepnegative_v1_75t.pt',
         url = 'https://civitai.com/api/download/models/5637',
         dest = 'embeddings/'),
    Item(display_name = 'ulzzang-6500.pt',
         url = 'https://huggingface.co/yesyeahvh/ulzzang-6500/resolve/main/ulzzang-6500.pt',
         dest = 'embeddings'),
    Item(display_name = 'pureerosface_v1.pt',
         url = 'https://civitai.com/api/download/models/5119',
         dest = 'embeddings/'),
  ]

  textual_inversion_textarea = section(title = 'Textual Inversions', 
                                       description = 'This downloads Textual Inversions (Embeddings) into embeddings/',
                                       items = textual_inversion_list, 
                                       textarea = True,
                                       textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
                                       store = store) 
  textual_inversion_textarea.dest = 'models/embeddings/'
  
  hyper_network_textarea = section(title = 'Hyper Networks', 
                                   description = 'This downloads Hyper Networks into models/hypernetworks/',
                                   textarea = True,
                                   textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
                                   store = store)
  hyper_network_textarea.dest = 'models/hypernetworks/'

  lora_textarea = section(title = 'LoRA', 
                          description = 'This downloads LoRA into models/Lora/',
                          textarea = True,
                          textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
                          store = store)
  lora_textarea.dest = 'models/Lora/'
  
  lycoris_textarea = section(title = 'LyCORIS', 
                             description = 'This downloads LyCORIS into models/LyCORIS/',
                             textarea = True,
                             textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
                             store = store)
  lycoris_textarea.dest = 'models/LyCORIS'

  controlnet_v1_0_list = [
    Item(display_name = display_name, 
         url = f'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/{filename}',
         dest = 'models/ControlNet/')
    for display_name, filename in [
      ('sd15_canny (5.71 GB)', 'control_sd15_canny.pth'),
      ('sd15_depth (5.71 GB)', 'control_sd15_depth.pth'),
      ('sd15_hed (5.71 GB)', 'control_sd15_hed.pth'),
      ('sd15_mlsd (5.71 GB)', 'control_sd15_mlsd.pth'),
      ('sd15_normal (5.71 GB)', 'control_sd15_normal.pth'),
      ('sd15_openpose (5.71 GB)', 'control_sd15_openpose.pth'),
      ('sd15_scribble (5.71 GB)', 'control_sd15_scribble.pth'),
      ('sd15_seg (5.71 GB)', 'control_sd15_seg.pth'),
    ]
  ]

  section(title = 'ControlNet v1.0', 
          description = 'This downloads models into models/ControlNet/',
          items = controlnet_v1_0_list, 
          store = store)

  controlnet_v1_1_list = [
    Item(display_name = display_name, 
         url = f'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/{filename}',
         dest = 'models/ControlNet/'
        ) 
    for display_name, filename in [
      ('v11e_sd15_ip2p (1.45 GB)', 'control_v11e_sd15_ip2p.pth'),
      ('v11e_sd15_shuffle (1.45 GB)', 'control_v11e_sd15_shuffle.pth'),
      ('v11f1e_sd15_tile (1.45 GB)', 'control_v11f1e_sd15_tile.pth'),
      ('v11f1p_sd15_depth (1.45 GB)', 'control_v11f1p_sd15_depth.pth'),
      ('v11p_sd15_canny (1.45 GB)', 'control_v11p_sd15_canny.pth'),
      ('v11p_sd15_inpaint (1.45 GB)', 'control_v11p_sd15_inpaint.pth'),
      ('v11p_sd15_lineart (1.45 GB)', 'control_v11p_sd15_lineart.pth'),
      ('v11p_sd15_mlsd (1.45 GB)', 'control_v11p_sd15_mlsd.pth'),
      ('v11p_sd15_normalbae (1.45 GB)', 'control_v11p_sd15_normalbae.pth'),
      ('v11p_sd15_openpose (1.45 GB)', 'control_v11p_sd15_openpose.pth'),
      ('v11p_sd15_scribble (1.45 GB)', 'control_v11p_sd15_scribble.pth'),
      ('v11p_sd15_seg (1.45 GB)', 'control_v11p_sd15_seg.pth'),
      ('v11p_sd15_softedge (1.45 GB)', 'control_v11p_sd15_softedge.pth'),
      ('v11p_sd15s2_lineart_anime (1.45 GB)', 'control_v11p_sd15s2_lineart_anime.pth'),
    ]
  ]

  section(title = 'ControlNet v1.1', 
          description = 'This downloads models into models/ControlNet/',
          items = controlnet_v1_1_list, 
          store = store, 
          check_all = True)

  t2i_adapter_list = [
    Item(display_name = display_name,
         url = f'https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/{filename}',
         dest = 'models/ControlNet/'
        ) 
    for display_name, filename in [
      ('canny_sd14v1 (308 MB)', 't2iadapter_canny_sd14v1.pth'),
      ('canny_sd15v2 (308 MB)', 't2iadapter_canny_sd15v2.pth'),
      ('color_sd14v1 (74.8 MB)', 't2iadapter_color_sd14v1.pth'),
      ('depth_sd14v1 (309 MB)', 't2iadapter_depth_sd14v1.pth'),
      ('depth_sd15v2 (309 MB)', 't2iadapter_depth_sd15v2.pth'),
      ('depth_sd15v2 (309 MB)', 't2iadapter_depth_sd15v2.pth'),
      ('keypose_sd14v1 (309 MB)', 't2iadapter_keypose_sd14v1.pth'),
      ('openpose_sd14v1 (309 MB)', 't2iadapter_openpose_sd14v1.pth'),
      ('seg_sd14v1 (309 MB)', 't2iadapter_seg_sd14v1.pth'),
      ('sketch_sd14v1 (308 MB)', 't2iadapter_sketch_sd14v1.pth'),
      ('sketch_sd15v2 (308 MB)', 't2iadapter_sketch_sd15v2.pth'),
      ('style_sd14v1 (154 MB)', 't2iadapter_style_sd14v1.pth'),
      ('zoedepth_sd15v1 (309 MB)', 't2iadapter_zoedepth_sd15v1.pth'),
    ]
  ]

  section(title = 'T2I-Adapter', 
          description = 'This downloads models models/ControlNet/',
          items = t2i_adapter_list, 
          store = store, 
          check_all = True)

  coadapter_list = [
    Item(display_name = display_name, 
         url = f'https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/{filename}',
         dest = 'models/ControlNet/'
        ) 
    for display_name, filename in [
      ('canny-sd15v1 (308 MB)', 'coadapter-canny-sd15v1.pth'),
      ('color-sd15v1 (74.8 MB)', 'color-coadapter-sd15v1.pth'),
      ('depth-sd15v1 (309 MB)', 'coadapter-depth-sd15v1.pth'),
      ('fuser-sd15v1 (109 MB)', 'coadapter-fuser-sd15v1.pth'),
      ('sketch-sd15v1 (308 MB)', 'coadapter-sketch-sd15v1.pth'),
      ('style-sd15v1 (154 MB)', 'coadapter-style-sd15v1.pth'),
    ]
  ]

  section(title = 'CoAdapter',
          description = '''This downloads models into models/ControlNet/.
          Note that currently sd-webui-controlnet does not support CoAdapter.
          (REF: <a href="http://https://github.com/Mikubill/sd-webui-controlnet/issues/614" target="_blank" style="color: blue; text-decoration:underline;">https://github.com/Mikubill/sd-webui-controlnet/issues/614).</a>''',
          items = coadapter_list, 
          store = store)

  textareas = {
    'checkpoint': checkpoint_textarea,
    'vae': vae_textarea,
    'textual_inversion': textual_inversion_textarea,
    'hyper_network': hyper_network_textarea,
    'lora': lora_textarea,
    'lycoris': lycoris_textarea,
  }

  return textareas

def parse_textarea(*, textarea, dest, store):
  lines = textarea.value.split('\n')
  for line in lines:
    comment_idx = line.find('##')
    if comment_idx != -1:
      url = line[:comment_idx]
    else:
      url = line
    url = url.strip()
    if not url:
      continue
    download_url = parse_url(url)
    store.add(Item(
      display_name = None,
      url = download_url,
      dest = dest,
    ))
