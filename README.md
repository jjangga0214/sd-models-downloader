# Stable Diffusion Models Auto Downloader

Jupyter notebook for easily downloading Stable Diffusion models (e.g. checkpoints, VAEs, LoRAs, etc).

This notebook is developed to use services like [runpod.io](https://runpod.io) more conveniently.

But in fact, you can use this notebook in **any environments** (local machine, cloud server, Colab, etc).

## Features

- Automatic convert normal page URL to download URL
- Support Any Project (e.g. stable-diffusion-webui, ComfyUI, etc)
- Automatic Preview Image Download
- Custom Download URL
- Support sub-directory

## Usage

### Step 1

Just simply clone the project

```bash
git clone https://github.com/jjangga0214/sd-models-downloader.git
```

Then open the Jupyter Notebook `sd-models-downloader/index.ipynb`.

### Step 2

A section like the screenshot below would appear.

![./images/1.png](./images/1.png)

Execute the cell.

### Step 3

Now the UI is generated. **(The screenshot below is just part of the whole page.)**

There're sections for Checkpoints, VAEs, Textual Inversions, Hyper Networks, LoRA, LyCORIS, ContrnolNet (v1.0, v1.1), T2I-Adapter, CoAdapter.

![./images/2.png](./images/2.png)

### Step 4

As the UI page (output of the cell) is long, it may be trimmed.
In that case, click the message like the screenshot below.
It will be at the end of the UI.
Then the full UI will be shown.

![./images/3.png](./images/3.png)

### Step 5

Now it's time to download. Simply execute the cell!

![./images/4.png](./images/4.png)

When you notice you need more models later, then just change the model selection and execute it again.

## License

MIT License. Copyright © 2023, GIL B. Chan <github.com/jjangga0214> <bnbcmindnpass@gmail.com>
