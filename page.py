from PIL import Image, ImageDraw, ImageFont

def font_size_to_pixels(font_size : int) -> int:
    return font_size // 12 * 64


def inches_to_pixels(inches_in : int) -> int:
    pixels_out = 300 * inches_in
    return int(pixels_out)

FONT_SIZE = font_size_to_pixels(12)
FONT_COLOR = (0,0,0)
FONT = ImageFont.truetype("arial.ttf", FONT_SIZE)

DEFAULT_A4 = (2480, 3508)  # 8.5 * 11 page
DEFAULT_A5 = (1748, 2480)
DEFAULT_A6 = (1240, 1748)
DEFAULT_A7 = (874, 1240)
DEFAULT_DL = (2480, 1169) # Comp slip
DEFAULT_BC = (1004, 650) # Business card

WHITE = (255, 255, 255)


class Page:
    def __init__(self, size=DEFAULT_A4, vertical=1, horizontal=1, spacing=1, color=WHITE, page_num=0,
                 filename='fxmt.fxmt', outfile='fxmt.png', color_code='RGB', showmargins=False):
        self.size = size
        self.vertical = vertical
        self.horizontal = horizontal
        self.spacing = spacing
        self.last_line = vertical + spacing
        self.page_num = page_num
        self.filename = filename
        self.showmargins = showmargins

        if outfile is None:
            self.outfile = self.filename.removesuffix('.jmhi')+'.png'
        else:
            self.outfile = outfile

        self.page = Image.new(color_code, (vertical, horizontal), color=color)
        self.formatted_lines = []

    def add_line(self, formatted_line):
        self.formatted_lines.append(formatted_line)

    def output(self):
        print('## Printing to: %s' % self.outfile)
        if self.showmargins:  # TODO - Implement
            pass
            # margins = get_margin_coords(PAGE_SIZE, HORIZONTAL_MARGIN, VERTICAL_MARGIN)
            # show_margins(margins)
        self.page.save(self.outfile)

    def __repr__(self):
        str_out = self.outfile + ' [' + str(self.page_num) + '] ' + '(' + self.filename + ')\n'
        for line in self.formatted_lines:
            str_out += '* ' + str(line) + '\n'
        return str_out


class Document:
    def __init__(self, document_name):
        self.document_name = document_name
        self.pages = []

    def add_page(self, page):
        page.page_num = len(self.pages) + 1
        self.pages.append(page)

    def get_page(self, index):
        return self.pages[index]

    def __repr__(self):
        str_out = self.document_name + '\n'
        for page in self.pages:
            str_out += '[' + str(page.page_num) + '] ' + page.filename + ' -> ' + page.outfile + '\n'
        return str_out


if __name__ == '__main__':
    page1 = Page(filename='test_file1.jmhi')
    page2 = Page(filename='test_file2.jmhi')
    doc1 = Document(document_name='testdoc.jmhd')
    doc1.add_page(page1)
    doc1.add_page(page2)
    print(doc1)
