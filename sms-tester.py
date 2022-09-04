
from argparse import ArgumentParser
import os
import sys

from pytils.log import setup_logging, teardown, user_log

from src.core import load, send_assignment, send_sms


@teardown
def main(argv):
    ap = ArgumentParser(prog="sms-tester")
    ap.add_argument("-v", "--verbose", default=False, action="store_true")
    ap.add_argument("--dry-run", action="store_true", default=False)
    ap.add_argument("textbelt_key")
    ap.add_argument("santas_config")
    aargs = ap.parse_args(argv)
    log_file = ".%s.log" % (os.path.splitext(os.path.basename(__file__))[0])
    setup_logging(log_file, aargs.verbose, False, True, True)

    santas = load(aargs.santas_config)
    user_log.info("The Santas are: %s" % santas)

    for santa in santas:
        send_sms(aargs.textbelt_key, aargs.dry_run, santa.number, "This is a test.  Please whatsapp Jeej to confirm its receipt.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

