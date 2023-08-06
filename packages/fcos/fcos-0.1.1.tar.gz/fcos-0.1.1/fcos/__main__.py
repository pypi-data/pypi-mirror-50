from fcos import FCOS
import cv2
import skimage.io as io
import argparse

parser = argparse.ArgumentParser(description="FCOS Object Detector")
parser.add_argument(
    "input_image",
    help="path or url to an input image",
)
args = parser.parse_args()

fcos = FCOS(
    model_name="fcos_R_50_FPN_1x",
    nms_thresh=0.6,
    cpu_only=False  # if you do not have GPUs, please set cpu_only as False
)

im = io.imread(args.input_image)
assert im.shape[-1] == 3, "only 3-channel images are supported"

# convert from RGB to BGR because fcos assumes the BRG input image
im = im[..., ::-1].copy()

# resize image to have its shorter size == 800
f = 800.0 / float(min(im.shape[:2]))
im = cv2.resize(im, (0, 0), fx=f, fy=f)

bbox_results = fcos.detect(im)

fcos.show_bboxes(im, bbox_results)
