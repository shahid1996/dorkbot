from __future__ import print_function
import sys
import os
import tempfile
import subprocess
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def run(args):
    required = ["domain"]
    for r in required:
        if r not in args:
            print ("ERROR: %s must be set" % r, file=sys.stderr)
            sys.exit(1)

    dorkbot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    default_cc_py_path = os.path.join(dorkbot_dir, "tools", "cc.py")
    if not os.path.isdir(default_cc_py_path): default_cc_py_path = ""

    if "cc_py_dir" in args:
        cc_py_path = os.path.abspath(args["cc_py_dir"])
    else:
        cc_py_path = default_cc_py_path
    domain = args["domain"]
    year = args.get("year", "")

    filename = os.path.relpath(os.path.join(tempfile.gettempdir(), domain + ".txt"))

    index_cmd = [os.path.join(cc_py_path, "cc.py")]
    if year: index_cmd += ["-y", year]
    index_cmd += ["-o", filename]
    index_cmd += [domain]

    try:
        subprocess.check_call(index_cmd)
    except OSError as e:
        if "No such file or directory" in e:
            print("Could not execute cc.py. If not in PATH, then download and unpack as /path/to/dorkbot/tools/cc.py/ or set cc_py_dir option to correct directory.", file=sys.stderr)
            sys.exit(1)
        elif "Permission denied" in e:
            print("Could not execute cc.py. Make sure it is executable, e.g.: chmod +x tools/cc.py/cc.py", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError:
        return False

    results = []
    with open(filename, "r") as output:
        for result in output: results.append(urlparse(result.strip().encode("utf-8")))
    os.remove(filename)

    return results

