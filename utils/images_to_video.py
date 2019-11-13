import math

import numpy as np

import cv2


def images_to_video(images_paths, output_path, images_per_second=10, codec='MJPG', zoom_out_smoothing_window=5):
    """
    Combine images of different sizes in a video

    Args:
        images_paths (List[str]): list of images paths to combine
        output_path (str): path to output the video
        images_per_second (int): number of frames per second
        codec (str): codec in which to output the video
        zoom_out_smoothing_window (int): size of the window used to smooth zoom ratios with a sliding average, in order
                                         to avoid sudden zoom changes.
                                         For example, if you have images with widths [50, 50, 50, 100, 100, 100, 200],
                                         the zoom ratios will be [4, 4, 4, 2, 2, 2, 1], and with a window of size 3, the
                                         smoothed zoom ratios will be [4, 4, 3.33, 2.66, 2, 1.66, 1.33].
    """
    images = [cv2.imread(image_path) for image_path in images_paths]

    widths = [image.shape[1] for image in images]
    accumulated_max_widths = np.maximum.accumulate(widths)
    max_width = accumulated_max_widths[-1]

    resize_ratios = np.full(len(images), max_width) / accumulated_max_widths
    smooth_resize_ratios = np.convolve(
        np.pad(
            resize_ratios,
            (math.ceil((zoom_out_smoothing_window - 1) / 2), math.floor((zoom_out_smoothing_window - 1) / 2)),
            'edge'
        ),
        np.ones((zoom_out_smoothing_window,)) / zoom_out_smoothing_window,
        mode='valid'
    )

    resized_images = [
        cv2.resize(image, (0, 0), fx=resize_ratio, fy=resize_ratio)
        for image, resize_ratio in zip(images, smooth_resize_ratios)
    ]
    resized_max_height = np.max([image.shape[0] for image in images])

    padded_images = [
        cv2.copyMakeBorder(
            resized_image,
            top=0,
            bottom=max(0, resized_max_height - resized_image.shape[0]),
            left=0,
            right=max(0, max_width - resized_image.shape[1]),
            borderType=cv2.BORDER_REPLICATE,
        )
        for resized_image in resized_images
    ]

    video_writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*codec),
        images_per_second,
        (max_width, resized_max_height)
    )

    for padded_image in padded_images:
        video_writer.write(padded_image)
    video_writer.release()
