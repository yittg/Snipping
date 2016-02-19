"""snipping.prompt_toolkit.layout

wrappers for layout
"""

from prompt_toolkit.key_binding import vi_state
from prompt_toolkit.layout import containers
from prompt_toolkit.layout import controls
from prompt_toolkit.layout import dimension
from prompt_toolkit.layout import highlighters
from prompt_toolkit.layout import margins
from prompt_toolkit.layout import processors
from prompt_toolkit.layout import screen
from prompt_toolkit.layout import toolbars

from snipping.prompt_toolkit import style
from snipping.prompt_toolkit import buffers


class NumberredMargin(margins.NumberredMargin):
    """ A simple and customized `create_margin` of origin `NumberredMargin`
    """

    def create_margin(self, cli, wr_info, width, height):
        visible_line_to_input_line = wr_info.visible_line_to_input_line

        token = style.Token.LineNumber
        token_error = style.ErrorLineNo

        result = []

        app = cli.application
        snippet = buffers.get_content(app)
        cp = app.engine.compile(snippet)

        for y in range(wr_info.window_height):
            line_number = visible_line_to_input_line.get(y)

            if line_number is not None:
                if cp is not None and line_number + 1 == cp:
                    result.append((token_error,
                                   ('%i ' % (line_number + 1)).rjust(width)))
                else:
                    result.append((token,
                                   ('%i ' % (line_number + 1)).rjust(width)))

            result.append((style.Token, '\n'))

        return result


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


def text_window_bar(name=None, key_binding_manager=None):
    def get_tokens(cli):
        text_style = style.Bar.Text
        display_text, read_only = buffers.buffer_display(cli.application, name)
        if not read_only and cli.current_buffer_name == name:
            vi_mode = key_binding_manager.get_vi_state(cli).input_mode
            if vi_mode == vi_state.InputMode.INSERT:
                text_style = style.Bar.Hl_Text
            tokens = [(text_style, display_text),
                      (text_style, u' \u2022 ')]
            if vi_mode == vi_state.InputMode.INSERT:
                tokens.append((text_style, 'INSERT'))
            elif vi_mode == vi_state.InputMode.NAVIGATION:
                tokens.append((text_style, 'NORMAL'))
            else:
                tokens.append((text_style, '[     ]'))
            return tokens
        else:
            return [(text_style, display_text)]
    return toolbars.TokenListToolbar(
        get_tokens, default_char=screen.Char(' ', style.Bar.Text))


def normal_text_window(name=None, lang=None, lineno=False,
                       leading_space=False, trailing_space=False,
                       width=None, height=None):
    if name is None:
        name = buffers.DEFAULT_BUFFER
    bf_attrs = {'buffer_name': name,
                'lexer': style.get_lexer_by_lang(lang),
                'highlighters': [highlighters.SelectionHighlighter()]}

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
        left_margins.append(NumberredMargin(name))
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


def text_window_with_bar(name=None, lang=None, lineno=False,
                         leading_space=False, trailing_space=False,
                         width=None, height=None, key_binding_manager=None):
    if name is None:
        name = buffers.DEFAULT_BUFFER
    return window_rows([
        normal_text_window(
            name=name, lang=lang, lineno=lineno,
            leading_space=leading_space, trailing_space=trailing_space,
            width=width, height=height),
        text_window_bar(name=name, key_binding_manager=key_binding_manager),
    ])
