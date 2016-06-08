from PIL import Image
import os
import os.path
import numpy

class Filmstrip:
    def __init__(self, image_shape=None, grid_shape=None,
                    margin=1, background='white'):
        self.image_shape = image_shape
        self.grid_shape = grid_shape
        self.margin = margin
        self.background = background
        self.im = Image.new('RGB',
            ((self.image_shape[1] + margin) * self.grid_shape[1] - margin,
             (self.image_shape[0] + margin) * self.grid_shape[0] - margin),
            self.background)

    def set_image(self, grid_location, image_data, mask_data=None,
                    negative=None, zeromean=False):
        if negative is None:
            negative = image_data.shape[0] == 1
        if zeromean:
            image_data = image_data + 128
        if negative:
            image_data = 255 - image_data
        if mask_data is not None:
            image_data = ((image_data.astype(numpy.float) - 128)
                            * mask_data + 128)
        if image_data.shape[0] == 1:
            data = image_data.astype(numpy.uint8).tostring()
            one_image = Image.frombytes('L', self.image_shape, data)
        else:
            data = (image_data.transpose((1, 2, 0))
                            ).astype(numpy.uint8).tostring()
            one_image = Image.frombytes('RGB', self.image_shape, data)
        self.im.paste(one_image, tuple((g * (s + self.margin))
                for g, s in zip(grid_location, self.image_shape)))

    def save(self, filename):
        dirname = os.path.dirname(filename)
        if dirname:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        #if self.im.size[0] * self.im.size[1] < 640 ** 2:
        opts = { 'subsampling': 0, 'quality': 99 }
        self.im.save(filename, 'JPEG', **opts)