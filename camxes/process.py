from pkg_resources import resource_filename
from subprocess import Popen, PIPE


_jarfile = resource_filename(__name__, 'camxes.jar')
_process_pool = {}


def _aquire(arg):
    if arg not in _process_pool or \
       _process_pool[arg].poll() is not None:

        _process_pool[arg] = Popen(['java', '-jar', _jarfile, arg],
                                   stdout=PIPE, stdin=PIPE)
        for _ in arg[1:]:
            _process_pool[arg].stdout.readline()

    return _process_pool[arg]


def camxes(arg, input):
    proc = _aquire(arg)
    proc.stdin.write(input.encode('utf-8'))
    proc.stdin.write(b'\n')
    proc.stdin.flush()
    output = proc.stdout.readline()
    if 'M' in arg:
        proc.stdout.readline()
        output = output.partition(b'Morphology pass: ')[2]
    return output.decode('utf-8').rstrip('\n')
