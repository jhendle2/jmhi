from interpreter import find_minimum_page_width, find_minimum_page_height
from PIL import Image, ImageDraw, ImageFont


def inches_to_pixels(inches_in : int) -> int:
    pixels_out = 300 * inches_in
    return int(pixels_out)


def font_size_to_pixels(font_size : int) -> int:
    return font_size // 12 * 64


FONT_SIZE = font_size_to_pixels(12)
FONT_COLOR = (0,0,0)
FONT = ImageFont.truetype("arial.ttf", FONT_SIZE)

DEFAULT_A1 = (2550, 3300)  # 8.5 * 11 page

PAGE_SIZE = DEFAULT_A1
PAGE_COLOR = (255, 255, 255)
PAGE = Image.new('RGB', PAGE_SIZE, color=PAGE_COLOR)

VERTICAL_MARGIN = inches_to_pixels(1)
HORIZONTAL_MARGIN = inches_to_pixels(1)
LINE_SPACING = 1 * FONT_SIZE // 2

LAST_LINE = VERTICAL_MARGIN


def set_page(width, height):
    global PAGE_SIZE, PAGE
    PAGE_SIZE = width, height
    PAGE = Image.new('RGB', PAGE_SIZE, color=PAGE_COLOR)


def fit_page_to_lines(formatted_lines):
    global PAGE_SIZE, PAGE
    fmpw = find_minimum_page_width(formatted_lines)
    fmph = find_minimum_page_height(formatted_lines)
    width =  fmpw #  + 2*HORIZONTAL_MARGIN # (fmpw + 2*HORIZONTAL_MARGIN) * int(FONT_SIZE)
    height = fmph # + 2*VERTICAL_MARGIN # (fmph + 2*VERTICAL_MARGIN + LINE_SPACING) * int(FONT_SIZE)
    PAGE_SIZE = width, height
    PAGE = Image.new('RGB', PAGE_SIZE, color=PAGE_COLOR)


def apply_with_formatting(format_line):
    global LAST_LINE
    d = ImageDraw.Draw(PAGE)

    # font = FONT
    new_font_size = font_size_to_pixels(format_line['size'])

    level = format_line['level']
    if level >= 1:
        level -= 1

    if format_line['type'] == 'BULLET':
        format_line['text'] = '* ' + format_line['text']

    if format_line['type'] == 'TITLE':
        level = 0
        header_size = 3 - format_line['level']
        if header_size < 1:
            header_size = 1
        # new_font_size = FONT_SIZE * header_size * 2
        # font = ImageFont.truetype("arial.ttf", new_font_size)

    if format_line['type'] == 'HEADER':
        level = 0
        header_size = 3 - format_line['level']
        if header_size < 1:
            header_size = 1
        new_font_size = FONT_SIZE * header_size

    if format_line['type'] == 'LINE':
        d.line(xy=(HORIZONTAL_MARGIN, LAST_LINE, PAGE_SIZE[0]-HORIZONTAL_MARGIN, LAST_LINE), width=10, fill=(0, 0, 0))
        return

    font = ImageFont.truetype("arial.ttf", new_font_size)

    if format_line['bold'] == True:
        font = ImageFont.truetype("arialbd.ttf", new_font_size)

    horizontal_shift = ( HORIZONTAL_MARGIN + level * FONT_SIZE ) # * FONT_SIZE
    page_width = PAGE_SIZE[0]
    if format_line['align'] == 'CENTER':
        chars_in_line = len(format_line['text'])
        horizontal_shift = ( page_width // 2) - ( chars_in_line * new_font_size ) // 4  # - (HORIZONTAL_MARGIN * FONT_SIZE)//2

    d.text((horizontal_shift, LAST_LINE), format_line['text'], fill=FONT_COLOR, font=font)
    LAST_LINE += new_font_size + LINE_SPACING


def page_add_line(format_line):
    apply_with_formatting(format_line=format_line)


def output_page(outfile, print_margins=False):
    print('## Printing to: %s' % outfile)
    if print_margins:
        margins = get_margin_coords(PAGE_SIZE, HORIZONTAL_MARGIN, VERTICAL_MARGIN)
        show_margins(margins)
    PAGE.save(outfile)


def get_margin_coords(page_size, horizontal_margin, vertical_margin):
    page_width = page_size[0]
    page_height = page_size[1]
    return (
        (horizontal_margin, vertical_margin),
        (horizontal_margin, page_height - vertical_margin),
        (page_width - horizontal_margin, vertical_margin),
        (page_width - horizontal_margin, page_height - vertical_margin),
    )


def show_margins(margins):
    draw = ImageDraw.Draw(PAGE)
    top_left = margins[0]
    top_right = margins[1]
    bot_left = margins[2]
    bot_right = margins[3]
    draw.line(xy=(top_left, top_right), width=5, fill=(255,0,0))
    draw.line(xy=(top_left, bot_left), width=5, fill=(255,0,0))
    draw.line(xy=(bot_left, bot_right), width=5, fill=(255,0,0))
    draw.line(xy=(top_right,bot_right), width=5, fill=(255,0,0))


# if __name__ == '__main__':
#     l = get_margin_coords(PAGE_SIZE, HORIZONTAL_MARGIN, VERTICAL_MARGIN)
#     show_margins(l)
#     PAGE.save('t.png')