# %load_ext autoreload
# %autoreload 2

import os
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils import data
from torchvision import transforms, utils
from tqdm import tqdm
torch.backends.cudnn.benchmark = True
import copy
from util import *
from PIL import Image

from model import *
# import moviepy.video.io.ImageSequenceClip
import scipy
# import cv2
# import dlib
import kornia.augmentation as K
# from IPython.display import Video
# from aubio import tempo, source
from  flask_socketio import  SocketIO
from server.src.training import Train
from flask import Flask


latent_dim = 8
n_mlp = 5
num_down = 3


G_A2B = Generator(256, 4, latent_dim, n_mlp, channel_multiplier=1, lr_mlp=.01,n_res=1).cuda().eval()

ensure_checkpoint_exists('/data/lxq/GANsNRoses-main/GNR_checkpoint_full.pt')
ckpt = torch.load('/data/lxq/GANsNRoses-main/GNR_checkpoint_full.pt', map_location=lambda storage, loc: storage)

G_A2B.load_state_dict(ckpt['G_A2B_ema'])

# mean latent
truncation = 1
with torch.no_grad():
    mean_style = G_A2B.mapping(torch.randn([1000, latent_dim]).cuda()).mean(0, keepdim=True)


test_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5), inplace=True)
])


plt.rcParams['figure.dpi'] = 200

torch.manual_seed(84986)

num_styles = 5
style = torch.randn([num_styles, latent_dim]).cuda()

#读图片

real_A = Image.open('/data/lxq/GANsNRoses-main/server/src/assets/images/1.png')

real_A = test_transform(real_A).unsqueeze(0).cuda()

with torch.no_grad():
    A2B_content, _ = G_A2B.encode(real_A)
    fake_A2B = G_A2B.decode(A2B_content.repeat(num_styles,1,1,1), style)
    A2B = torch.cat([real_A, fake_A2B], 0)

#存图片
display_image(utils.make_grid(A2B.cpu(), normalize=True, range=(-1, 1), nrow=10))

#//////
# modulate = {
#     k: v
#     for k, v in ckpt["G_A2B_ema"].items()
#     if "modulation" in k and "to_rgbs" not in k and "weight" in k
# }

# weight_mat = []
# for k, v in modulate.items():
#     weight_mat.append(v)

# W = torch.cat(weight_mat, 0)
# eigvec = torch.svd(W).V.to("cpu")
# plt.rcParams['figure.dpi'] = 200

# real_A = Image.open('./samples/zzs.png')
# real_A = test_transform(real_A).unsqueeze(0).cuda()


# eig_idx = 2 # which eigenvec to choose
# eig_scale = 4 # how much to scale the eigvec

# style = G_A2B.mapping(torch.randn([1, latent_dim]).cuda())
# direction = eig_scale * eigvec[:, eig_idx].unsqueeze(0).cuda()


# with torch.no_grad():
#     A2B_content, _ = G_A2B.encode(real_A)
#     fake_A2B = G_A2B.decode(A2B_content, style, use_mapping=False)
#     fake_A2B2 = G_A2B.decode(A2B_content, style+direction, use_mapping=False)

# display_image(utils.make_grid(torch.cat([real_A, fake_A2B, fake_A2B2], 0).cpu(), normalize=True, range=(-1, 1)))