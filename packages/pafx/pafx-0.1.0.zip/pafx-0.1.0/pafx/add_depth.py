from pafx.utils import get_color_value, istransparent, process_pixels


def add_depth(src, color='black'):
    """Add a 1px line below the non-transparent pixels of src"""
    def fcn(dst, src, xy):
        if not istransparent(src, xy):
            return
        x, y = xy
        if not istransparent(src, (x, y - 1)):
            dst.putpixel(xy, color)

    color = get_color_value(src, color)
    return process_pixels(src, fcn)
