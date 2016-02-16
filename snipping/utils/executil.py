import contextlib
import sys
import six
import traceback

from snipping.utils import strutil

_OUTPUT_STREAM = None


def _init_output_stream():
    global _OUTPUT_STREAM
    if _OUTPUT_STREAM is None:
        _OUTPUT_STREAM = six.moves.cStringIO()
    else:
        _OUTPUT_STREAM.truncate(0)
        _OUTPUT_STREAM.seek(0)
    return _OUTPUT_STREAM


@contextlib.contextmanager
def reopen_stdout_stderr():
    old_stdout, old_stderr = sys.stdout, sys.stderr
    _init_output_stream()
    sys.stderr = sys.stdout = _OUTPUT_STREAM
    yield _OUTPUT_STREAM
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
        global_env = exec_globals()
        local_env = global_env
        six.exec_(compile(content, '<stdin>', 'exec'), global_env, local_env)
        return global_env

    globals_ = {}
    output_handler = None
    try:
        with reopen_stdout_stderr() as output_handler:
            globals_ = _inner()
    except SyntaxError:
        output = "SyntaxError"
    except Exception:
        if output_handler is not None:
            output = "%s%s" % (output_handler.getvalue(), _exception())
        else:
            output = _exception()
    else:
        output = output_handler.getvalue()

    output = strutil.ensure_text(output)

    globals_texts = []
    for k, v in globals_.items():
        if k in _inner_name:
            continue
        if isinstance(v, six.string_types):
            v = strutil.ensure_text(v)
        kvs = u"%s: %s" % (k, v)
        globals_texts.append(kvs)
    globals_text = '\n'.join(globals_texts)
    return output, globals_text
