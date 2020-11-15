from math import ceil
import re
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
    bits_per_pixel = 1
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


def create_pixel_data(pixels, width):
    bytes_in_row = ceil(width/32)*4
    row_size = ceil(width/8)
    pixels.reverse()
    pix_str = ''.join(map(str, pixels))

    rows = re.findall('\\d{'+str(width)+'}', pix_str)
    chunk_len = width if width < 8 else 8
    res = []
    for i in rows:
        res.extend(re.findall('\\d{'+str(chunk_len)+'}', i))
        if width % 8 != 0:
            i_sub = re.sub('\\d{'+str(chunk_len)+'}', '', i)
            res.append(i_sub)
    res = [val.ljust(8, '0') for val in res]

    row_str =  ''.join(res)
    rows = re.findall('\\d{'+str(8*row_size)+'}', row_str)
    rows = [val.ljust(8*bytes_in_row, '0') for val in rows]

    row_str =  ''.join(rows)
    rows = re.findall(r'\d{8}', row_str)
    rows = [int(byte, base=2) for byte in rows]

    pixel_data = pack(f'<{len(rows)}B', *rows)
    return pixel_data


def create_monochrome_bitmap(file_name, pixels, width, height):
    with open(file_name, 'wb') as f:
        f.write(create_header(width, height))
        f.write(create_info_header(width, height))
        f.write(create_color_pallet())
        f.write(create_pixel_data(pixels, width))


if __name__ == '__main__':
    width = 4
    height = 4
    pix = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    create_monochrome_bitmap('test.bmp', pix, 12, 4)
