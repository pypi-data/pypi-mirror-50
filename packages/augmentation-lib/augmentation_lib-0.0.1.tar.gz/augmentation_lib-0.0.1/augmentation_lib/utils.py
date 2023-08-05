import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def resize_image(image: str, size: tuple) -> np.ndarray:
    """
    Takes an image and resize it to your specified size in px.

    Keyword Arguments:
        image {str} -- the path to the image
        size {tuple} -- size of image you want to get after resize (w, h)

    Returns:
        numpy.ndarray -- resized image
    """
    image = Image.open(image)
    img_arr = np.asarray(image)
    #     print(f'Image before resize: {img_arr.shape}')
    new_w, new_h = size
    resized = image.resize(size, Image.ANTIALIAS)
    return np.asarray(resized)


def namestr(obj: str, namespace) -> str:
    """
    Takes an object and returns variable names.
    Eg. Can be used to get variable names from the list with np.arrays

    Keyword Arguments:
        obj {str} -- name of the variable for assigned object
        namespace {obj} -- namespace of object (eg. globals())

    Returns:
        str -- name of the variable
    """
    return [name for name in namespace if namespace[name] is obj][0]


def plot_images(pictures: list, columns: int, rows: int, fig_size: tuple) -> None:
    """
    Plots images in specified grid for provided image list

    Keyword Arguments:
        pictires {list} -- list of images as np.arrays
        columns {int} -- columns to plot
        rows {int} -- rows to plot
        fig_size -- tuple of image size

    Returns:
        None -- plots an images
    """
    fig = plt.figure(figsize=fig_size)
    for i in range(1, columns * rows + 1):
        image = pictures[i - 1]
        img_name = namestr(image, globals())
        fig.add_subplot(rows, columns, i, title=img_name)
        plt.imshow(image)
    plt.show()


