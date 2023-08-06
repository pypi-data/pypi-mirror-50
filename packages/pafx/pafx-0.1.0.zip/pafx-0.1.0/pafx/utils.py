from PIL import ImageColor


def get_color_value(img, color):
    """Given an image and a color, try to find the best color value. For RGB
    images, it's a simple conversion. For P images, it looks in the image
    palette"""

    if type(color) == str:
        color = ImageColor.getrgb(color)

    if img.mode == 'RGB' or img.mode == 'RGBA':
        return color
    if img.mode == 'P':
        color = list(color)
        palette = img.getpalette()
        transparent_idx = img.info['transparency']
        for i in range(0, len(palette), 3):
            rgb = palette[i:i + 3]
            if rgb == color:
                idx = i // 3
                if idx != transparent_idx:
                    return idx
        raise ValueError(
                'Cannot find color {} in image'.format(color))
    else:
        raise ValueError(
                'Cannot get color value for images of type {}'.format(img.mode))


def istransparent(img, xy, default=True):
    x, y = xy
    w, h = img.size
    if x < 0 or x >= w or y < 0 or y >= h:
        return default
    return get_pixel_alpha(img, xy) == 0


def process_pixels(src, fcn):
    dst = src.copy()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            fcn(dst, src, (x, y))
    return dst


def get_pixel_alpha(img, xy):
    pixel = img.getpixel(xy)
    if img.mode == 'RGBA':
        return pixel[3] == 0
    elif img.mode == 'RGB':
        return 255
    elif img.mode == 'P':
        transparent_idx = img.info['transparency']
        if pixel == transparent_idx:
            return 0
        else:
            return 255
    else:
        raise ValueError(
                'Cannot get alpha for images of type {}'.format(img.mode))
