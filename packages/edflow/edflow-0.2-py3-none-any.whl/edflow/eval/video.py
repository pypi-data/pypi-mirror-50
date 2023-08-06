import cv2
import numpy as np
import os
from tqdm import trange

from abc_pose.evaluations.flow_eval import back_trans
from edflow.data.util import adjust_support


def direct_video(root, data_in, data_out, config):
    '''Expects an entry ``frame_gen`` in :attr:`data_out` examples.
    Concatenates all these images to one video.'''

    savename = os.path.join(root, 'direct_video.avi')
    fcc = cv2.VideoWriter_fourcc(*'MJPG')
    imsize = data_out[0]['frame_gen'].shape[:2]

    out = cv2.VideoWriter(savename, fcc, 25.0, tuple(imsize), True)

    white = 255 * np.ones(shape=list(imsize) + [3], dtype='uint8')

    for i in trange(len(data_out), desc='Frame'):
        image = data_out[i]['frame_gen']

        alpha = image[..., 3:] / 255.

        image = image[..., :3] * alpha + white * (1 - alpha)
        image = np.clip(image, 0, 255)
        image = image.astype(np.uint8)

        out.write(image[..., [2, 1, 0]])

    out.release()


def kp_video(root, data_in, data_out, config):
    from abc_pose.abcnet.heatmaps import kp2heat

    savename = os.path.join(root, 'kp_video.avi')
    fcc = cv2.VideoWriter_fourcc(*'MJPG')
    imsize = data_out[0]['frame_gen'].shape[:2]

    out = cv2.VideoWriter(savename, fcc, 25.0, tuple(imsize), False)

    for i in trange(len(data_out), desc='Frame'):
        kps = data_in[i]['pose_keypoints'] * 256
        print(kps)
        heatmap = kp2heat(kps)
        print(heatmap.shape)
        heatmap_gray = np.mean(heatmap, -1)
        print(heatmap_gray.shape)
        heatmap_gray = heatmap_gray / heatmap_gray.max()
        print(heatmap_gray.shape, heatmap_gray.min(), heatmap_gray.max())

        heatmap_gray = adjust_support(heatmap_gray, '0->255', '0->1', True)

        out.write(heatmap_gray)

    out.release()


def backtrans_video(root, data_in, data_out, config, add_debug_output=False):
    '''Expects the entries ``orig_frame, box, target`` in :attr:`data_in` and
    ``frame_gen`` in :attr:`data_out`.

    Properties of the entries:
        ``orig_frame``: Frame to be painted onto.
        ``box``: Bounding box of the generated image in the original frame.
        ``mask``: grayscale mask of the person/object in the image to be
            overpainted.
        ``frame_gen``: RBGA image to be overpainted on the original frame.
    '''
    savename = os.path.join(root, '{}.avi')
    fcc = cv2.VideoWriter_fourcc(*'MJPG')
    imsize = list(data_in[0]['orig_frame'].shape[:2])

    # for back_trans
    orig_shape = imsize + [4]
    mask_shape = imsize + [1]

    overpaint_vid = cv2.VideoWriter(savename.format('overpaint'),
                                    fcc,
                                    25.0,
                                    tuple(imsize[::-1]),
                                    True)

    if add_debug_output:
        mask_orig_vid = cv2.VideoWriter(savename.format('mask_orig'),
                                        fcc,
                                        25.0,
                                        tuple(imsize[::-1]),
                                        False)

        mask_person_vid = cv2.VideoWriter(savename.format('mask_person'),
                                          fcc,
                                          25.0,
                                          tuple(imsize[::-1]),
                                          False)

        person_vid = cv2.VideoWriter(savename.format('person'),
                                     fcc,
                                     25.0,
                                     tuple(imsize[::-1]),
                                     True)

        background_vid = cv2.VideoWriter(savename.format('background'),
                                         fcc,
                                         25.0,
                                         tuple(imsize[::-1]),
                                         True)

    for i in trange(len(data_out), desc='Frame'):
        in_example = data_in[i]
        background = in_example['orig_frame']
        background = adjust_support(background, '0->255', clip=True)
        box = in_example['box']

        image = data_out[i]['frame_gen']
        image = adjust_support(image, '0->255')

        image_mask = image[..., 3:]

        if 'mask' in in_example:
            inpaint_mask = in_example['mask']
        else:
            inpaint_mask = image_mask

        transformed_gen = back_trans([image],
                                     [box],
                                     orig_shape)[0]

        transformed_mask = back_trans([inpaint_mask],
                                      [box],
                                      mask_shape)[0]
        transformed_mask_gen = back_trans([image_mask],
                                          [box],
                                          mask_shape)[0]

        transformed_mask = adjust_support(transformed_mask,
                                          '0->255',
                                          clip=True)
        transformed_mask_gen = adjust_support(transformed_mask_gen,
                                              '0->255',
                                              clip=True)

        kernel = np.ones([13, 13])
        dilated_mask = cv2.dilate(transformed_mask[..., 0],
                                  kernel,
                                  iterations=1)

        inpainted_original = cv2.inpaint(background,
                                         dilated_mask,
                                         3,
                                         cv2.INPAINT_TELEA)

        transformed_gen = adjust_support(transformed_gen, '0->255', clip=True)
        transformed_gen = transformed_gen[..., :3]

        M = adjust_support(transformed_mask_gen, '0->1')
        M[M > 0.95] = 1
        final_frame = M * transformed_gen + (1 - M) * inpainted_original
        final_frame = adjust_support(final_frame, '0->255', clip=True)

        # Need to save color image as BGR -> [2, 1, 0]
        overpaint_vid.write(final_frame[..., [2, 1, 0]])

        if add_debug_output:
            mask_orig_vid.write(transformed_mask)
            mask_person_vid.write(adjust_support(M,
                                                 '0->255',
                                                 '0->1',
                                                 clip=True))
            person_vid.write(transformed_gen[..., [2, 1, 0]])
            background_vid.write(inpainted_original[..., [2, 1, 0]])

    overpaint_vid.release()
    if add_debug_output:
        mask_orig_vid.release()
        mask_person_vid.release()
        person_vid.release()
        background_vid.release()


if __name__ == '__main__':
    import argparse
    from abc_pose.evaluations.eval_pipeline import EvalDataFolder
    from edflow.util import pprint

    A = argparse.ArgumentParser()

    A.add_argument('-r', '--root', type=str, help='data root')

    a = A.parse_args()

    r = a.root

    d_out = EvalDataFolder(r, show_bar=False)
    pprint(d_out[0])

    print('Found {} frames'.format(len(d_out)))

    direct_video(r, None, d_out)
