# @Author: yican.kz
# @Date: 2019-08-02 11:38:57
# @Last Modified by:   yican.kz
# @Last Modified time: 2019-08-02 11:38:57

# Standard libraries
import random

# Third party libraries
import torch
import torchvision.transforms.functional as FT


# ==============================================================================
# 图像相关
# ==============================================================================
def xyccwd_to_xymmmm(cxcy):
    """Convert bounding boxes from center-size coordinates (c_x, c_y, w, h) to boundary coordinates
    (x_min, y_min, x_max, y_max)

    Parameters
    ----------
    cxcy : PyTorch tensor
        Bounding boxes in center-size coordinates, a tensor of size (n_boxes, 4)

    Returns
    -------
    PyTorch tensor
        Bounding boxes in boundary coordinates, a tensor of size (n_boxes, 4)
    """

    return torch.cat([cxcy[:, :2] - cxcy[:, 2:] / 2, cxcy[:, :2] + cxcy[:, 2:] / 2], dim=1)


def xymmmm_to_xyccwd(xy):
    """Convert bounding boxes from boundary coordinates (x_min, y_min, x_max, y_max)
        to center-size coordinates (c_x, c_y, w, h).

    Parameters
    ----------
    xy : Pytorch tensor
        Bounding boxes in boundary coordinates, a tensor of size (n_boxes, 4)

    Returns
    -------
    Pytorch tensor
        bounding boxes in center-size coordinates, a tensor of size (n_boxes, 4)
    """

    return torch.cat([(xy[:, 2:] + xy[:, :2]) / 2, xy[:, 2:] - xy[:, :2]], 1)  # c_x, c_y  # w, h


def xyccwd_to_xygcgcgwgh(cxcy, priors_cxcy):
    """Encode bounding boxes (that are in center-size form) w.r.t. the corresponding prior boxes
        (that are in center-size form).

        For the center coordinates, find the offset with respect to the prior box,
        and scale by the size of the prior box.
        For the size coordinates, scale by the size of the prior box, and convert to the log-space.

        In the model, we are predicting bounding box coordinates in this encoded form.

        # The 10 and 5 below are referred to as 'variances' in the original Caffe repo, completely empirical
        # They are for some sort of numerical conditioning, for 'scaling the localization gradient'
        # See https://github.com/weiliu89/caffe/issues/155
    Parameters
    ----------
    cxcy : Pytorch tensor
        Bounding boxes in center-size coordinates, a tensor of size (n_priors, 4)
    priors_cxcy : Pytorch tensor
        Prior boxes with respect to which the encoding must be performed, a tensor of size (n_priors, 4)

    Returns
    -------
    Pytorch tensor
        Encoded bounding boxes, a tensor of size (n_priors, 4)
    """

    return torch.cat(
        [
            (cxcy[:, :2] - priors_cxcy[:, :2]) / (priors_cxcy[:, 2:] / 10),  # g_c_x, g_c_y
            torch.log(cxcy[:, 2:] / priors_cxcy[:, 2:]) * 5,
        ],
        1,
    )


def xygcgcgwgh_to_xyccwd(gcxgcy, priors_cxcy):
    """Decode bounding box coordinates predicted by the model, since they are encoded in the form mentioned above.
    They are decoded into center-size coordinates. This is the inverse of the function above.

    Parameters
    ----------
    gcxgcy : Pytorch tensor
        Encoded bounding boxes, i.e. output of the model, a tensor of size (n_priors, 4)
    priors_cxcy : Pytorch tensor
        Prior boxes with respect to which the encoding is defined, a tensor of size (n_priors, 4)

    Returns
    -------
    Pytorch tensor
        Decoded bounding boxes in center-size form, a tensor of size (n_priors, 4)
    """

    return torch.cat(
        [
            gcxgcy[:, :2] * priors_cxcy[:, 2:] / 10 + priors_cxcy[:, :2],  # c_x, c_y
            torch.exp(gcxgcy[:, 2:] / 5) * priors_cxcy[:, 2:],
        ],
        1,
    )


