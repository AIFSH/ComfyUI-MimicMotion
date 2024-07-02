import os,sys
now_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(now_dir)

import math
import torch
# import logging
import cuda_malloc
import folder_paths
import numpy as np
from PIL import Image
from datetime import datetime
from omegaconf import OmegaConf
from huggingface_hub import snapshot_download
from moviepy.editor import VideoFileClip,AudioFileClip
from torchvision.transforms.functional import pil_to_tensor, resize, center_crop,to_pil_image

from mimicmotion.pipelines.pipeline_mimicmotion import MimicMotionPipeline
from mimicmotion.utils.loader import create_pipeline
from mimicmotion.utils.utils import save_to_mp4

# logging.basicConfig(level=logging.INFO, format="%(asctime)s: [%(levelname)s] %(message)s")
# logger = logging.getLogger(__name__)
device = torch.device("cuda" if cuda_malloc.cuda_malloc_supported() else "cpu")

input_path = folder_paths.get_input_directory()
output_dir = folder_paths.get_output_directory()
ckpt_dir = os.path.join(now_dir, "models")
svd_dir = os.path.join(ckpt_dir,"stable-video-diffusion-img2vid-xt-1-1")
ASPECT_RATIO = 9 / 16
# yzd-v/DWPose
os.environ["dwpose"] = os.path.join(ckpt_dir,"DWPose")
snapshot_download(repo_id="yzd-v/DWPose",local_dir=os.environ["dwpose"],
                    allow_patterns=["dw-ll_ucoco_384.onnx","yolox_l.onnx"])

from mimicmotion.dwpose.preprocess import get_video_pose, get_image_pose

class MimicMotionNode:
    def __init__(self) -> None:
        # weights/stable-video-diffusion-img2vid-xt-1-1
        snapshot_download(repo_id="weights/stable-video-diffusion-img2vid-xt-1-1",local_dir=svd_dir,
                          ignore_patterns=["svd_xt*"],allow_patterns=["*.json","*fp16*"])
        
        # ixaac/MimicMotion
        snapshot_download(repo_id="ixaac/MimicMotion",local_dir=ckpt_dir,
                          allow_patterns="*.pth")
        
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "ref_image":("IMAGE",),
                "ref_video_path":("VIDEO",),
                "resolution":([576,768],{
                    "default":576,
                }),
                "sample_stride":("INT",{
                    "default": 2
                }),
                "tile_size": ("INT",{
                    "default": 16
                }),
                "tile_overlap": ("INT",{
                    "default": 6
                }),
                "decode_chunk_size":("INT",{
                    "default": 8
                }),
                "num_inference_steps":  ("INT",{
                    "default": 25
                }),
                "guidance_scale":("FLOAT",{
                    "default": 2.0
                }),
                "fps": ("INT",{
                    "default": 15
                }),
                "seed": ("INT",{
                    "default": 42
                }),
            }
        }
    
    RETURN_TYPES = ("VIDEO",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "gen_video"

    #OUTPUT_NODE = False

    CATEGORY = "AIFSH_MimicMotion"

    @torch.no_grad()
    def gen_video(self,ref_image,ref_video_path,resolution,sample_stride,
                  tile_size,tile_overlap,decode_chunk_size,num_inference_steps,
                  guidance_scale,fps,seed):
        torch.set_default_dtype(torch.float16)
        infer_config = OmegaConf.load(os.path.join(now_dir,"test.yaml"))
        infer_config.base_model_path = svd_dir
        infer_config.ckpt_path = os.path.join(ckpt_dir,"MimicMotion.pth")
        pipeline = create_pipeline(infer_config,device)

        ############################################## Pre-process data ##############################################
        ref_image = ref_image.numpy()[0] * 255
        ref_image = ref_image.astype(np.uint8)
        ref_image = Image.fromarray(ref_image)
        pose_pixels, image_pixels = preprocess(
            ref_video_path, ref_image, 
            resolution=resolution, sample_stride=sample_stride
        )
        task_config = {
            "tile_size": tile_size,
            "tile_overlap": tile_overlap,
            "decode_chunk_size": decode_chunk_size,
            "num_inference_steps": num_inference_steps,
            "noise_aug_strength": 0,
            "guidance_scale": guidance_scale,
            "fps": fps,
            "seed": seed,
        }
        ########################################### Run MimicMotion pipeline ###########################################
        _video_frames = run_pipeline(
            pipeline, 
            image_pixels, pose_pixels, 
            device, task_config
        )
        ################################### save results to output folder. ###########################################
        outfile = f"{output_dir}/mimicmotion_{os.path.basename(ref_video_path).split('.')[0]}" \
                    f"_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        save_to_mp4(_video_frames,outfile,fps=fps,)
        if os.path.isfile(ref_video_path+".wav"):
            video_clip = VideoFileClip(outfile)
            audio_clip = AudioFileClip(ref_video_path+".wav")
            video_clip = video_clip.set_audio(audio_clip)
            outfile = f"{output_dir}/mimicmotion_{os.path.basename(ref_video_path).split('.')[0]}" \
                    f"_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            video_clip.write_videofile(outfile)
        return (outfile, )


class PreViewVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "video":("VIDEO",),
        }}
    
    CATEGORY = "AIFSH_MimicMotion"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_video"

    def load_video(self, video):
        video_name = os.path.basename(video)
        video_path_name = os.path.basename(os.path.dirname(video))
        return {"ui":{"video":[video_name,video_path_name]}}

