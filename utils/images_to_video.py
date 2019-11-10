import cv2


def images_to_video(images_paths, output_path, images_per_seconds=10, codec='MJPG'):
    images = [cv2.imread(image_path) for image_path in images_paths]
    height, width, _ = images[0].shape

    video_writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*codec),
        images_per_seconds,
        (width, height)
    )
    for image in images:
        video_writer.write(image)
    video_writer.release()