def find_intersection(set_1, set_2):
    """Find the intersection of every box combination between two sets of boxes that are in boundary coordinates.

    Parameters
    ----------
    set_1 : Pytorch tensor
        Set 1, a tensor of dimensions (n1, 4)
    set_2 : Pytorch tensor
        Set 2, a tensor of dimensions (n2, 4)

    Returns
    -------
    Pytorch tensor
        Intersection of each of the boxes in set 1 with respect to each of the boxes in set 2,
        a tensor of dimensions (n1, n2)
    """

    lower_left = torch.max(set_1[:, :2].unsqueeze(1), set_2[:, :2].unsqueeze(0))  # (n1, n2, 4)
    upper_right = torch.min(set_1[:, 2:].unsqueeze(1), set_2[:, 2:].unsqueeze(0))  # (n1, n2, 4)
    dims_intersection = torch.clamp(upper_right - lower_left, min=0)  # (n1, n2, 2)
    return dims_intersection[:, :, 0] * dims_intersection[:, :, 1]  # (n1, n2)


def find_jaccard_overlap(set_1, set_2):
    """Find the Jaccard Overlap (IoU) of every box combination between two sets of boxes
        that are in boundary coordinates.

    Parameters
    ----------
    set_1 : Pytorch tensor
        Set 1, a tensor of dimensions (n1, 4)
    set_2 : Pytorch tensor
        Set 2, a tensor of dimensions (n2, 4)

    Returns
    -------
    Pytorch tensor
        Jaccard Overlap of each of the boxes in set 1 with respect to each of the boxes in set 2,
        a tensor of dimensions (n1, n2)
    """

    areas_intersection = find_intersection(set_1, set_2)  # (n1, n2)

    areas_set_1 = (set_1[:, 2] - set_1[:, 0]) * (set_1[:, 3] - set_1[:, 1])  # (n1)
    areas_set_2 = (set_2[:, 2] - set_2[:, 0]) * (set_2[:, 3] - set_2[:, 1])  # (n2)

    areas_union = areas_set_1.unsqueeze(1) + areas_set_2.unsqueeze(0) - areas_intersection  # (n1, n2)

    return areas_intersection / areas_union  # (n1, n2)


# Some augmentation functions below have been adapted from
# From https://github.com/amdegroot/ssd.pytorch/blob/master/utils/augmentations.py
def expand(image, boxes, filler):
    """Perform a zooming out operation by placing the image in a larger canvas of filler material.
    Helps to learn to detect smaller objects.

    Parameters
    ----------
    image : Pytorch tensor
        Image, a tensor of dimensions (3, original_h, original_w)
    boxes : Pytorch tensor
        Bounding boxes in boundary coordinates, a tensor of dimensions (n_objects, 4)
    filler : list
        RBG values of the filler material, a list like [R, G, B]

    Returns
    -------
    new_image : Pytorch tensor
        Expanded image
    new_boxes : Pytorch tensor
        Updated bounding box coordinates
    """

    # Calculate dimensions of proposed expanded (zoomed-out) image
    original_h = image.size(1)
    original_w = image.size(2)
    max_scale = 4
    scale = random.uniform(1, max_scale)
    new_h = int(scale * original_h)
    new_w = int(scale * original_w)

    # Create such an image with the filler
    filler = torch.FloatTensor(filler)  # (3)
    new_image = torch.ones((3, new_h, new_w), dtype=torch.float) * filler.unsqueeze(1).unsqueeze(1)  # (3, new_h, new_w)
    # Note - do not use expand() like new_image = filler.unsqueeze(1).unsqueeze(1).expand(3, new_h, new_w)
    # because all expanded values will share the same memory, so changing one pixel will change all

    # Place the original image at random coordinates in this new image (origin at top-left of image)
    left = random.randint(0, new_w - original_w)
    right = left + original_w
    top = random.randint(0, new_h - original_h)
    bottom = top + original_h
    new_image[:, top:bottom, left:right] = image

    # Adjust bounding boxes' coordinates accordingly
    new_boxes = boxes + torch.FloatTensor([left, top, left, top]).unsqueeze(
        0
    )  # (n_objects, 4), n_objects is the no. of objects in this image

    return new_image, new_boxes


