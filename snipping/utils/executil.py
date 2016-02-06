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


def execwrap(content):
    def _inner():
        six.exec_(compile(content, '<stdin>', 'exec'), locals(), locals())
        return locals()

    exec_locals = {}
    try:
        with reopen_stdout_stderr() as output:
            exec_locals = _inner()
    except SyntaxError:
        output = "SyntaxError"
    except Exception:
        output = "%s%s" % (output.getvalue(), _exception())
    else:
        output = output.getvalue()

    output = strutil.ensure_text(output)

    exec_locals_text = []
    if '__builtins__' in exec_locals:
        exec_locals.pop('__builtins__')
        exec_locals_text = [u"__builtins__: ..."]
    if 'content' in exec_locals:
        exec_locals.pop('content')
    for k, v in exec_locals.items():
        if isinstance(v, six.string_types):
            v = strutil.ensure_text(v)
        kvs = u"%s: %s" % (k, v)
        exec_locals_text.append(kvs)
    locals_text = '\n'.join(exec_locals_text)
    return output, locals_text
