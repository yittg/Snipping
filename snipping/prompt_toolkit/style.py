"""snipping.prompt_toolkit.style

wrappers for style
"""

from prompt_toolkit import styles
from prompt_toolkit.layout import lexers

from pygments import lexers as pygments_lexers

Token = styles.Token
Line = Token.Line
Title = Token.Title
Bar = Token.Bar
Key = Token.Key
ErrorLineNo = Token.ErrorLineNo

style_dict = {
    Line:   "#ffffff bg:#666666",
    Title:  "#ffff00",
    Bar.Text: "#111111 bg:#666666",
    Bar.Hl_Text: "#ffffff bg:#666666",
    Key: "#ffffff bg:#222222",
    ErrorLineNo: "#ff0000",
}

default_style = styles.PygmentsStyle.from_defaults(style_dict)


def get_lexer_by_lang(lang=None):
    cls = pygments_lexers.find_lexer_class(lang or 'Python')
    return lexers.PygmentsLexer(cls)
