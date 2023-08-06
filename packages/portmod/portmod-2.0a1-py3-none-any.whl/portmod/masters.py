# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import shutil
import subprocess
import shlex
import re


def get_masters(file):
    """
    Detects masters for the given file
    """
    _, ext = os.path.splitext(file)
    if re.match("(esp|esm|omwaddon|omwgame)", ext, re.IGNORECASE):
        omwcmd = shutil.which("omwcmd")
        process = subprocess.Popen(
            shlex.split('{} -m "{}"'.format(omwcmd, file)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (output, err) = process.communicate()
        if err:
            raise Exception(err)

        result = output.decode("utf-8", errors="ignore").rstrip("\n")
        if result:
            return set(result.split("\n"))
    return set()
