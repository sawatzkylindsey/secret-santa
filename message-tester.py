
from argparse import ArgumentParser
import logging
import os
import sys

from pytils.log import setup_logging, teardown, user_log

from src.core import send_assignment, Santa


@teardown
def main(argv):
    ap = ArgumentParser(prog="message-tester")
    ap.add_argument("-v", "--verbose", default=False, action="store_true")
    ap.add_argument("--dry-run", action="store_true", default=False)
    ap.add_argument("textbelt_key")
    ap.add_argument("number")
    aargs = ap.parse_args(argv)
    log_file = ".%s.log" % (os.path.splitext(os.path.basename(__file__))[0])
    setup_logging(log_file, aargs.verbose, False, True, True)

    send_assignment(aargs.textbelt_key, aargs.dry_run, [Santa("abc", aargs.number), Santa("def", aargs.number)], [1, 0])

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

