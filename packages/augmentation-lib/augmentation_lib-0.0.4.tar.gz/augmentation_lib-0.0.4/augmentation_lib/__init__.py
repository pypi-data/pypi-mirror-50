VERSION = (0, 0, 4)
__version__ = '.'.join([str(x) for x in VERSION])

from augmentation_lib.augmentation import center_crop_px
from augmentation_lib.augmentation import center_crop_percents
from augmentation_lib.augmentation import crop_px
from augmentation_lib.augmentation import crop_percents
from augmentation_lib.augmentation import random_crop_px
from augmentation_lib.augmentation import random_crop_percents
from augmentation_lib.augmentation import flip_horizontal
from augmentation_lib.augmentation import flip_vertical
from augmentation_lib.augmentation import zero_pad
from augmentation_lib.augmentation import conv_one_step
from augmentation_lib.augmentation import convolution_one_layer
from augmentation_lib.augmentation import full_convolution
from augmentation_lib.augmentation import dropout_random
from augmentation_lib.augmentation import dropout
from augmentation_lib.augmentation import shuffle
from augmentation_lib.augmentation import jitter
from augmentation_lib.augmentation import opacity
from augmentation_lib.augmentation import opacity_object
from augmentation_lib.augmentation import overlay2_images
from augmentation_lib.augmentation import resize_np
