import click
import os
from PIL import Image

def extract_frames_from_gif(gif, out):
    if out is None:
        out, _ = os.path.splitext(gif)
        if out == gif:
            out += ".frames"
    if not os.path.exists(out):
        os.makedirs(out, exist_ok=True)
    imobj = Image.open(gif)
    if not imobj.is_animated:
        filename = os.path.join(out, "0.png")
        imobj.save(filename)
        return 1
    else:
        for index in range(0, 53):
            imobj.seek(index)
            filename = os.path.join(out, "{0}.png".format(index))
            imobj.save(filename)
        return imobj.n_frames


@click.command()
@click.argument("image", nargs=1, required=True)
@click.argument("out", nargs=1, required=False)
def main(image, out):
    """Extract frames from gif image.

    IMAGE: The file path of the gif image
    
    OUT: The folder where extraced frames to save
    """
    n_frames = extract_frames_from_gif(image, out)
    click.echo("n_frames = {0}".format(n_frames))


if __name__ == "__main__":
    main()
