# ComfyUI-MimicMotion

ComfyUI 的自定义节点，用于 [MimicMotion](https://github.com/Tencent/MimicMotion) 的实现。

![演示图像](https://github.com/user-attachments/assets/915ffdd5-b97d-4d79-b047-37fc3558a93d)

[工作流示例](./doc/mimicmotion_workflow.json)

## 参数说明

- **ref image**: 参考图像路径，用于指定生成视频的参考图像。该选项接受一个图像输入。
- **ref_video_path**: 参考视频路径，用于指定参考的视频文件。该选项接受一个视频文件路径。
- **resolution**: 输出视频的高度（以像素为单位），宽度自动计算。
- **sample stride**: 采样步幅，控制从视频中采样帧的密度。调整该值可以影响视频的流畅度。
- **tile size**: 分片大小，指定分块处理时每个块的大小，优化处理速度和内存使用。
- **tile overlap**: 瓦片重叠，控制相邻块之间的重叠区域，以减少块边界的伪影。
- **decode chunk size**: 解码块大小，控制解码时每次处理的数据量大小，优化解码效率。
- **num inference steps**: 推理步骤数量，生成视频时的推理步骤数。增加该值可以提高生成视频的质量，但也会增加计算时间。
- **guidance scale**: 引导比例，控制生成视频时的引导程度。该值越大，生成的视频越接近参考图像。
- **fps**: 帧率，设置生成视频的每秒帧数，默认值为15。确保上传的视频帧数与此一致，否则可能会出现慢动作或加速效果。
- **seed**: 随机种子，用于生成视频的随机性控制，默认值为42。设置随机种子可以保证生成视频的可重复性。
- **control_after_generate**: 生成后控制，设置为"randomize"表示生成后进行随机化处理，以增加多样性。

## 示例

### 测试环境
- 2080ti 11GB
- torch==2.3.0+cu121
- python 3.10.8

### 输入

#### 参考图像
![参考图像](./doc/demo1.jpg)

#### 参考视频

### 输出

https://github.com/Tencent/MimicMotion/assets/149982694/940a4aa0-a174-48e6-add7-96bb74ea916e

## 使用方法

### 确保 `ffmpeg` 可以在命令行中使用

#### 对于 Linux
```sh
apt update
apt install ffmpeg
```

#### 对于 Windows
可以通过 [WingetUI](https://github.com/marticliment/WingetUI) 自动安装 `ffmpeg`。

### 安装步骤

1. 安装与您的 torch 版本匹配的 xformers，例如 torch==2.1.0+cu121
```sh
pip install xformers==0.0.22.post7
```

2. 在 ComfyUI 的 custom_nodes 目录中克隆此仓库
```sh
git clone https://github.com/AIFSH/ComfyUI-MimicMotion.git
cd ComfyUI-MimicMotion
pip install -r requirements.txt
```

权重文件将从 Huggingface 下载。

## 教程

- [MimicMotion! ComfyUI 插件来了-哔哩哔哩](https://b23.tv/McnRUpd)
- QQ 群：852228202

## 致谢

感谢 [MimicMotion](https://github.com/Tencent/MimicMotion) 提供的支持。