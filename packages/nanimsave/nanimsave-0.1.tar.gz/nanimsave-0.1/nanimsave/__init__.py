import matplotlib.pyplot as plt
import os.path
import numpy as np
import scipy.misc

name = 'nanimsave'


def imsave(path, im_np, im_type=None, im_range=None, palette=plt.cm.gray, null_color=(255, 0, 0)):
    if (im_type is None):
        im_type = 'image'
        filename, ext = os.path.splitext(path)
        
        if (ext == '.npz'):
            im_type = 'npz'

        if (ext == '.npy'):
            im_type = 'npy'

    if (im_type == 'image'):

        if (np.isnan(im_np).max() == False and im_range is None):
            scipy.misc.imsave(path, im_np)
        else:
            if (im_range is None):
                im_np_min = np.nanmin(im_np)
                im_np_max = np.nanmax(im_np)
            else:
                im_np_min = im_range[0]
                im_np_max = im_range[1]

            im_np_nan = np.isnan(im_np)

            im_normalized_np = (im_np - im_np_min) * 1.0 / (im_np_max - im_np_min)
            im_normalized_np[im_np_nan] = 0
            im_normalized_np[im_normalized_np < 0] = 0
            im_normalized_np[im_normalized_np > 1.0] = 1.0

            im_color_np = np.zeros((im_np.shape[0], im_np.shape[1], 3), dtype='uint8')
            colors = palette(im_normalized_np)

            im_color_np[:, :, 0] = colors[:, :, 0] * 255.0
            im_color_np[:, :, 1] = colors[:, :, 1] * 255.0
            im_color_np[:, :, 2] = colors[:, :, 2] * 255.0

            im_color_np[im_np_nan, 0] = null_color[0]
            im_color_np[im_np_nan, 1] = null_color[1]
            im_color_np[im_np_nan, 2] = null_color[2]

            scipy.misc.imsave(path, im_color_np)
    elif (im_type == 'npz'):
        np.savez_compressed(path, data=im_np)
    elif (im_type == 'npy'):
        np.save(path, im_np)