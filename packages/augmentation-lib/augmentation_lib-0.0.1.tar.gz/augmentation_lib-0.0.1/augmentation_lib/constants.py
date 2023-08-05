import numpy as np


kernel_blur = np.array([[1.0,2.0,1.0], [2.0,4.0,2.0], [1.0,2.0,1.0]])
kernel_blur = kernel_blur / np.sum(kernel_blur)

kernel_sharp = np.array([[0., -1., 0.], [-1., 5., -1.], [0., -1., 0.]])

gaussian_kernel = np.array([[[1.0,2.0,1.0], [2.0,4.0,2.0], [1.0,2.0,1.0]],
                            [[1.0,2.0,1.0], [2.0,4.0,2.0], [1.0,2.0,1.0]],
                            [[1.0,2.0,1.0], [2.0,4.0,2.0], [1.0,2.0,1.0]]])

