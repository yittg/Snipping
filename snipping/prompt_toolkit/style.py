"""snipping.prompt_toolkit.style

wrappers for style
"""

from prompt_toolkit import styles
from prompt_toolkit.layout import lexers

from pygments import lexers as pygments_lexers


Line = styles.Token.Line
Title = styles.Token.Title

style_dict = {
    Line:   "#ffffff bg:#666666",
    Title:  "#ffff00"
}

default_style = styles.PygmentsStyle.from_defaults(style_dict)


def get_lexer_by_lang(lang=None):
    cls = pygments_lexers.find_lexer_class(lang or 'Python')
    return lexers.PygmentsLexer(cls)


def title_tokens(content):

    def get_tokens(_):
        return [(Title, content)]

    return get_tokens
