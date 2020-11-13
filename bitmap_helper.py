from struct import pack


def create_header(width, height):
    file_type = 19778
    reserved_1 = 0
    reserved_2 = 0
    pixel_data_offset = 62
    file_size = pixel_data_offset + 1 * width * height
    return pack('<HL2HL', file_type, file_size, reserved_1, reserved_2, pixel_data_offset)


def create_info_header(width, height):
    header_size = 40
    image_width = width
    image_height = height
    planes = 1
    bits_per_pixel = 8
    compression = 0
    image_size = 0
    x_pixels_per_meter = 0
    y_pixels_per_meter = 0
    total_colors = 0
    important_colors = 0
    return pack('<3L2H6L', header_size,
                image_width, image_height,
                planes, bits_per_pixel,
                compression, image_size,
                x_pixels_per_meter, y_pixels_per_meter,
                total_colors, important_colors)


def create_color_pallet():
    color_0 = (0, 0, 0, 0)
    color_1 = (255, 255, 255, 0)
    return pack('<8B', *color_0, *color_1)


def create_pixel_data(pixels):
    pixels.reverse()
    pixel_data = pack(f'<{len(pixels)}B', *pixels)
    return pixel_data


def create_monochrome_bitmap(file_name, pixels, width, height):
    with open(file_name, 'wb') as f:
        f.write(create_header(width, height))
        f.write(create_info_header(width, height))
        f.write(create_color_pallet())
        f.write(create_pixel_data(pixels))


if __name__ == '__main__':
    width = 4
    height = 4
    pix = [0, 1, 1, 0,
           1, 0, 0, 1,
           1, 1, 1, 1,
           1, 0, 0, 1]
    create_monochrome_bitmap('test.bmp', pix, 4, 4)
