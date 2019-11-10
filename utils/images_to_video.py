import cv2


def images_to_video(images_paths, output_path, images_per_seconds=10, codec='MJPG'):
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
        images_per_seconds,
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