def random_crop(image, boxes, labels, difficulties):
    """Performs a random crop in the manner stated in the paper. Helps to learn to detect larger and partial objects.
    Note that some objects may be cut out entirely.
    Adapted from https://github.com/amdegroot/ssd.pytorch/blob/master/utils/augmentations.py

    Parameters
    ----------
    image : Pytorch tensor
        A tensor of dimensions (3, original_h, original_w)
    boxes : Pytorch tensor
        Bounding boxes in boundary coordinates, a tensor of dimensions (n_objects, 4)
    labels : Pytorch tensor
        Labels of objects, a tensor of dimensions (n_objects)
    difficulties : Pytorch tensor
        Difficulties of detection of these objects, a tensor of dimensions (n_objects)

    Returns
    -------
        Cropped image, updated bounding box coordinates, updated labels, updated difficulties
    """

    original_h = image.size(1)
    original_w = image.size(2)
    # Keep choosing a minimum overlap until a successful crop is made
    while True:
        # Randomly draw the value for minimum overlap
        min_overlap = random.choice([0.0, 0.1, 0.3, 0.5, 0.7, 0.9, None])  # 'None' refers to no cropping

        # If not cropping
        if min_overlap is None:
            return image, boxes, labels, difficulties

        # Try up to 50 times for this choice of minimum overlap
        # This isn't mentioned in the paper, of course, but 50 is chosen in paper authors' original Caffe repo
        max_trials = 50
        for _ in range(max_trials):
            # Crop dimensions must be in [0.3, 1] of original dimensions
            # Note - it's [0.1, 1] in the paper, but actually [0.3, 1] in the authors' repo
            min_scale = 0.3
            scale_h = random.uniform(min_scale, 1)
            scale_w = random.uniform(min_scale, 1)
            new_h = int(scale_h * original_h)
            new_w = int(scale_w * original_w)

            # Aspect ratio has to be in [0.5, 2]
            aspect_ratio = new_h / new_w
            if not 0.5 < aspect_ratio < 2:
                continue

            # Crop coordinates (origin at top-left of image)
            left = random.randint(0, original_w - new_w)
            right = left + new_w
            top = random.randint(0, original_h - new_h)
            bottom = top + new_h
            crop = torch.FloatTensor([left, top, right, bottom])  # (4)

            # Calculate Jaccard overlap between the crop and the bounding boxes
            overlap = find_jaccard_overlap(
                crop.unsqueeze(0), boxes
            )  # (1, n_objects), n_objects is the no. of objects in this image
            overlap = overlap.squeeze(0)  # (n_objects)

            # If not a single bounding box has a Jaccard overlap of greater than the minimum, try again
            if overlap.max().item() < min_overlap:
                continue

            # Crop image
            new_image = image[:, top:bottom, left:right]  # (3, new_h, new_w)

            # Find centers of original bounding boxes
            bb_centers = (boxes[:, :2] + boxes[:, 2:]) / 2.0  # (n_objects, 2)

            # Find bounding boxes whose centers are in the crop
            centers_in_crop = (
                (bb_centers[:, 0] > left)
                * (bb_centers[:, 0] < right)
                * (bb_centers[:, 1] > top)
                * (bb_centers[:, 1] < bottom)
            )  # (n_objects), a Torch uInt8/Byte tensor, can be used as a boolean index

            # If not a single bounding box has its center in the crop, try again
            if not centers_in_crop.any():
                continue

            # Discard bounding boxes that don't meet this criterion
            new_boxes = boxes[centers_in_crop, :]
            new_labels = labels[centers_in_crop]
            new_difficulties = difficulties[centers_in_crop]

            # Calculate bounding boxes' new coordinates in the crop
            new_boxes[:, :2] = torch.max(new_boxes[:, :2], crop[:2])  # crop[:2] is [left, top]
            new_boxes[:, :2] -= crop[:2]
            new_boxes[:, 2:] = torch.min(new_boxes[:, 2:], crop[2:])  # crop[2:] is [right, bottom]
            new_boxes[:, 2:] -= crop[:2]

            return new_image, new_boxes, new_labels, new_difficulties


def flip(image, boxes):
    """Flip image horizontally.

    Parameters
    ----------
    image : PIL Image
        A PIL Image
    boxes : Pytorch tensor
        Bounding boxes in boundary coordinates, a tensor of dimensions (n_objects, 4)

    Returns
    -------
    new_image : Pytorch tensor
        Flipped image
    new_boxes : Pytorch tensor
        Updated bounding box coordinates
    """

    # Flip image
    new_image = FT.hflip(image)

    # Flip boxes
    new_boxes = boxes
    new_boxes[:, 0] = image.width - boxes[:, 0] - 1
    new_boxes[:, 2] = image.width - boxes[:, 2] - 1
    new_boxes = new_boxes[:, [2, 1, 0, 3]]

    return new_image, new_boxes


