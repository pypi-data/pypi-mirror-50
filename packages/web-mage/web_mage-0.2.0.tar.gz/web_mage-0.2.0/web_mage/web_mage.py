
import argparse
import errno
import os

import PIL.ExifTags
import PIL.Image

from .formats import ImageFormat, IMG_FORMAT_DEFAULT

class Job(object):
    def __init__(self, source=".", dest=None, formats=[IMG_FORMAT_DEFAULT]):
        self.source = source
        self.formats = formats

        if dest is not None:
            self.dest = dest
        else:
            if os.path.isdir(source):
                self.dest = source
            elif os.path.isfile(source):
                self.dest = os.path.dirname(source)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source)

    def get_filenames(self, source):
        result = []

        if os.path.isdir(source):
            for filename in os.listdir(source):
                if filename.endswith(".jpg"):
                    result.append(os.path.join(source, filename))
        elif os.path.isfile(source):
            result.append(source)

        return result

    def run(self):
        for filename in self.get_filenames(self.source):
            image_set = ImageSet(source_filename=filename,
                                 dest_dir=self.dest,
                                 target_formats=self.formats)
            image_set.optimize()


class ImageSet(object):
    def __init__(self, source_filename=None, dest_dir=None, target_formats=[IMG_FORMAT_DEFAULT]):
        self.source_filename = source_filename
        self.dest_dir = dest_dir
        self.target_formats = target_formats

    @staticmethod
    def transpositions_for_orientation(orientation_code):
        transpositions = []
        if orientation_code == 2:
            transpositions = [PIL.Image.FLIP_LEFT_RIGHT]
        elif orientation_code == 3:
            transpositions = [PIL.Image.ROTATE_180]
        elif orientation_code == 4:
            transpositions = [PIL.Image.FLIP_LEFT_RIGHT,
                              PIL.Image.ROTATE_180]
        elif orientation_code == 5:
            transpositions = [PIL.Image.FLIP_LEFT_RIGHT,
                              PIL.Image.ROTATE_270]
        elif orientation_code == 6:
            transpositions = [PIL.Image.ROTATE_270]
        elif orientation_code == 7:
            transpositions = [PIL.Image.FLIP_LEFT_RIGHT,
                              PIL.Image.ROTATE_90]
        elif orientation_code == 8:
            transpositions = [PIL.Image.ROTATE_90]

        return transpositions

    def optimize(self):
        # Ensure destination directory exists
        if not os.path.exists(self.dest_dir):
            try:
                os.mkdir(self.dest_dir)
            except OSError:
                print("ERROR: Could not create directory %s! Aborting.", self.dest_dir)
                raise

        for image_format in self.target_formats:
            with PIL.Image.open(self.source_filename) as image:
                exif_data = {
                    PIL.ExifTags.TAGS[k]: v
                    for k, v in image._getexif().items()
                    if k in PIL.ExifTags.TAGS
                }

                ((width, height), quality) = image_format.dimensions_for_image(image)
                image = image.resize((width, height), PIL.Image.ANTIALIAS)

                for transposition in ImageSet.transpositions_for_orientation(exif_data['Orientation']):
                    image = image.transpose(transposition)

                new_filename = image_format.get_tagged_filename(self.source_filename)

                output_path = os.path.join(self.dest_dir, new_filename)
                image.save(output_path, quality=quality, optimize=True)

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("--version", help="display version number")
    parser.add_argument("source", help="the file (or directory of files) to be optimized")
    parser.add_argument("destination", help="the output directory for optimized files (default cwd)",
                                       default=".")
    args = parser.parse_args()

    main_job = Job(source=args.source, dest=args.destination)
    main_job.run()
    #myset = ImageSet(source_file=infile, destination=outfile)
    #myset.optimize()


