import contextlib
import sys
import six
import traceback

from snipping.utils import strutil


@contextlib.contextmanager
def reopen_stdout_stderr():
    old_stdout, old_stderr = sys.stdout, sys.stderr
    output = six.moves.cStringIO()
    sys.stderr = sys.stdout = output
    yield output
    sys.stdout, sys.stderr = old_stdout, old_stderr


def _exception():
    t, v, tb = sys.exc_info()
    tbs = traceback.extract_tb(tb)

    for seq, tb_tuple in enumerate(tbs):
        if tb_tuple[0] == '<stdin>':
            tbs = tbs[seq:]
            break

    outputs = traceback.format_list(tbs)
    if outputs:
        outputs.insert(0, u"Traceback (most recent call last):\n")
    outputs.extend(traceback.format_exception_only(t, v))
    return ''.join(outputs)


_inner_name = ['__name__', '__doc__', '__package__', '__builtins__']


def exec_globals():
    return {
        '__builtins__': six.moves.builtins,
        '__doc__': None,
        '__name__': '__main__',
        '__package__': None,
    }


def exec_locals():
    return {}


def execwrap(content):
    def _inner():
        globals_ = exec_globals()
        locals_ = globals_
        six.exec_(compile(content, '<stdin>', 'exec'), globals_, locals_)
        return locals_

    locals_ = {}
    try:
        with reopen_stdout_stderr() as output:
            locals_ = _inner()
    except SyntaxError:
        output = "SyntaxError"
    except Exception:
        output = "%s%s" % (output.getvalue(), _exception())
    else:
        output = output.getvalue()

    output = strutil.ensure_text(output)

    exec_locals_text = []
    for k, v in locals_.items():
        if k in _inner_name:
            continue
        if isinstance(v, six.string_types):
            v = strutil.ensure_text(v)
        kvs = u"%s: %s" % (k, v)
        exec_locals_text.append(kvs)
    locals_text = '\n'.join(exec_locals_text)
    return output, locals_text
