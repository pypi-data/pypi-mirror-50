from PIL import Image


def clone_format(src, size, color=0):
    """Create an empty image of size `size` using the same mode and palette
    as image `src`"""
    dst = Image.new(src.mode, size, color)
    dst.info = src.info
    if dst.mode == 'P':
        dst.putpalette(src.getpalette())
    return dst
