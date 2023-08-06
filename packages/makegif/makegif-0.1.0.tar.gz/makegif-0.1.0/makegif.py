import os
import glob
import imageio
import click


def _filename_key(filename):
    basename = os.path.basename(filename)
    name, _ = os.path.splitext(basename)
    if name.isdigit():
        return int(name)
    else:
        return name


def make_gif(images, output, duration=0.3):
    if isinstance(images, str):
        if os.path.isdir(images):
            images = glob.glob(os.path.join(images, "*"))
            images.sort(key=_filename_key)
        else:
            images = [images]
    frames = []
    for image in images:
        frame = imageio.imread(image)
        frames.append(frame)
    return imageio.mimsave(output, frames, "GIF", duration=duration)


@click.command()
@click.option("-o", "--output", required=True, help="Output image path.")
@click.option("-d", "--duration", type=float, default=0.1, help="Gap time between frames.")
@click.argument("image_folder", nargs=1, required=False)
def makegif_cli(output, duration, image_folder):
    """Make gif from images.
    """
    make_gif(image_folder, output, duration)


if __name__ == "__main__":
    makegif_cli()
