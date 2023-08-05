import ipywidgets as widgets
from utils import parse_url, File
import os

class Item:
  def __init__(self, *, display_name, file, dest = None, filename = None):
    self.display_name = display_name
    self.file = file # download url (FileUrl instance)
    self.dest = dest

class Section:
  def __init__(self, *, path, items, textarea = None):
    self.path = path
    self.items = items
    self.textarea = textarea

def section(
  *, 
  title, 
  store,
  default_path,
  description = None, 
  items = [], 
  textarea_desc = '', 
  textarea_placeholder = '', 
  textarea = False,  
  check_all = False):
  display(widgets.HTML(f'<h2>{title}</h2>'))
  if description:
    display(widgets.HTML(f'<p>{description}</p>'))

  display(widgets.HTML(f'<h4>Path<h4>'))
  path_text_input = widgets.Text(
    value = default_path,
    layout = widgets.Layout(width="92%"),
  )
  display(path_text_input)

  if items:
    display(widgets.HTML(f'<h4>Models<h4>'))
    check_all_box = widgets.Checkbox(
        value = check_all,
        description = 'Check All',
        disabled = False,
        layout=widgets.Layout(margin='0px', width = "92%")
      )
    display(check_all_box)

  check_boxes = []

  def checkbox(item):
    checkbox = widgets.Checkbox(
      value = False,
      layout = widgets.Layout(width="92%"),
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
      layout=widgets.Layout(width = "100%", height = '125px'),
      placeholder = textarea_placeholder,
      disabled = False)
    display(textarea_box)
    return Section(path = path_text_input, items = items, textarea = textarea_box )
  
  return Section(path = path_text_input, items = items)

