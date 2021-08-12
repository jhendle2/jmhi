from keywords_handler import KEYWORDS, resolve_keyword
import roman

def open_file_as_lines(file_name):
    print('## Opening File: %s' % file_name)
    lines = []
    with open(file_name) as file:
        for line in file:
            if '\n' in line:
                line = line.strip('\n')
            if line != '':
                if '|' in line:
                    line_without_char = line[1:]
                    num_newlines = 1
                    if len(line_without_char) > 0:
                        num_newlines = int(line_without_char)
                    for i in range(num_newlines):
                        lines.append('')
                else:
                    lines.append(line)
    return lines


def expand_all_keywords(line):
    for key in KEYWORDS.keys():
        if '/' + key in line:
            line = line.replace('/' + key, resolve_keyword(key))
    return line


last_line_was_outline = False
outline_levels = {}

def determine_formatting(line):
    global last_line_was_outline
    format_line = {
        'type': 'NORMAL',  # 'HEADER', 'TITLE', ETC.
        'level': 0,
        'text': line,

        'align': 'LEFT',  # 'CENTER', 'RIGHT'
        'size': 12,  # 'CENTER', 'RIGHT'

        'bold': False,
        'italic': False,
        'underline': False,
        'strikethrough': False,
    }

    if '\center' in format_line['text']:
        format_line['align'] = 'CENTER'
        format_line['text'] = format_line['text'][7:]

    if '\\font' in format_line['text']:
        font_size_index = format_line['text'].index('\\font')
        format_line['text'] = format_line['text'].replace('\\font','')
        font_size_str = ''
        font_size_end_index = 0
        for c in format_line['text'][font_size_index:]:
            if c in '0123456789':
                font_size_str += c
                font_size_end_index += 1
            else:
                break
        format_line['text'] = format_line['text'][len(font_size_str):]
        font_size = int(font_size_str)
        format_line['size'] = font_size

    if '=' in format_line['text']:
        format_line['type'] = 'LINE'
        format_line['bold'] = True
        format_line['text'] = '_'
        format_line['align'] = 'CENTER'
    if '-' in line:
        format_line['type'] = 'TITLE'
        format_line['align'] = 'CENTER'
        format_line['level'] = format_line['text'].count('-') // 2 - 1
        format_line['text'] = format_line['text'].strip('-')

        header_size = 3 - format_line['level']
        if header_size < 1:
            header_size = 1
        format_line['size'] = header_size * format_line['size']
    if '>' in line:
        format_line['type'] = 'HEADER'
        format_line['level'] = format_line['text'].count('>')
        format_line['text'] = format_line['text'].strip('>')

        header_size = 3 - format_line['level']
        if header_size < 1:
            header_size = 1
        format_line['size'] = header_size * format_line['size']
    if '*' in line:
        format_line['type'] = 'BULLET'
        format_line['level'] = format_line['text'].count('*') + 1
        format_line['text'] = format_line['text'].strip('*')
    if '~' in line:
        format_line['type'] = 'OUTLINE'
        format_line['level'] = format_line['text'].count('~') + 1
        format_line['text'] = format_line['text'].strip('~')

        last_line_was_outline = True

        if format_line['level'] in outline_levels.keys():
            outline_levels[format_line['level']] += 1
        else:
            outline_levels[format_line['level']] = 1

        outline_level = format_line['level'] - 1
        outline_level_num = int(outline_levels[format_line['level']])
        outline_str = ''

        if outline_level % 5 == 1:
            outline_str = roman.toRoman(outline_level_num)
        elif outline_level % 5 == 2:
            outline_str = [c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'][(outline_level_num - 1) % 26]
        elif outline_level % 5 == 3:
            outline_str = str(outline_level_num)
        elif outline_level % 5 == 4:
            outline_str = [c for c in 'abcdefghijklmnopqrstuvwxyz'][(outline_level_num - 1) % 26]
        else:
            outline_str = roman.toRoman(outline_level_num).lower()

        format_line['text'] = outline_str + '. ' + format_line['text']
        # format_line['text'] = str(last_outline_level) + '. ' + format_line['text']
        # print('flt:' , last_outline_level, format_line['text'])
        # last_outline_level += 1
    else:
        last_outline_level = 1
        last_line_was_outline = False

    if ':' in line:
        format_line['bold'] = True
        format_line['text'] = format_line['text'].strip(':')
    if ';' in line:
        format_line['italic'] = True
        format_line['text'] = format_line['text'].strip(';')
    if '_' in line:
        format_line['underline'] = True
        format_line['text'] = format_line['text'].strip('_')
    if '$' in line:
        format_line['strikethrough'] = True
        format_line['text'] = format_line['text'].strip('$')

    format_line['text'] = expand_all_keywords(format_line['text'])
    return format_line


def format_all_lines(lines_in):
    lines_out = []
    for line in lines_in:
        lines_out.append(determine_formatting(line))
    return lines_out


def find_minimum_page_width(formatted_lines):
    max_line_length = 0
    for line in formatted_lines:
        modifier = 1
        if line['type'] == 'HEADER':
            modifier = 2
        if line['type'] == 'TITLE':
            modifier = 4
        line_length = modifier * len(line['text'])
        if line_length > max_line_length:
            max_line_length = line_length
    return max_line_length


def find_minimum_page_height(formatted_lines):
    min_page_height = 0
    for line in formatted_lines:
        if line['type'] == 'HEADER':
            min_page_height += 2
        if line['type'] == 'TITLE':
            min_page_height += 4
        else:
            min_page_height += 1
    return min_page_height


if __name__ == '__main__':
    ls = open_file_as_lines('test.fxmt')
    lf = []
    for l in ls:
        lf.append(determine_formatting(l))

    for l in lf:
        print(l)
    #
    # l = 'a2/addb2/eqc2'
    # lo = expand_all_keywords(l)
    # print(lo)
