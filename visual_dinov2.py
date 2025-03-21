import torch
import numpy
import numpy as np
from torchvision.models.feature_extraction import create_feature_extractor
from pathlib import Path
from PIL import Image
import cv2 
from torchvision import transforms

def plot_pca( pca_image: numpy.ndarray, save_dir: str, last_components_rgb: bool = False,
             save_resized=False, save_prefix: str = ''):
    """
    finding pca of a set of images.
    :param pil_image: The original PIL image.
    :param pca_image: A numpy tensor containing pca components of the image. HxWxn_components
    :param save_dir: if None than show results.
    :param last_components_rgb: If true save last 3 components as RGB image in addition to each component separately.
    :param save_resized: If true save PCA components resized to original resolution.
    :param save_prefix: optional. prefix to saving
    :return: a list of lists containing an image and its principal components.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(exist_ok=True, parents=True)
    h,w = pca_image.shape
    comp = pca_image
    comp_min = comp.min(axis=(0, 1))
    comp_max = comp.max(axis=(0, 1))
    comp_img = (comp - comp_min) / (comp_max - comp_min)
    comp_img = (comp_img * 255).astype(np.uint8)
    heatmap_color = cv2.applyColorMap(comp_img, cv2.COLORMAP_JET)
    heatmap_color = cv2.resize(heatmap_color, (w*14,h*14))
    return heatmap_color
     

if __name__ == "__main__":
    # Import necessary modules and functions
    from dinov2.dinov2.models import build_model_from_cfg
    from easydict import EasyDict as edict
    from dinov2.dinov2.utils.config import get_cfg
    from dinov2.dinov2.utils.utils import load_pretrained_weights

    # Set the device to CUDA
    DEVICE = "cuda" 

    # Load the configuration for the model
    cfg = get_cfg("dinov2/dinov2/configs/eval/vits14_pretrain.yaml")

    # Build the model from the configuration
    model, _, embed_dim = build_model_from_cfg(cfg, only_teacher=False)

    # Load the pretrained weights into the model
    load_pretrained_weights(model, 'weights/dinov2_vits14.pth', checkpoint_key="teacher")

    # Move the model to the specified device and set it to evaluation mode
    model.to(device=DEVICE).eval()
    
    # Open the target image and convert it to RGB
    pil_image = Image.open("data/demos/target.png").convert('RGB')

    # Define the preprocessing steps
    prep = transforms.Compose([
        transforms.Resize((448, 448)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
    ])

    # Apply the preprocessing to the image and add a batch dimension
    input_tensor = prep(pil_image)[None, ...].cuda()

    # Import PCA from sklearn
    from sklearn.decomposition import PCA
    # dict_keys(['x_norm_clstoken', 'x_norm_patchtokens', 'x_prenorm', 'masks'])
    
    # Get the model output
    out = model(input_tensor, is_training=True)

    # Extract the patch token descriptors from the model output
    descriptors = out["x_norm_patchtokens"].cpu().detach().numpy()

    # Perform PCA on the descriptors to reduce dimensionality to 1 component
    pca = PCA(n_components=1).fit(descriptors[0])

    # Transform the descriptors using the PCA model
    img_pca = pca.transform(descriptors[0])

    # Plot the PCA result and save the heatmap image
    heatmap_color = plot_pca(img_pca.reshape((448 // 14, 448 // 14)), save_dir="./")
    cv2.imwrite("heatmap.jpg", heatmap_color)