def render(store):

  display(widgets.HTML(f'<h2>Project</h2>'))
  display(widgets.HTML(f'''<p>Check the project you use.<br/>
It will change <b>Root Path</b> and <b>Path</b> of each sections.
Think of it as a preset. Of course you can override each path manually.</p>'''))
  
  options = ['stable-diffusion-webui', 'ComfyUI', 'Others']
  platform_radio = widgets.RadioButtons(options = options)
  display(platform_radio)

  display(widgets.HTML(f'<h2>Root Path</h2>'))
  display(widgets.HTML(f'<p>Specity the root directory of the project (e.g. <b>stable-diffusin-wedui</b> or <b>ComfyUI</b>).</p>'))
  root_text_input = widgets.Text(value = '/workspace/stable-diffusion-webui/', layout = widgets.Layout(width="92%"),)
  display(root_text_input)

  checkpoint_list = [
    Item(display_name = 'v1-5-pruned-emaonly (4.27 GB)',
         file = File(url = f'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors',)),
    Item(display_name = 'v1-5-pruned (7.7 GB)',
         file = File(url = f'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors',)),
    Item(display_name = 'sd-v1-5-inpainting (4.27 GB)',
         file = File(url = f'https://huggingface.co/runwayml/stable-diffusion-inpainting/resolve/main/sd-v1-5-inpainting.ckpt',)),
    Item(display_name = 'sd_xl_base_1.0 (6.94 GB)',
         file = File(url = f'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors',)),
    Item(display_name = 'sd_xl_refiner_1.0 (6.08 GB)',
         file = File(url = f'https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors',)),
  ]

  textarea_desc = 'You can also paste multiple model URLs into textarea below from civitai.com or huggingface.co. '
  textarea_desc += 'For example, <a href="https://civitai.com/models/20282" target="_blank" style="color: blue; text-decoration:underline;">https://civitai.com/models/20282</a> means the latest version of "Henmix_Real" model. '
  textarea_desc += 'On the other hand, <a href="https://civitai.com/models/20282?modelVersionId=58992" target="_blank" style="color: blue; text-decoration:underline;">https://civitai.com/models/20282?modelVersionId=58992</a> means v3.0 of "Henmix_Real" model. '
  textarea_desc += 'From civitai.com or huggingface.co, just copy and paste the model url from browser. '
  textarea_desc += 'You can also list any url not from civitai.com or huggingface.co, but you should input the url of raw file. '
  textarea_desc += 'Multiple URLs should be separated by newlines (not comma). '
  textarea_desc += 'Note that any sentence following after "##" is treated as comment.'
  textarea_desc += 'So ignored when parsing URL, but useful for taking memo (e.g. model name).'

  checkpoint = section(
    title = 'Checkpoints', 
    default_path = 'models/Stable-diffusion/',
    items = checkpoint_list, 
    textarea = True,
    textarea_desc = textarea_desc,
    textarea_placeholder = '''Example:
https://civitai.com/models/20282?modelVersionId=58992 ## Henmix_Real v3.0
https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/blob/main/sd-v1-4-full-ema.ckpt
https://civitai.com/models/33918 ## Shampoo Mix latest version''',
    store = store)

  vae_list = [
    Item(display_name = 'vae-ft-ema-560000-ema-pruned (335 MB)',
         file = File(url = 'https://huggingface.co/stabilityai/sd-vae-ft-ema-original/resolve/main/vae-ft-ema-560000-ema-pruned.safetensors',)),
    Item(display_name = 'vae-ft-mse-840000-ema-pruned (335 MB)',
         file = File(url = 'https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors',)),
    Item(display_name = ' (405 MB)',
         file = File(url = 'https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt',)),     
    Item(display_name = 'sdxl_vae (335 MB)',
         file = File(url = 'https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors',)),
  ]

  vae = section(
    title = 'VAEs', 
    default_path = 'models/VAE/',
    items = vae_list, 
    textarea = True,
    textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
    store = store)
  
  textual_inversion_list = [
    Item(display_name = 'bad_prompt.pt',
         file = File(url = 'https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt.pt',)),
    Item(display_name = 'bad_prompt_version2.pt',
         file = File(url = 'https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt',
                       name='bad_prompt_version2.pt',
                       image='https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/0f12ec45-0d26-4e15-0bb1-6e23230d8700/width=450/bad_prompt_showcase.jpeg')),
    Item(display_name = 'EasyNegative.safetensors',
         file = File(url = 'https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors',
                       name='EasyNegative.safetensors',
                       image='https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/a2505a48-8eed-4b12-b6a0-6a8ec7e0c600/width=3387/sample01.jpeg')),
    Item(display_name = 'badhandv4',
         file = File(url = 'https://civitai.com/api/download/models/20068',
                       name='badhandv4.pt',
                       image='https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/45318cc7-231d-4d8a-044d-a081d0a40700/width=450/212048.jpeg')),
    Item(display_name = 'negative_hand-neg.pt',
         file = File(url = 'https://civitai.com/api/download/models/60938',
                       name='negative_hand-neg.pt',
                       image='https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/1de1b4da-e9eb-43bf-9e9c-050e51cbbb25/width=450/667878.jpeg')),
    Item(display_name = 'ng_deepnegative_v1_75t.pt',
         file = File(url = 'https://civitai.com/api/download/models/5637',
                       name='ng_deepnegative_v1_75t.pt',
                       image='https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/f7fe0b31-86a6-48ff-4fc2-906227af9300/width=450/45555.jpeg')),
    Item(display_name = 'ulzzang-6500.pt',
         file = File(url = 'https://huggingface.co/yesyeahvh/ulzzang-6500/resolve/main/ulzzang-6500.pt',)),
    Item(display_name = 'pureerosface_v1.pt',
         file = File(url = 'https://civitai.com/api/download/models/5119',
                       name='pureerosface_v1.pt',
                       image='https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/9fbf8bf0-aad7-4360-eeb0-3e2e09628900/width=450/110973.jpeg')),
  ]

  textual_inversion = section(
    title = 'Textual Inversions', 
    default_path = 'embeddings/',
    items = textual_inversion_list, 
    textarea = True,
    textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
    store = store) 
  
  hyper_network = section(
    title = 'Hyper Networks', 
    default_path = 'models/hypernetworks/',
    textarea = True,
    textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
    store = store)

  lora = section(
    title = 'LoRA', 
    default_path = 'models/Lora/',
    textarea = True,
    textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
    store = store)
  
  lycoris = section(
    title = 'LyCORIS', 
    default_path = 'models/LyCORIS/',
    textarea = True,
    textarea_desc = 'The rule is same as "Custom URLs" from "Checkpoints" section.',
    store = store)

  controlnet_v1_list = [
    Item(display_name = display_name, 
         file = File(url = f'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/{filename}'))
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

  controlnet_v1 = section(
    title = 'ControlNet v1.0', 
    default_path = 'models/ControlNet/',
    items = controlnet_v1_list, 
    store = store)

  controlnet_v1_1_list = [
    Item(display_name = display_name, 
         file = File(url = f'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/{filename}'))
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

  controlnet_v1_1 = section(
    title = 'ControlNet v1.1', 
    default_path = 'models/ControlNet/',
    items = controlnet_v1_1_list, 
    store = store)

  t2i_adapter_list = [
    Item(display_name = display_name,
         file = File(url = f'https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/{filename}',)) 
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

  t2i_adapter = section(
    title = 'T2I-Adapter', 
    default_path = 'models/ControlNet/',
    items = t2i_adapter_list, 
    store = store)

  coadapter_list = [
    Item(display_name = display_name, 
         file = File(url = f'https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/{filename}',))
    for display_name, filename in [
      ('canny-sd15v1 (308 MB)', 'coadapter-canny-sd15v1.pth'),
      ('color-sd15v1 (74.8 MB)', 'color-coadapter-sd15v1.pth'),
      ('depth-sd15v1 (309 MB)', 'coadapter-depth-sd15v1.pth'),
      ('fuser-sd15v1 (109 MB)', 'coadapter-fuser-sd15v1.pth'),
      ('sketch-sd15v1 (308 MB)', 'coadapter-sketch-sd15v1.pth'),
      ('style-sd15v1 (154 MB)', 'coadapter-style-sd15v1.pth'),
    ]
  ]

  coadapter = section(
    title = 'CoAdapter',
    default_path='models/ControlNet/',
    description = '''Note that currently sd-webui-controlnet does not support CoAdapter.
    (REF: <a href="http://https://github.com/Mikubill/sd-webui-controlnet/issues/614" target="_blank" style="color: blue; text-decoration:underline;">https://github.com/Mikubill/sd-webui-controlnet/issues/614).</a>''',
    items = coadapter_list, 
    store = store)

  sections = {
    'checkpoint': checkpoint,
    'vae': vae,
    'textual_inversion': textual_inversion,
    'hyper_network': hyper_network,
    'lora': lora,
    'lycoris': lycoris,
    'controlnet_v1': controlnet_v1,
    'controlnet_v1_1': controlnet_v1_1,
    't2i_adapter': t2i_adapter,
    'coadapter': coadapter,
  }

  def platform_radio_on_change(event):
    print("The value of the radio box is:", event)
    if event['new'] == 'stable-diffusin-webui':
      checkpoint.path.value = 'models/Stable-diffusion/'
      vae.path.value = 'models/VAE/'
      textual_inversion.path.value = 'embeddings/'
      hyper_network.path.value = 'models/hypernetworks/'
      lora.path.value = 'models/Lora/'
      lycoris.path.value = 'models/LyCORIS/'
      controlnet_v1.path.value = 'models/ControlNet/'
      controlnet_v1_1.path.value = 'models/ControlNet/'
      t2i_adapter.path.value = 'models/ControlNet/'
      coadapter.path.value = 'models/ControlNet/'
    if event['new'] == 'ComfyUI':
      checkpoint.path.value = 'models/checkpoints/'
      vae.path.value = 'models/vae'
      textual_inversion.path.value = 'models/embeddings/'
      hyper_network.path.value = 'models/hypernetworks/'
      lora.path.value = 'models/loras/'
      lycoris.path.value = 'models/loras/'
      controlnet_v1.path.value = 'models/controlnet/'
      controlnet_v1_1.path.value = 'models/controlnet/'
      t2i_adapter.path.value = 'models/controlnet/'
      coadapter.path.value = 'models/controlnet/'
    else:
      pass

  platform_radio.observe(platform_radio_on_change, names = ['value'])

  return root_text_input, sections

def parse_textarea(*, textarea, dest):
  lines = textarea.value.split('\n')
  items = []
  for line in lines:
    comment_idx = line.find('##')
    if comment_idx != -1:
      url = line[:comment_idx]
    else:
      url = line
    url = url.strip()
    if not url:
      continue
    file = parse_url(url)
    items.append(
      Item(
        display_name = None,
        file = file,
        dest = dest))
  return items
