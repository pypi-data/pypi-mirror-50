import numpy as np
from PIL import Image
import doctest
import numbers
from typing import Optional, Union
import random
from .utils import resize_image
from .constants import kernel_blur, kernel_sharp


def center_crop_px(image: Union[str, np.ndarray], size: tuple) -> np.ndarray:
    """
    Takes an image, width and height in pixels and returns
    center cropped image.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        size {tuple} -- the height and width of image you want to get in pixels,
        if provided only one value - you will get square crop

    Returns:
        numpy.ndarray -- the center cropped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    h, w, _ = img_arr.shape
    if isinstance(size, numbers.Number):
        height = width = size
    elif len(size) == 2:
        height, width = size
    else:
        print('Enter correct size: must be tuple (h, w) for standard crop, or (size) for square crop.')
        return img_arr
    if width <= w and height <= h:
        start_w = w // 2 - (width // 2)
        start_h = h // 2 - (height // 2)
        return img_arr[start_h:start_h + height, start_w:start_w + width]
    else:
        return img_arr


def center_crop_percents(image: Union[str, np.ndarray], size: tuple) -> np.ndarray:
    """
    Takes an image and size in percents (0 - 1) and returns
    center cropped image.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        size {tuple} -- the height and width of image you want to get in percents (0 -1),
        if provided only one value - both height and width percentage values will be the same

    Returns:
        numpy.ndarray -- the center cropped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    h, w, _ = img_arr.shape
    if isinstance(size, numbers.Number):
        percents_height = percents_width = size
    elif len(size) == 2:
        percents_height, percents_width = size
    else:
        print('Enter correct size: must be tuple (h, w) or (size) for square crop.')
        return img_arr
    if 0 <= percents_height <= 1 and 0 <= percents_width <= 1:
        center_h = h // 2
        center_w = w // 2
        half_h = int(h * percents_height // 2)
        half_w = int(w * percents_width // 2)
        return img_arr[center_h - half_h:center_h + half_h,
                       center_w - half_w:center_w + half_w]
    else:
        return img_arr


def crop_px(image: Union[str, np.ndarray], start_h: int, start_w: int, size: tuple) -> np.ndarray:
    """
    Takes an image starting point for cropping, width and height in pixels and returns
    cropped image.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        start_h {int} -- start h coordinate for cropping
        start_w {int} -- start w coordinate for cropping
        size {tuple} -- the height and width of image you want to get in pixels,
        if provided only one value - you will get square crop

    Returns:
        numpy.ndarray -- the cropped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    h, w, _ = img_arr.shape
    # TODO good to have: if isinstance(size, numbers.Number)
    start_w = abs(start_w)
    start_h = abs(start_h)
    if isinstance(size, numbers.Number):
        height = width = size
    elif len(size) == 2:
        height, width = size
    else:
        print('Enter correct size: must be tuple (h, w) or (size) for square crop.')
        return img_arr
    if width <= w and height <= h and start_w <= w and start_h <= h:
        return img_arr[start_h:start_h + height, start_w:start_w + width]
    else:
        return img_arr


def crop_percents(image: Union[str, np.ndarray], start_point: tuple, size: tuple) -> np.ndarray:
    """
    Takes an image starting point (height_coordinate, width_coordinate) in px,
    and size (height, width) in percents for cropping

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        start_point {tuple} -- start h and w coordinates for cropping
        size {tupe} -- the height and width of image in percents (0 - 1) you want to get

    Returns:
        numpy.ndarray -- the cropped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    h, w, _ = img_arr.shape
    if isinstance(start_point, numbers.Number):
        start_h = start_w = start_point
    elif len(start_point) == 2:
        start_h, start_w = start_point
    else:
        print('Enter correct start point: must be tuple (h, w) in px or (int) for the same number.')
        return img_arr
    start_h = abs(start_h)
    start_w = abs(start_w)

    if isinstance(size, numbers.Number):
        percents_height = percents_width = size
    elif len(size) == 2:
        percents_height, percents_width = size
    else:
        print('Enter correct size: must be tuple (h, w) or (size) for square crop.')
        return img_arr
    if 0 <= percents_height <= 1 and 0 <= percents_width <= 1:
        height = int(h * percents_height)
        width = int(w * percents_width)
        return img_arr[start_h:start_h + height,
               start_w:start_w + width]
    else:
        return img_arr


def random_crop_px(image: Union[str, np.ndarray], size: tuple) -> np.ndarray:
    """
    Takes a cropping size and randomly crops an image.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        size {tuple} -- the height and width of image you want to get in pixels,
        if provided only one value - you will get square crop

    Returns:
        numpy.ndarray -- the cropped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    h, w, _ = img_arr.shape
    if isinstance(size, numbers.Number):
        height = width = size
    elif len(size) == 2:
        height, width = size
    else:
        print('Enter correct size: must be tuple (h, w) or (size) for square crop.')
        return img_arr
    if width <= w and height <= h:
        start_h = np.random.randint(0, h - height)
        start_w = np.random.randint(0, w - width)
        return img_arr[start_h:start_h + height, start_w:start_w + width]
    else:
        return img_arr


def random_crop_percents(image: Union[str, np.ndarray], size: tuple) -> np.ndarray:
    """
    Takes a cropping size in percents (0 - 1) and randomly crops an image.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        size {tuple} -- the height and width of image you want to get in percents,
        if provided only one value - you will get square crop

    Returns:
        numpy.ndarray -- the random cropped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    h, w, _ = img_arr.shape
    if isinstance(size, numbers.Number):
        percents_height = percents_width = size
    elif len(size) == 2:
        percents_height, percents_width = size
    else:
        print('Enter correct size: must be tuple (h, w) or (size) for square crop.')
        return img_arr
    if 0 <= percents_height <= 1 and 0 <= percents_width <= 1:
        height = int(h * percents_height)
        width = int(w * percents_width)
        start_h = np.random.randint(0, h - height)
        start_w = np.random.randint(0, w - width)
        return img_arr[start_h:start_h + height, start_w:start_w + width]
    else:
        return img_arr


def flip_horizontal(image: Union[str, np.ndarray]) -> np.ndarray:
    """
    Takes an image and flips it horizontally.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array

    Returns:
        numpy.ndarray -- horizontally flipped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    return np.flip(img_arr, axis=0)


def flip_vertical(image: Union[str, np.ndarray]) -> np.ndarray:
    """
    Takes an image and flips it vertically.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array

    Returns:
        numpy.ndarray -- the vertically flipped image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        img_arr = np.asarray(img)
    else:
        img_arr = image
    return np.flip(img_arr, axis=1)


def zero_pad(image: Union[str, np.ndarray], pad: int) -> np.ndarray:
    """
    Takes an image and pads it with zeros by specified number of pixels.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        pad {int} -- number of pixels you want to pad an image

    Returns:
        numpy.ndarray -- padded image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), 'constant', constant_values=(0, 0))
    return padded


def conv_one_step(slc: np.array, kernel: np.array) -> np.array:
    """
    Performs convolution for specified slice

    Keyword Arguments:
        slc {np.array} -- the slice of an array you want to apply the filter
        kernel {np.array} -- kernel (filter) you use for convolution

    Returns:
        numpy.ndarray -- convoluted array
    """
    s = np.multiply(slc, kernel)
    #     res = np.median(s)
    res = np.sum(s)
    return res


def convolution_one_layer(image: Union[str, np.ndarray], layer: int, kernel: np.array) -> np.ndarray:
    """
    Performs one layer convolution

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        layer {int} -- layer number you want to convolute
        kernel {np.array} -- kernel (filter) you use for convolution

    Returns:
        numpy.ndarray -- convoluted layer
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    # padded = zero_pad(image, 1)
    #     plt.imshow(padded[:,:,layer])
    #     plt.show()

    #     for_blur = padded[:,:,layer]
    for_blur = image[:, :, layer]
    height, width = for_blur.shape
    changed = np.zeros((image[:, :, layer].shape))
    h_f, w_f = kernel.shape

    for h in np.arange(height - 2):
        for w in np.arange(width - 2):
            slc = for_blur[h:h + h_f, w:w + w_f]
            changed[h, w] = conv_one_step(slc, kernel)

    return changed


def full_convolution(image: Union[str, np.ndarray], kernel: np.array) -> np.ndarray:
    """
    Performs image convolution by specified kernel

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        kernel {np.array} -- kernel (filter) you use for convolution

    Returns:
        numpy.ndarray -- convoluted image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)

    height, width, channels = image.shape
    image = image / np.max(image)
    changed = np.zeros((image.shape))

    for c in np.arange(channels):
        changed[:, :, c] = convolution_one_layer(image, c, kernel)

    if changed.max() > 0 or changed.min() < 0:
        changed = np.clip(changed, 0, 1)
    return changed


def dropout_random(image: Union[str, np.ndarray]) -> np.ndarray:
    """
    Performs random dropout of image pixels

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array

    Returns:
        numpy.ndarray -- image with randomly dropped pixels
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    img = image.copy()
    size = img[:, :, 0].shape
    mask = np.random.randint(0, 2, size=size).astype(np.bool)
    replace = np.zeros(size)
    for i in range(3):
        layer = img[:, :, i]
        layer[mask] = replace[mask]
    return img


def dropout(image: Union[str, np.ndarray], intensity: float) -> np.ndarray:
    """
    Performs dropout of image pixels by specified intensity in percents (0 - 1)

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.arra
        intensity {float} -- dropout intensity in percents (0 - 1)

    Returns:
        numpy.ndarray -- image with dropped pixels
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    img = image.copy()
    size = img[:, :, 0].shape
    mask = np.random.choice(a=[True, False], size=size, p=[intensity, 1 - intensity])
    replace = np.zeros(size)
    for i in range(3):
        layer = img[:, :, i]
        layer[mask] = replace[mask]
    return img


def shuffle(image: Union[str, np.ndarray], channels: Optional[str] = None) -> np.ndarray:
    """
    Performs shuffle of image layers by specified order

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        channels {str} -- change channels order, if not provided returns random channels order

    Returns:
        numpy.ndarray -- image with changed channels order
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    image = image / 255
    shuffled = np.zeros(image.shape)
    order = {'R': 0, 'G': 1, 'B': 2}
    if channels:
        if channels != 'RGB' and set(channels.upper()) == set('RGB'):
            channels = channels.upper()
        else:
            print('Nothing changed!')
            return image
    else:
        channels = ''.join(random.sample('RGB', 3))
        print(f'Random channels: {channels}')

    for i, v in enumerate(channels):
        shuffled[:, :, i] = image[:, :, order[v.upper()]]

    # if shuffled.max() > 0 or shuffled.min() < 0:
    #     shuffled = np.clip(shuffled, 0, 1)
    return shuffled


def jitter(image: Union[str, np.ndarray], probability: float,
           channel: Optional[str] = None) -> np.ndarray:
    """
    Performs color jitter of one specified or random image layer.
    One of the color channels of the image is modified adding or subtracting a random and bounded value.

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        probability {float} -- probability from 0 to 1 for applying jitter
        channel {str} -- channel to which to apply jitter (optional)

    Returns:
        numpy.ndarray -- image with color jitter applied on random or specified channel
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    image = image / 255
    shuffled = image.copy()
    order = {'R': 0, 'G': 1, 'B': 2}
    if channel:
        if len(channel) == 1 and channel in ['R', 'G', 'B']:
            channel = channel.upper()
        else:
            print('Nothing changed!')
            return image
    else:
        channel = random.sample('RGB', 1)[0]
        print(f'Random channel: {channel}')

    size = image[:,:,0].shape

    mask = np.random.choice(a=[False, True], size=size,
                            p=[1-probability, probability])

    change = image[:,:,order[channel]]
    jitters = np.random.random(size)
    jitters = change + jitters
    change[mask] = jitters[mask]

    shuffled[:,:,order[channel]] = change

    if shuffled.max() > 0 or shuffled.min() < 0:
        shuffled = np.clip(shuffled, 0, 1)
    return shuffled


def opacity(image: Union[str, np.ndarray], transparency: float):
    """
    Makes an image transparent

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        transparency {float} -- value from 0 to 1 for image tranparency,
        where 0 is fully transparent, and 1 is no transparent

    Returns:
        numpy.ndarray -- transparent image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    if not 0 <= transparency <= 1:
        print('Nothing changed, enter transparency from 0 to 1.')
        return image

    h, w, _ = image.shape
    image = image / np.max(image)
    alpha = np.full(shape=(h, w), fill_value=transparency)
    transparent = np.zeros((h, w, 4))
    for i in range(3):
        transparent[:, :, i] = image[:, :, i]
    transparent[:, :, 3] = alpha
    return transparent


def opacity_object(image: Union[str, np.ndarray], object_intensity: tuple):
    """
    Makes an image transparent

    Keyword Arguments:
        image {Union[str, np.ndarray]} -- the path to the image or np.array
        transparency {float} -- value from 0 to 1 for image tranparency,
        where 0 is fully transparent, and 1 is no transparent

    Returns:
        numpy.ndarray -- transparent image
    """
    if type(image) is not np.ndarray:
        img = Image.open(image)
        image = np.asarray(img)
    # if not 0 <= object_intensity <= 1:
    #         print('Nothing changed, enter transparency from 0 to 1.')
    #         return image
    # TODO change w and h order
    h, w, _ = image.shape
    image = image / np.max(image)
    kernel = image[:, :, 0].copy()
    # print('kernel shape', kernel.shape)
    lower, higher = object_intensity
    kernel[kernel < lower] = 0
    kernel[kernel > higher] = 1
    #     alpha = np.full(shape=(h, w), fill_value=transparency)
    transparent = np.zeros((h, w, 4))
    for i in range(3):
        transparent[:, :, i] = image[:, :, i]
    transparent[:, :, 3] = kernel  # alpha
    return transparent


def overlay2_images(image1: Union[str, np.ndarray],
                    image2: Union[str, np.ndarray],
                    transparency: Optional[float] = None) -> np.ndarray:
    """
    Overlay 2 images with applied transparency

    Keyword Arguments:
        image1 {Union[str, np.ndarray]} -- the path to the image or np.array,
        image2 {Union[str, np.ndarray]} -- the path to the image or np.array,
        transparency {Optional[float] = None} -- value from 0 to 1 for image tranparency,
        where 0 is fully transparent, and 1 is not transparent

    Returns:
        numpy.ndarray -- overlayed two images with predefined transparency (optional)
    """
    if type(image1) is not np.ndarray:
        image1 = Image.open(image1)
        image1 = np.asarray(image1)
    if type(image2) is not np.ndarray:
        image2 = Image.open(image2)
        image2 = np.asarray(image2)

    h, w, _ = image1.shape

    if transparency:
        if not 0 <= transparency <= 1:
            print('Nothing changed, enter transparency from 0 to 1.')
            return image1
        image1 = opacity(image1, transparency)
        image2 = opacity(image2, transparency)

    result = np.maximum(image1, image2)
    # result = (image1 + image2) / 2
    return result


def resize_np(image: str, new_size: tuple) -> np.ndarray:
    """
        Resize image using numpy and Nearest Neighbor Interpolation

        Keyword Arguments:
            image {str} -- the path to the image,
            new_size {tuple} -- size you want to get (h, w)

        Returns:
            numpy.ndarray -- resized according specified new_size
        """
    img = Image.open(image)
    image = np.asarray(img)
    x, y, _ = image.shape
    x1, y1 = new_size
    resized = np.zeros((x1, y1, 3), dtype=np.uint8)
    cx = x1 / x
    cy = y1 / y

    for i in range(x1):
        for j in range(y1):
            v = int(np.round(i / cx))
            w = int(np.round(j / cy))
            resized[i][j] = image[v][w]
    return resized


if __name__ == '__main__':
    img = 'pics/bird.jpg'
    flip_vertical(img)
