<div align="center">

<h1>POPE: 6-DoF Promptable Pose Estimation of Any Object, in Any Scene, with One Reference</h1>

[![Project Page](https://img.shields.io/badge/POPE-Project-blue?logo=googlechrome&logoColor=blue)](https://paulpanwang.github.io/POPE/)
[![Paper](https://img.shields.io/badge/cs.CV-Paper-b31b1b?logo=arxiv&logoColor=red)](https://arxiv.org/abs/2305.15727)


<div>
        <a href="https://zhiwenfan.github.io/">Zhiwen Fan</a><strong><sup>1,*</sup></strong>,
        <a href="https://paulpanwang.github.io/">Panwang Pan</a><strong><sup>2,*</sup></strong>,
        <a href="https://peihaowang.github.io/">Peihao Wang</a><strong><sup>1</sup></strong>,
        <a href="https://yifanjiang19.github.io/">Yifan Jiang</a><strong><sup>1</sup></strong>, <br>
        <a href="https://ir1d.github.io/">Dejia Xu</a><strong><sup>1</sup></strong>,
        <a href="https://hwjiang1510.github.io/">Hanwen Jiang</a><strong><sup>1</sup></strong>, 
        <a href="https://vita-group.github.io/">Zhangyang Wang</a><strong><sup>1</sup></strong>
</div>
 <div>
    <sup>1</sup>The University of Texas at Austin &emsp;
    <sup>2</sup>ByteDance &emsp; 
         <sup>*</sup>denotes equal contribution
</div>

<img src="docs/static/imgs/teaser.png" width="100%"/>

</div>
<img src="docs/static/media/MOUSE_G1_adjusted_compressed.e9504417d415b735e684.gif" width="100%"/>
<strong> Welcome to the project repository for POPE (Promptable Pose Estimation), a state-of-the-art technique for 6-DoF pose estimation of any object in any scene using a single reference.</strong>



## Preparation

### Installation

#### Docker setup
Please check [docker/README.MD](docker/README.md)

OR you can follow the steps below:

The code is tested with python 3.9, cuda == 11.3, pytorch == 1.10.1. Additionally dependencies include: 

```bash
h5py
kornia
torch
torchvision
omegaconf
torchmetrics==0.10.3
fvcore
iopath
submitit
pathlib
transforms3d
numpy
plyfile
easydict
scikit-image
matplotlib
pyyaml
tabulate
numpy
tqdm
loguru
opencv-python
--extra-index-url https://pypi.nvidia.com
```

```bash
pip3 install -r ./requirements.txt
```

### Download model checkpoints
download SegmentAnything Model to weights
```bash
wget   https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth  -O weights/sam_vit_h_4b8939.pth
```

download DINOv2 Model to weights
```bash
wget  https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_pretrain.pth -O   weights/dinov2_vits14.pth
```


### Prepare datasets (Updated dataset [download links](https://huggingface.co/datasets/paulpanwang/POPE_Dataset))

Download  datasets from the Hugging Face Website: download OnePose/OnePose_LowTexture datasets from [here](https://huggingface.co/datasets/paulpanwang/POPE_Dataset/tree/main) YCB-Video and LINEMOD dataset from [here](https://huggingface.co/datasets/paulpanwang/POPE_Dataset/tree/main), and extract them into `./data`. 

* LM_dataset: https://huggingface.co/datasets/paulpanwang/POPE_Dataset/resolve/main/LM_dataset.zip
* onepose: https://huggingface.co/datasets/paulpanwang/POPE_Dataset/resolve/main/onepose.zip
* onepose_plusplus: https://huggingface.co/datasets/paulpanwang/POPE_Dataset/resolve/main/onepose_plusplus.zip
* ycbv: https://huggingface.co/datasets/paulpanwang/POPE_Dataset/resolve/main/ycbv.zip



~~If you want to evaluate on LINEMOD dataset, download the real training data, test data and 3D object models from [CDPN](https://github.com/LZGMatrix/CDPN_ICCV2019_ZhigangLi), and detection results by YOLOv5 from [here](https://zjueducn-my.sharepoint.com/:u:/g/personal/12121064_zju_edu_cn/EdodUdKGwHpCuvw3Cio5DYoBTntYLQuc7vNg9DkytWuJAQ?e=sAXp4B). Then extract them into `./data`~~

The directory should be organized in the following structure:
```
    |--📂data
    |       |--- 📂ycbv
    |       |--- 📂OnePose_LowTexture
    |       |--- 📂demos
    |       |--- 📂onepose
    |       |--- 📂LM_dataset
    |       |      |--- 📂bbox_2d
    |       |      |--- 📂corlor
    |       |      |--- 📂color_full
    |       |      |--- 📂intrin
    |       |      |--- 📂intrin_ba
    |       |      |--- 📂poses_ba
    |       |      |--- 📜box3d_corners.txt
    
```


### Demos
<div>

<strong style="color:red">
Thank you for your attention, and I apologize for the excessive use of hard-coded values in the code. We have now organized the code structure and README to make it more user-friendly.  

The code has been recently tidied up for release and could perhaps contain tiny bugs. Please feel free to open an issue.
</strong>
</div>

```bash
bash demo.sh
# Demo1: visual DINOv2 feature
python3 visual_dinov2.py

# Demo2: visual Segment Anything Model
python3 visual_sam.py
# Demo2: visual 3D BBox
python3 visual_3dbbox.py
```


<img src="docs/static/media/lm1_adjusted_compressed.0c024804c5097f6284bd.gif" width="100%"/>


### Evaluation
```bash
python3 eval_linemod_json.py
python3 eval_onepose_json.py
python3 eval_ycb_json.py
```

### Zero-shot Promtable Pose Estimation

Some Visual Examples of Promptable Object Pose Estimation Test Cases on Outdoor, indoor and scene with severe occlutions.


We also conduct a more challenging evaluation using an edge map as the reference,
which further demonstrates the robustness of POPE([DINOv2](https://github.com/paulpanwang/POPE/tree/main/dinov2) and [Matcher](https://github.com/paulpanwang/POPE/blob/main/src/matcher.py)).
<div>
  <img src="data/demos/match.png" width="100%"/>
</div>

### Application on Novel View Synthesis

We show the Application of Novel View Synthesis, by leveraging the estimated object poses, our method generate photo-realistic rendering results. we employ the estimated
 multi-view poses obtained from our POPE model, in combi nation with a pre-trained and generalizable Neural Radiance
 Field ([GNT](https://github.com/VITA-Group/GNT) and [Render](https://github.com/paulpanwang/POPE/tree/main/src/novel_view_render.py)) 
<div>
 <img src="docs/static/imgs/novel-view.png" width="100%"/>
</div>

### Comparison based on Video and Image

We show Visualizations on LINEMOD, YCB-Video, OnePose and OnePose++ datasets, with the comparison with LoFTR and Gen6D.


## Citation

If you find this repo is helpful, please consider citing:
```bibtex
@article{fan2023pope,
  title={POPE: 6-DoF Promptable Pose Estimation of Any Object, in Any Scene, with One Reference},
  author={Fan, Zhiwen and Pan, Panwang and Wang, Peihao and Jiang, Yifan and Xu, Dejia and Jiang, Hanwen and Wang, Zhangyang},
  journal={arXiv preprint arXiv:2305.15727},
  year={2023}
}

```
