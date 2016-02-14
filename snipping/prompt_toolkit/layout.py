"""snipping.prompt_toolkit.layout

wrappers for layout
"""

from prompt_toolkit.layout import containers
from prompt_toolkit.layout import controls
from prompt_toolkit.layout import dimension
from prompt_toolkit.layout import margins
from prompt_toolkit.layout import processors

from snipping.prompt_toolkit import style
from snipping.prompt_toolkit import buffers


def dim(min_=None, max_=None, exact=None):
    if exact is not None:
        return dimension.LayoutDimension.exact(exact)
    return dimension.LayoutDimension(min=min_, max=max_)


def horizontal_line(min_width=None, max_width=None, char=' '):
    height = dim(exact=1)
    width = dim(min_=min_width, max_=max_width)
    content = controls.FillControl(char, token=style.Line)
    return containers.Window(width=width, height=height, content=content)


def vertical_line(min_height=None, max_height=None, char=' '):
    width = dim(exact=1)
    height = dim(min_=min_height, max_=max_height)
    content = controls.FillControl(char, token=style.Line)
    return containers.Window(width=width, height=height, content=content)


def normal_text_window(name=None, lang=None, lineno=False,
                       leading_space=False, trailing_space=False,
                       width=None, height=None):
    if name is None:
        name = buffers.DEFAULT_BUFFER
    bf_attrs = {'buffer_name': name,
                'lexer': style.get_lexer_by_lang(lang)}

    input_processors = []
    if leading_space:
        input_processors.append(processors.ShowLeadingWhiteSpaceProcessor())
    if trailing_space:
        input_processors.append(processors.ShowTrailingWhiteSpaceProcessor())
    if input_processors:
        bf_attrs['input_processors'] = input_processors

    win_attrs = {}
    left_margins = []
    if lineno:
        left_margins.append(margins.NumberredMargin(name))
    if left_margins:
        win_attrs['left_margins'] = left_margins

    if height is not None:
        win_attrs['height'] = height
    if width is not None:
        win_attrs['width'] = width

    content = controls.BufferControl(**bf_attrs)
    return containers.Window(content=content, **win_attrs)


def horizontal_tokenlist_window(get_tokens, align='left'):
    tlc_attrs = {}
    if align == 'center':
        tlc_attrs['align_center'] = True
    if align == 'right':
        tlc_attrs['align_right'] = True
    height = dim(exact=1)
    content = controls.TokenListControl(get_tokens, **tlc_attrs)
    return containers.Window(height=height, content=content)


def window_rows(windows):
    return containers.HSplit(windows)


def window_columns(windows):
    return containers.VSplit(windows)
