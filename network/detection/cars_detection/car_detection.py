import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import cv2
from matplotlib.patches import Polygon
from skimage.measure import find_contours
import random
import colorsys
from matplotlib import patches,  lines

ROOT_DIR = os.path.abspath("../../")
sys.path.append(ROOT_DIR)

from mrcnn import utils
from mrcnn import visualize
# from mrcnn.visualize import display_instances
import mrcnn.model as modellib
from mrcnn.model import log

from network.detection.cars_detection import car_model

MODEL_DIR = os.path.join(ROOT_DIR, "logs")
config = car_model.carConfig()

class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()
DEVICE = "/gpu:0"  # /cpu:0 or /gpu:0

TEST_MODE = "inference"

dataset = car_model.carDataset()
dataset.prepare()
print(dataset.class_names)

with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                              config=config)

weights_path = "path_to_weight"

# Load weights
print("Loading weights ", weights_path)
model.load_weights(weights_path, by_name=True)


def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.

    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size * cols, size * rows))
    return ax

def get_car_boxes(boxes):
    car_boxes = []
    #print("box",boxes)

    for i, box in enumerate(boxes):
        car_boxes.append(box)

    return np.array(car_boxes)


def overlay_mask(image, vertices1):
    mask = np.zeros_like(image)
    if len(mask.shape) == 2:
        cv2.fillPoly(mask, vertices1, 255)
    #         cv2.fillPoly(mask,vertices2,255)
    else:
        cv2.fillPoly(mask, vertices1, (255,) * mask.shape[2])
    # cv2.fillPoly(mask, vertices2, (255,)*mask.shape[2])
    #        cv2.fillPoly(mask,vertices2,(255,)*mask.shape[2])
    #        cv2.fillPoly(mask,vertices3,(255,)*mask.shape[2])

    return cv2.bitwise_and(image, mask)


def add_mask(image, mask):
    vertices1 = np.array([mask], dtype=np.int32)
    return overlay_mask(image, vertices1)

def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors


def apply_mask(image, mask, color, alpha=0.15):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

def display_instances(image, boxes, masks, class_ids, class_names,
                      scores=None, title="",
                      figsize=(16, 16), ax=None,
                      show_mask=True, show_bbox=True,
                      colors=None, captions=None):
    """
    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
    masks: [height, width, num_instances]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # Number of instances
    N = boxes.shape[0]
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    # If no axis is passed, create one and automatically call show()
    auto_show = False
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)
        auto_show = True

    # Generate random colors
    colors = colors or random_colors(N)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    erer=type(image)
    for i in range(N):
        color = colors[i]

        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]
        if show_bbox:
            p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
                                alpha=0.7, linestyle="dashed",
                                edgecolor=color, facecolor='none')
            ax.add_patch(p)

        # Label
        if not captions:
            class_id = class_ids[i]
            score = scores[i] if scores is not None else None
            label = class_names[class_id]
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption,
                color='w', size=11, backgroundcolor="none")

        # Mask
        mask = masks[:, :, i]
        if show_mask:
            masked_image = apply_mask(masked_image, mask, color)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)
    ax.imshow(masked_image.astype(np.uint8))
    if auto_show:
        plt.show()
    return masked_image


def detect_cars(image_, mask):
    im_orig = np.copy(image_)
    image=np.copy(image_)
    image = add_mask(image, mask)

    results = model.detect([image], verbose=1)
    # Display results
    ax = get_ax(1)
    r = results[0]
    im=display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                ['BG',''], ax=ax,
                                title="")

    car_boxes = get_car_boxes(r['rois'])
    #
    # for box in car_boxes:
    #     print("Car: ", box)
    #
    #     y1, x1, y2, x2 = box
    #
    #     cv2.rectangle(im_orig, (x1, y1), (x2, y2), (0, 255, 0), 3)

    plt.imshow(im_orig)
    plt.show()

    return car_boxes
