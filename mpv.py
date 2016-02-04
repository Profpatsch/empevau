import json
import subprocess as sub
import socket as s
import os
import tempfile
import time

class MPV:
    _socket = None
    _player = None

    def __init__(self):
        (fd, fn) = tempfile.mkstemp()
        os.close(fd)
        self._player = sub.Popen([
            "mpv",
            "--input-unix-socket=" + fn,
            "--keep-open=yes",
            "--idle=yes",
            "--no-video"
        ], stdin=sub.DEVNULL, stdout=sub.DEVNULL, stderr=sub.DEVNULL)
        # otherwise the socket is not yet open
        time.sleep(1)
        so = s.socket(s.AF_UNIX)
        so.connect(fn)
        self._socket = so

    def play(self, uri):
        self.command('loadfile', uri)

    def command(self, name, *args):
        j = json.dumps(
            { "command":
              [name]+list(args) }
        )
        f = self._socket.makefile('rw')
        f.write(j)
        # print(f.read())

    def __del__(self):
        self._player.terminate()
        self._socket.shutdown()
        self._socket.close()