def resize(image, boxes, dims=(300, 300), return_percent_coords=True):
    """Resize image. For the SSD300, resize to (300, 300).
    Since percent/fractional coordinates are calculated for the bounding boxes (w.r.t image dimensions) in this process,
    you may choose to retain them.

    Parameters
    ----------
    image : PIL Image
        [description]
    boxes : Pytorch tensor
        Bounding boxes in boundary coordinates, a tensor of dimensions (n_objects, 4)
    dims : tuple, optional
        Resized image, updated bounding box coordinates (or fractional coordinates), by default (300, 300)
    return_percent_coords : bool, optional
        [description], by default True

    Returns
    -------
    [type]
        [description]
    """

    # Resize image
    new_image = FT.resize(image, dims)

    # Resize bounding boxes
    old_dims = torch.FloatTensor([image.width, image.height, image.width, image.height]).unsqueeze(0)
    new_boxes = boxes / old_dims  # percent coordinates

    if not return_percent_coords:
        new_dims = torch.FloatTensor([dims[1], dims[0], dims[1], dims[0]]).unsqueeze(0)
        new_boxes = new_boxes * new_dims

    return new_image, new_boxes


def photometric_distort(image):
    """Distort brightness, contrast, saturation, and hue, each with a 50% chance, in random order.

    Parameters
    ----------
    image : PIL Image

    Returns
    -------
        Distorted image
    """

    new_image = image

    distortions = [FT.adjust_brightness, FT.adjust_contrast, FT.adjust_saturation, FT.adjust_hue]

    random.shuffle(distortions)

    for d in distortions:
        if random.random() < 0.5:
            if d.__name__ == "adjust_hue":
                # Caffe repo uses a 'hue_delta' of 18 - we divide by 255 because PyTorch needs a normalized value
                adjust_factor = random.uniform(-18 / 255.0, 18 / 255.0)
            else:
                # Caffe repo uses 'lower' and 'upper' values of 0.5 and 1.5 for brightness, contrast, and saturation
                adjust_factor = random.uniform(0.5, 1.5)

            # Apply this distortion
            new_image = d(new_image, adjust_factor)

    return new_image


def transform(image, boxes, labels, difficulties, split):
    """Apply the transformations above.

    Parameters
    ----------
    image : PIL Image
        [description]
    boxes : [type]
        Bounding boxes in boundary coordinates, a tensor of dimensions (n_objects, 4)
    labels : [type]
        Labels of objects, a tensor of dimensions (n_objects)
    difficulties : [type]
        Difficulties of detection of these objects, a tensor of dimensions (n_objects)
    split : [type]
        One of 'TRAIN' or 'TEST', since different sets of transformations are applied

    Returns
    -------
        transformed image, transformed bounding box coordinates, transformed labels, transformed difficulties
    """

    assert split in {"TRAIN", "TEST"}

    # Mean and standard deviation of ImageNet data that our base VGG from torchvision was trained on
    # see: https://pytorch.org/docs/stable/torchvision/models.html
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    new_image = image
    new_boxes = boxes
    new_labels = labels
    new_difficulties = difficulties
    # Skip the following operations if validation/evaluation
    if split == "TRAIN":
        # A series of photometric distortions in random order, each with 50% chance of occurrence, as in Caffe repo
        new_image = photometric_distort(new_image)

        # Convert PIL image to Torch tensor
        new_image = FT.to_tensor(new_image)

        if 0:
            # Expand image (zoom out) with a 50% chance - helpful for training detection of small objects
            # Fill surrounding space with the mean of ImageNet data that our base VGG was trained on
            if random.random() < 0.5:
                new_image, new_boxes = expand(new_image, boxes, filler=mean)

            # Randomly crop image (zoom in)
            new_image, new_boxes, new_labels, new_difficulties = random_crop(
                new_image, new_boxes, new_labels, new_difficulties
            )

        # Convert Torch tensor to PIL image
        new_image = FT.to_pil_image(new_image)

        # Flip image with a 50% chance
        if random.random() < 0.5:
            new_image, new_boxes = flip(new_image, new_boxes)

    # Resize image to (300, 300) - this also converts absolute boundary coordinates to their fractional form
    new_image, new_boxes = resize(new_image, new_boxes, dims=(300, 300))

    # Convert PIL image to Torch tensor
    new_image = FT.to_tensor(new_image)

    # Normalize by mean and standard deviation of ImageNet data that our base VGG was trained on
    new_image = FT.normalize(new_image, mean=mean, std=std)

    return new_image, new_boxes, new_labels, new_difficulties