class LoadVideo:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and f.split('.')[-1] in ["mp4", "webm","mkv","avi"]]
        return {"required":{
            "video":(files,),
        }}
    
    CATEGORY = "AIFSH_MimicMotion"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("VIDEO",)

    OUTPUT_NODE = False

    FUNCTION = "load_video"

    def load_video(self, video):
        video_path = os.path.join(input_path,video)
        video_clip = VideoFileClip(video_path)
        audio_path = os.path.join(input_path,video+".wav")
        try:
            video_clip.audio.write_audiofile(audio_path)
            print(f"bgm save at {audio_path}")
        except:
            print("none audio")
        return (video_path,)


def run_pipeline(pipeline: MimicMotionPipeline, image_pixels, pose_pixels, device, task_config):
    image_pixels = [to_pil_image(img.to(torch.uint8)) for img in (image_pixels + 1.0) * 127.5]
    pose_pixels = pose_pixels.unsqueeze(0).to(device)
    generator = torch.Generator(device=device)
    generator.manual_seed(task_config["seed"])
    frames = pipeline(
        image_pixels, image_pose=pose_pixels, num_frames=pose_pixels.size(1),
        tile_size=task_config["tile_size"], tile_overlap=task_config["tile_overlap"],
        height=pose_pixels.shape[-2], width=pose_pixels.shape[-1], fps=task_config["fps"],
        noise_aug_strength=task_config["noise_aug_strength"], num_inference_steps=task_config["num_inference_steps"],
        generator=generator, min_guidance_scale=task_config["guidance_scale"], 
        max_guidance_scale=task_config["guidance_scale"], decode_chunk_size=task_config['decode_chunk_size'], output_type="pt", device=device
    ).frames.cpu()
    video_frames = (frames * 255.0).to(torch.uint8)

    for vid_idx in range(video_frames.shape[0]):
        # deprecated first frame because of ref image
        _video_frames = video_frames[vid_idx, 1:]

    return _video_frames

def preprocess(video_path, image_pixels, resolution=576, sample_stride=2):
    """preprocess ref image pose and video pose

    Args:
        video_path (str): input video pose path
        image_pixels (Image): reference image pil
        resolution (int, optional):  Defaults to 576.
        sample_stride (int, optional): Defaults to 2.
    """
    # image_pixels = pil_loader(image_path)
    image_pixels = pil_to_tensor(image_pixels) # (c, h, w)
    h, w = image_pixels.shape[-2:]
    ############################ compute target h/w according to original aspect ratio ###############################
    if h>w:
        w_target, h_target = resolution, int(resolution / ASPECT_RATIO // 64) * 64
    else:
        w_target, h_target = int(resolution / ASPECT_RATIO // 64) * 64, resolution
    h_w_ratio = float(h) / float(w)
    if h_w_ratio < h_target / w_target:
        h_resize, w_resize = h_target, math.ceil(h_target / h_w_ratio)
    else:
        h_resize, w_resize = math.ceil(w_target * h_w_ratio), w_target
    image_pixels = resize(image_pixels, [h_resize, w_resize], antialias=None)
    image_pixels = center_crop(image_pixels, [h_target, w_target])
    image_pixels = image_pixels.permute((1, 2, 0)).numpy()
    ##################################### get image&video pose value #################################################
    image_pose = get_image_pose(image_pixels)
    video_pose = get_video_pose(video_path, image_pixels, sample_stride=sample_stride)
    pose_pixels = np.concatenate([np.expand_dims(image_pose, 0), video_pose])
    image_pixels = np.transpose(np.expand_dims(image_pixels, 0), (0, 3, 1, 2))
    return torch.from_numpy(pose_pixels.copy()) / 127.5 - 1, torch.from_numpy(image_pixels) / 127.5 - 1
