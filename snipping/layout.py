"""layout"""

from snipping.prompt_toolkit import layout
from snipping.prompt_toolkit import style

HEADER = 'Snipping'
FOOTER = 'Quit: ctrl-c  Save: <F4>'


def create_layout(contents):
    result_windows = []
    for content in contents:
        if result_windows:
            result_windows.append(layout.horizontal_line(40, 80))
        result_windows.append(layout.normal_text_window(
            name=content, width=layout.dim(40, 80))
        )
    result_layout = layout.window_rows(result_windows)
    editor_window = layout.normal_text_window(lineno=True,
                                              trailing_space=True)
    main_layout = layout.window_columns([
        editor_window, layout.vertical_line(), result_layout
    ])
    screen = layout.window_rows([
        layout.horizontal_tokenlist_window(style.title_tokens(HEADER),
                                           align='center'),
        layout.horizontal_line(),
        main_layout,
        layout.horizontal_tokenlist_window(style.title_tokens(FOOTER)),
    ])
    return screen
