# Image augmentation library

This image augmentation library can be used to crop, flip, blur, sharpen, mix channels, overlay images.
The main idea is to use only numpy library to perform these tasks.
Augmented images can be used for Machine Learning projects

# Getting it

To download augmentation_lib, either fork this github repo or simply use Pypi via pip.
```
$ pip install augmentation-lib
```
# Features

This library performs different types of augmentation.

## Crops:

`center_crop_px` takes an image, width and height in pixels and returns center cropped image.

`center_crop_percents` takes an image and size in percents (0 - 1) and returns center cropped image.

`crop_px` takes an image starting point for cropping, width and height in pixels and returns cropped image.

`crop_percents` takes an image starting point (height_coordinate, width_coordinate) in px, and size (height, width) in percents for cropping.

`random_crop_px` takes a cropping size in pixels and randomly crops an image.

`random_crop_percents` takes a cropping size in percents (0 - 1) and randomly crops an image.

## Flips:

`flip_horizontal` takes an image and flips it horizontally.

`flip_vertical` takes an image and flips it vertically.

## Padding:

`zero_pad` takes an image and pads it with zeros by specified number of pixels.

## Convolution:

`conv_one_step` performs convolution for specified slice.

`convolution_one_layer` performs one image layer convolution.

`full_convolution` performs image convolution by specified kernel.

## Dropouts:

`dropout_random` performs random dropout of image pixels.

`dropout` performs dropout of image pixels by specified intensity in percents (0 - 1).

## Other augmentation:

`shuffle` performs shuffle of image layers by specified order.

`jitter` performs color jitter of one specified or random image layer. One of the color channels of the image is modified adding or subtracting a random and bounded value.

`opacity` makes an image transparent.

`opacity_object` makes an image background transparent, works better with object images.

`overlay2_images` overlay 2 images with applied transparency.

`resize_np` resize image using numpy and Nearest Neighbor Interpolation.

# Showcase

More info about using this library you can find in:
https://github.com/laume/augmentation_lib/blob/master/augmentation_lib/showcase.ipynb