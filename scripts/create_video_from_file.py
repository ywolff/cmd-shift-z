import os
from os.path import splitext

import click
import imgkit
from tqdm import tqdm

from utils.code_to_html import code_to_html
from utils.generate_sub_versions import generate_all_sub_versions_from_list
from utils.images_to_video import images_to_video
from utils.git_utils import get_file_history


@click.option(
    '--repository', '-r',
    help='Path to a git local repository, or link to a remote repository.',
    required=True,
)
@click.option(
    '--file_path', '-f',
    help='Path to the file from which you want to create a video.',
    required=True,
)
@click.option(
    '--branch', '-b',
    help='Git branch where to find the file history.',
    default='master',
)
@click.option(
    '--output', '-o',
    help='Output path for the video.',
    required=True,
)
@click.option(
    '--tmp_dir', '-t',
    help='Temporary directory to output intermediary files.',
    default='tmp',
)
@click.command()
def create_video_from_file(repository, file_path, branch, output, tmp_dir):
    """
    Generate a video from a file git history on a given branch of a given repository (url or local path).
    """
    file_name_without_ext, ext = splitext(os.path.basename(file_path))
    os.makedirs(tmp_dir, exist_ok=True)
    file_history = get_file_history(repository, file_path, branch, tmp_dir)
    file_generated_history = generate_all_sub_versions_from_list(file_history)

    images_paths = []

    for index, file_content in enumerate(tqdm(file_generated_history, desc='Generating images...')):
        html_file_path = os.path.join(tmp_dir, f'{file_name_without_ext}_{index}.html')
        css_file_path = os.path.join(tmp_dir, f'{file_name_without_ext}_{index}.css')
        image_file_path = os.path.join(tmp_dir, f'{file_name_without_ext}_{index}.png')

        code_to_html(file_content, file_path, html_file_path, css_file_path)
        imgkit.from_file(
            str(html_file_path),
            str(image_file_path),
            options={
                'quiet': 1,
                'width': 1,
                # `width` option is handled as a min_width. Setting a value of 1 instead of 1024 default value allows to
                # output an image with the smallest width still containing all html content.
            }
        )
        images_paths.append(str(image_file_path))

    images_to_video(images_paths, output)
    click.launch(output)


if __name__ == '__main__':
    create_video_from_file()
