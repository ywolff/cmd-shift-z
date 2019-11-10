import cv2


def images_to_video(images_paths, output_path, images_per_second=10, codec='MJPG'):
    """
    Combine images in a video

    Args:
        images_paths (List[str]): list of images paths to combine
        output_path (str): path to output the video
        images_per_second (int): number of frames per second
        codec (str): codec in which to output the video
    """
    images = []
    max_height = 0
    max_width = 0

    for image_path in images_paths:
        image = cv2.imread(image_path)
        height, width, _ = image.shape
        if height > max_height:
            max_height = height
        if width > max_width:
            max_width = width
        images.append(image)

    video_writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*codec),
        images_per_second,
        (max_width, max_height)
    )

    for image in images:
        height, width, _ = image.shape
        padded_image = cv2.copyMakeBorder(
            image,
            top=0,
            bottom=max(0, max_height - height),
            left=0,
            right=max(0, max_width - width),
            borderType=cv2.BORDER_REPLICATE
        )
        video_writer.write(padded_image)
    video_writer.release()
