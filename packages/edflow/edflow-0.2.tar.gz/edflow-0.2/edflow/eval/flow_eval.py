import numpy as np
import os
from scipy.misc import imresize
from tqdm import trange
import torch
from torch.autograd import Variable

from abc_pose.util.flow_tool import Flow, crop
from edflow.metrics.image_metrics import ssim_metric, l2_metric
from edflow.custom_logging import get_logger


class FlowEval(object):

    def __init__(self, orig_size, inverse=True, metric='ssim'):
        '''Args:
            orig_size (list(int)): Shape of the image from which the frame
                crops are taken. Needed to back transform the generated frames
                before calculating the flow.
            inverse (bool): If True (default) the flow is calculated from the
                current frame to thre previous, as is usually done in the flow
                of our datasets.
        '''
        assert metric in ['ssim', 'l2'], 'metric must be ssim or l2'
        self.logger = get_logger(self)

        self.osize = orig_size
        self.inverse = inverse
        self.mname = metric
        self.metric = l2_metric if metric == 'l2' else ssim_metric

        self.save_template = '{}_{:0>6}.{}'

        self.flow = Flow()

    def calculate_flow(self, root, data_in, data_out, force=False):
        '''Calculates the flow between all generated images and compares with
        the ground_truth flow.'''

        assert len(data_in) == len(data_out)

        for i in trange(len(data_in), desc='Calc Flow'):
            if 'frame_prev' in data_out[i]:
                datum_curr = data_out[i]
                datum_prev = data_out[data_out[i]['frame_prev']]

                frame_curr = datum_curr['frame_gen']
                frame_prev = datum_prev['frame_gen']

                box_curr = datum_curr['box']
                box_prev = datum_prev['box']

                idx_curr = datum_curr['save_index_']
                root_curr = datum_curr['datum_root']

                savename = self.save_template.format('flow', idx_curr, 'npy')
                savename = os.path.join(root_curr, savename)

                if os.path.exists(savename) and not force:
                    continue

                full_frame_curr = back_trans(frame_curr, box_curr, self.osize)
                full_frame_prev = back_trans(frame_prev, box_prev, self.osize)

                if self.inverse:
                    flow = self.flow(full_frame_curr, full_frame_prev)
                else:
                    flow = self.flow(full_frame_prev, full_frame_curr)

                flow_crop = crop(flow, box_curr)

                np.save(savename, flow_crop)

    def compare_flow(self, root, data_in, data_out, force=False):
        measurements = []
        for i in trange(len(data_in), desc='Comp Flow'):
            if 'frame_prev' in data_out[i]:
                root_curr = data_in.labels['datum_root'][i]
                idx_curr = data_in.labels['save_index_'][i]

                loadname = self.save_template.format('flow', idx_curr, 'npy')
                loadname = os.path.join(root_curr, loadname)

                flow_gen = np.load(loadname)
                flow_grt = data_in[i]['flow']

                measurements += [self.metric(flow_gen, flow_grt)]

        savename = os.path.join(root, '{}_flow_metric.npy'.format(self.mname))
        np.save(savename, measurements)


def ssim(image1, image2):
    '''Wrapper to use metric for non batched images.'''
    im1 = np.expand_dims(image1, 0)
    im2 = np.expand_dims(image2, 0)

    s = ssim_metric(im1, im2)
    s = s[0]

    return s


def l2(image1, image2):
    '''Wrapper to use metric for non batched images.'''
    im1 = np.expand_dims(image1, 0)
    im2 = np.expand_dims(image2, 0)

    l2 = l2_metric(im1, im2)
    l2 = l2[0]

    return l2


def to_torch(image, no_transpose=False):
    if not no_transpose:
        image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, 0)
    image = np.array(image, dtype=np.float32)
    image = Variable(torch.from_numpy(image)).cuda()

    return image


def from_torch(image, no_transpose=False):
    image = image.data.cpu().numpy()
    image = np.squeeze(image, 0)
    if not no_transpose:
        image = np.transpose(image, [1, 2, 0])

    return image


def apply_mask(image):
    return (image * image[..., 3:])[..., :3]


def back_trans(crops, boxes, orig_shape):
    '''Transforms a crop into its original position in an empty image.'''
    # Shape of the final frame
    xdim, ydim, nc = orig_shape

    finals = []
    for i, [one_crop, box] in enumerate(zip(crops, boxes)):
        # Final frame, where we put the data into
        big_picture = np.zeros(orig_shape, dtype=np.float32)

        xmin, ymin, xw, yw = box
        xmax = xmin + xw
        ymax = ymin + yw
        xdim_c, ydim_c, nc_c = one_crop.shape

        # xmin *= xdim
        # xmax *= xdim
        # ymin *= ydim
        # ymax *= ydim

        xmin = int(xmin)
        xmax = int(xmax)
        ymin = int(ymin)
        ymax = int(ymax)

        startx = -xmin if xmin < 0 else None
        stopx = -(xmax - xdim) if xmax > xdim else None
        starty = -ymin if ymin < 0 else None
        stopy = -(ymax - ydim) if ymax > ydim else None

        sizex = int(xmax - xmin)
        sizey = int(ymax - ymin)

        one_crop = one_crop if nc_c in [3, 4] else one_crop[..., 0]
        one_crop_resize = imresize(one_crop, [sizex, sizey])
        one_crop_resize = np.array(one_crop_resize, dtype=float)
        if nc_c == 1:
            one_crop_resize = np.expand_dims(one_crop_resize, -1)

        one_crop_resize /= 255.

        # Clip to avoid negative indices or too large ones
        xmin = np.clip(xmin, 0, xdim)
        ymin = np.clip(ymin, 0, ydim)
        xmax = np.clip(xmax, 0, xdim)
        ymax = np.clip(ymax, 0, ydim)

        try:
            one_crop_final = one_crop_resize[startx:stopx, starty:stopy]
            if nc_c == 3 and nc == 4:
                alpha = np.ones(list(one_crop_final.shape[:2]) + [1])
                one_crop_final = np.concatenate([one_crop_final, alpha], -1)
            big_picture[xmin:xmax, ymin:ymax] = one_crop_final
            finals += [big_picture]
        except Exception as e:
            print(xmin, xmax, ymin, ymax)
            print(box)
            print(startx, stopx, starty, stopy)
            print(one_crop_final.shape)
            print(sizex, sizey)
            raise e

    return finals
