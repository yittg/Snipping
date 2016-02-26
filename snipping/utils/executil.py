import contextlib
import sys
import six
import traceback

from snipping.utils import fileutil
from snipping.utils import strutil


@contextlib.contextmanager
def reopen_stdout_stderr():
    f = fileutil.temp_file()

    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stderr = sys.stdout = f
    try:
        yield f
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr


def _exception(top_frame):
    t, v, tb = sys.exc_info()
    tbs = traceback.extract_tb(tb)

    for seq, tb_tuple in enumerate(tbs):
        if tb_tuple[0] == top_frame:
            tbs = tbs[seq:]
            break

    outputs = traceback.format_list(tbs)
    if outputs:
        outputs.insert(0, u"Traceback (most recent call last):\n")
    outputs.extend(traceback.format_exception_only(t, v))
    return ''.join(outputs)


def exec_globals():
    return {
        '__builtins__': six.moves.builtins,
        '__doc__': None,
        '__name__': '__main__',
        '__package__': None,
    }


def exec_locals():
    return {}


def compile_text(content, from_file=None):
    return compile(content, from_file or '<stdin>', 'exec')


def execwrap(content, from_file=None):
    from_file = from_file or '<stdin>'
    if isinstance(content, six.string_types):
        content = compile_text(content, from_file=from_file)

    def _inner():
        global_env = exec_globals()
        local_env = global_env
        six.exec_(content, global_env, local_env)
        return global_env

    globals_ = {}
    output_handler = None
    try:
        with reopen_stdout_stderr() as output_handler:
            globals_ = _inner()
    except Exception:
        if output_handler is not None:
            output = "%s%s" % (output_handler.read(),
                               _exception(from_file))
        else:
            output = _exception(from_file)
    else:
        output = output_handler.read()

    output = strutil.ensure_text(output)

    return output, globals_
