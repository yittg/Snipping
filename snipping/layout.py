"""layout"""

from snipping import key_bindings
from snipping.prompt_toolkit import layout
from snipping.prompt_toolkit import style

MAIN_WINDOW_SIZE = 100
SUB_WINDOW_SIZE = 40


def title_tokens(_):
    return [(style.Title, 'Snipping')]


def footer_tokens(_):
    tokens = []
    for token in key_bindings.REGISTER_KEYS:
        tokens.append((style.Key, "[%s]" % token[0]))
        tokens.append((style.Token, " %s " % token[1]))
    return tokens


def create_layout(contents, key_binding_manager=None):
    result_windows = []
    for content in contents:
        result_windows.append(layout.text_window_with_bar(
            name=content, width=layout.dim(SUB_WINDOW_SIZE),
            key_binding_manager=key_binding_manager))
    result_layout = layout.window_rows(result_windows)
    editor_window = layout.text_window_with_bar(
        lineno=True, trailing_space=True, width=layout.dim(MAIN_WINDOW_SIZE),
        key_binding_manager=key_binding_manager)
    main_layout = layout.window_columns([
        editor_window, layout.vertical_line(), result_layout
    ])
    screen = layout.window_rows([
        layout.horizontal_tokenlist_window(title_tokens, align='center'),
        layout.horizontal_line(),
        main_layout,
        layout.horizontal_tokenlist_window(footer_tokens, align='right'),
    ])
    return screen
