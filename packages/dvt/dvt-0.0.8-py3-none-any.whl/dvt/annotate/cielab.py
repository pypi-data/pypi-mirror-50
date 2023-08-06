# -*- coding: utf-8 -*-
"""Annotators to extract CIELAB color histograms.
"""

import numpy as np
import cv2
from scipy.cluster.vq import kmeans

from .core import FrameAnnotator
from ..utils import _proc_frame_list, _which_frames


class CIElabAnnotator(FrameAnnotator):
    """Annotator for constructing a color histogram and extracting the dominant
    colours for an image in CIELAB colorspace.

    The annotator will return a histogram describing the color distribution
    of an image, and a list of the most dominant colors.

    Attributes:
        freq (int): How often to perform the embedding. For example, setting
            the frequency to 2 will computer every other frame in the batch.
        num_buckets (tuple): A tuple of three numbers giving the maximum number
            of buckets in each color channel, Lightness, A, B. These
            should each be divisible by 256. Default is (16, 16, 16).
        num_dominant (int): Number of dominant colors to extract. Default is 5.
        frames (array of ints): An optional list of frames to process. This
            should be a list of integers or a 1D numpy array of integers. If
            set to something other than None, the freq input is ignored.
    """

    name = "cielab"

    def __init__(
        self, freq=1, num_buckets=(16, 16, 16), num_dominant=5, frames=None
    ):

        self.freq = freq
        self.num_buckets = num_buckets
        self.num_dominant = num_dominant
        self.frames = _proc_frame_list(frames)
        super().__init__()

    def annotate(self, batch):
        """Annotate the batch of frames with the cielab annotator.

        Args:
            batch (FrameBatch): A batch of images to annotate.

        Returns:
            A list of dictionaries containing the video name, frame, the
            CIELAB histogram of length (num_buckets[0] * num_buckets[1] *
            num_buckets[2]), and an array of dominant colors of shape
            (num_dominant, 3).
        """
        # determine which frames to work on
        frames = _which_frames(batch, self.freq, self.frames)
        if not frames:
            return

        # run the color analysis on each frame
        hgrams = []
        dominant = []
        for fnum in frames:
            img_lab = cv2.cvtColor(batch.img[fnum, :, :, :], cv2.COLOR_RGB2LAB)

            hgrams += [_get_cielab_histogram(img_lab, self.num_buckets)]
            if self.num_dominant > 0:
                dominant += [_get_cielab_dominant(img_lab, self.num_dominant)]

        obj = {"cielab": np.vstack(hgrams)}

        if self.num_dominant > 0:
            obj_rgb = cv2.cvtColor(np.stack(dominant), cv2.COLOR_LAB2RGB)

            shp = (obj_rgb.shape[0], self.num_dominant)
            out = np.full(shp, "#000000", dtype=np.dtype("<U7"))
            for i, obj_frame in enumerate(obj_rgb):
                for j, oc in enumerate(obj_frame):
                    out[i, j] = "#{0:02x}{1:02x}{2:02x}".format(
                        oc[0], oc[1], oc[2]
                    )

            obj["dominant_colors"] = out

        # Add video and frame metadata
        obj["video"] = [batch.vname] * len(frames)
        obj["frame"] = np.array(batch.get_frame_names())[list(frames)]

        return [obj]


def _get_cielab_histogram(img, num_buckets):

    return cv2.calcHist(
        [img], [0, 1, 2], None, num_buckets, [0, 256, 0, 256, 0, 256]
    ).reshape(-1)


def _get_cielab_dominant(img, num_dominant):
    img_flat = img.reshape(-1, 3).astype(np.float32)

    # increasing iter would give 'better' clustering, at the cost of speed
    dominant_colors, _ = kmeans(img_flat, num_dominant, iter=5)

    return dominant_colors.astype(np.uint8)
