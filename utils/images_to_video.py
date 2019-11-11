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
    max_width = 0
    for image_path in images_paths:
        image = cv2.imread(image_path)
        _, width, _ = image.shape
        if width > max_width:
            max_width = width
        images.append(image)

    resized_images = []
    max_width_until_now = 0
    resized_max_height = 0
    for image in images:
        _, width, _ = image.shape
        if width > max_width_until_now:
            max_width_until_now = width
        resize_ratio = max_width / max_width_until_now
        resized_image = cv2.resize(image, (0, 0), fx=resize_ratio, fy=resize_ratio)
        height, _, _ = resized_image.shape
        if height > resized_max_height:
            resized_max_height = height
        resized_images.append(resized_image)

    video_writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*codec),
        images_per_second,
        (max_width, resized_max_height)
    )

    for resized_image in resized_images:
        height, width, _ = resized_image.shape
        padded_image = cv2.copyMakeBorder(
            resized_image,
            top=0,
            bottom=max(0, resized_max_height - height),
            left=0,
            right=max(0, max_width - width),
            borderType=cv2.BORDER_REPLICATE,
        )
        print('padded:', padded_image.shape)
        video_writer.write(padded_image)
    video_writer.release()
