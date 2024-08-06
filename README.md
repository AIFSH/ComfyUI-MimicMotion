# ComfyUI-MimicMotion

A custom node for ComfyUI used for [MimicMotion](https://github.com/Tencent/MimicMotion) implementation.

![Demo Image](https://github.com/user-attachments/assets/915ffdd5-b97d-4d79-b047-37fc3558a93d)

[Workflow Example](./doc/mimicmotion_workflow.json)

## Parameter Description

- **ref_image**: Path to the reference image used for generating the video. This option accepts an image input.
- **ref_video_path**: Path to the reference video file. This option accepts a video file path.
- **resolution**: The height of the output video (in pixels), with the width calculated automatically.
- **sample stride**: Sample stride, controlling the density of frames sampled from the video. Adjusting this value affects the smoothness of the generated video.
- **tile size**: Tile size, specifying the size of each block when processing in chunks. Optimizes processing speed and memory usage.
- **tile overlap**: Tile overlap, controlling the overlap area between adjacent blocks to reduce artifacts at block boundaries.
- **decode chunk size**: Decode chunk size, controlling the amount of data processed each time during decoding. Optimizes decoding efficiency.
- **num inference steps**: Number of inference steps, specifying the number of steps required to generate the video. Increasing this value improves the video quality but also increases computation time.
- **guidance scale**: Guidance scale, controlling the degree of guidance when generating the video. A larger value makes the generated video closer to the reference image.
- **fps**: Frame rate, setting the number of frames per second for the generated video. The default value is 15. Ensure the uploaded video has the same frame rate to avoid slow or fast motion effects.
- **seed**: Random seed, used to control the randomness of video generation. The default value is 42. Setting the random seed ensures reproducibility of the generated video.
- **control_after_generate**: Control after generation, set to "randomize" for post-generation randomization to increase diversity.

## Example

### Test Environment
- 2080ti 11GB
- torch==2.3.0+cu121
- python 3.10.8

### Input

#### Reference Image
![Reference Image](./doc/demo1.jpg)

#### Reference Video

### Output

https://github.com/Tencent/MimicMotion/assets/149982694/940a4aa0-a174-48e6-add7-96bb74ea916e

## How to Use

### Ensure `ffmpeg` Works in Your Command Line

#### For Linux
```sh
apt update
apt install ffmpeg
```

#### For Windows
You can install `ffmpeg` automatically using [WingetUI](https://github.com/marticliment/WingetUI).

### Installation Steps

1. Install xformers matching your torch version, e.g., torch==2.1.0+cu121
```sh
pip install xformers==0.0.22.post7
```

2. Clone this repository in the custom_nodes directory of ComfyUI
```sh
git clone https://github.com/AIFSH/ComfyUI-MimicMotion.git
cd ComfyUI-MimicMotion
pip install -r requirements.txt
```

The weights will be downloaded from Huggingface.

## Tutorial

- [MimicMotion! ComfyUI Plugin on Bilibili](https://b23.tv/McnRUpd)
- QQ Group: 852228202

## Thanks

Thanks to [MimicMotion](https://github.com/Tencent/MimicMotion) for the support.