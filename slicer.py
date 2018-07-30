import os
from math import sqrt, ceil, floor

from PIL import Image

#from .helpers import get_basename
from helpers import get_basename


class Tile(object):
    """Represents a single tile."""

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    @property
    def basename(self):
        """Strip path and extension. Return base filename."""
        return get_basename(self.filename)

    def generate_filename(self, directory=os.getcwd(), prefix='tile',
                          format='png', path=True):
        """Construct and return a filename for this tile."""
        #directory = directory + '\\tiles'
        #if not os.path.exists(directory):
        #    os.makedirs(directory)
        filename = prefix + '_{col:02d}_{row:02d}.{ext}'.format(
                      col=self.column, row=self.row, ext=format)
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, format='png'):
        if not filename:
            filename = self.generate_filename(format=format)
        self.image.save(filename, format)
        self.filename = filename

    def __repr__(self):
        """Show tile number, and if saved to disk, filename."""
        if self.filename:
            return '<Tile #{} - {}>'.format(self.number,
                                            os.path.basename(self.filename))
        return '<Tile #{}>'.format(self.number)



def slice(filename, cols, rows, save=True):
    """
    Split an image into a specified number of tiles.
    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.
    Kwargs:
       save (bool): Whether or not to save tiles to disk.
    Returns:
        Tuple of :class:`Tile` instances.
    """
    im = Image.open(filename)
    #validate_image(im, number_tiles)

    im_w, im_h = im.size
    #columns, rows = calc_columns_rows(number_tiles)
    #extras = (columns * rows) - number_tiles
    tile_w, tile_h = int(floor(im_w / cols)), int(floor(im_h / rows))

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - cols, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1,
                        int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1
    if save:
        save_tiles(tiles,
                   prefix=get_basename(filename),
                   directory=os.path.dirname(filename))
    return tuple(tiles)

def save_tiles(tiles, prefix='', directory=os.getcwd(), format='png'):
    """
    Write image files to disk. Create specified folder(s) if they
       don't exist. Return list of :class:`Tile` instance.
    Args:
       tiles (list):  List, tuple or set of :class:`Tile` objects to save.
       prefix (str):  Filename prefix of saved tiles.
    Kwargs:
       directory (str):  Directory to save tiles. Created if non-existant.
    Returns:
        Tuple of :class:`Tile` instances.
    """
#    Causes problems in CLI script.
    #if not os.path.exists(directory):
     #   os.makedirs(directory)
    for tile in tiles:
        tile.save(filename=tile.generate_filename(prefix=prefix,
                                                  directory=directory,
                                                  format=format), 
                                                  format=format)
    #88faxkprint(tiles[0])												  
    return tuple(tiles)