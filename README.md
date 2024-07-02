# ComfyUI-MimicMotion
a comfyui custom node for [MimicMotion](https://github.com/Tencent/MimicMotion)
[workflow](./doc/mimicmotion_workflow.json)

## Example
test on 2080ti 11GB torch==2.3.0+cu121 python 3.10.8
- input

refer_img
<div>
  <figure>
  <img src="./doc/demo1.jpg" width="600px"/>
  <figure>
</div>

refer_video

- output

https://github.com/Tencent/MimicMotion/assets/149982694/940a4aa0-a174-48e6-add7-96bb74ea916e

## How to use
make sure `ffmpeg` is worked in your commandline
for Linux
```
apt update
apt install ffmpeg
```
for Windows,you can install `ffmpeg` by [WingetUI](https://github.com/marticliment/WingetUI) automatically

then!
```
## insatll xformers match your torch,for torch==2.1.0+cu121
pip install xformers==0.0.22.post7

## in ComfyUI/custom_nodes
git clone https://github.com/AIFSH/ComfyUI-MimicMotion.git
cd ComfyUI-MimicMotion
pip install -r requirements.txt
```
weights will be downloaded from huggingface

## Tutorial
-【MimicMotion! ComfyUI插件来了-哔哩哔哩】 https://b23.tv/McnRUpd
- QQ群：852228202

## Thanks

[MimicMotion](https://github.com/Tencent/MimicMotion)
