import ast
import os
import sys
import tokenize


__version__ = '0.0.2'

EXACT_PIN_ERROR_CODE = 'P001'
EXACT_PIN_ERROR_MESSAGE = 'exact pin found in install_requires'


class ExactPinChecker(object):
    name = 'flake8-exact-pin'
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        self.tree = tree
        self.filename = (filename == 'stdin' and sys.stdin) or filename

    def run(self):
        if self.filename == sys.stdin:
            noqa = get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as file_to_check:
                noqa = get_noqa_lines(file_to_check.readlines())

        if os.path.basename(self.filename) == 'setup.py':
            errors = pinned_install_requires(self.tree, noqa)

            for error in errors:
                yield (
                    error.get("line"), error.get("col"), error.get("message"),
                    type(self))


def get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    noqa = [token[2][0] for token in tokens
            if token[0] == tokenize.COMMENT
            and (token[1].endswith('noqa')
            or (isinstance(token[0], str) and token[0].endswith('noqa')))]
    return noqa


def pinned_install_requires(tree, noqa):
    errors = []
    setup_node = None

    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == 'install_requires':
            try:
                node.value.elts
            except AttributeError:
                errors.append({
                    'message': 'P100 Unrecognised install_requires value',
                    'line': node.lineno,
                    'col': node.col_offset,
                })
                return errors

            for str_node in node.value.elts:
                if not isinstance(str_node, ast.Str):
                    errors.append({
                        'message': 'P101 Unrecognised install_requires item',
                        'line': str_node.lineno,
                        'col': str_node.col_offset,
                    })
                    continue

                requirement = str_node.s.split(';', 1)[0]
                if '==' in requirement:
                    errors.append({
                        'message': '{0} {1}: "{2}"'.format(
                            EXACT_PIN_ERROR_CODE, EXACT_PIN_ERROR_MESSAGE,
                            requirement),
                        'line': str_node.lineno,
                        'col': str_node.col_offset,
                    })
            break
        elif isinstance(node, ast.Call):
            try:
                if node.func.id == 'setup':
                    setup_node = node
            except:
                pass
    else:
        if setup_node:
            errors.append({
                'message': 'P103 Missing install_requires in setup(..)',
                'line': setup_node.lineno,
                'col': setup_node.col_offset,
            })
        else:
            errors.append({
                'message': 'P104 Missing setup()',
                'line': 0,
                'col': 0,
            })

    return errors
