
import logging
import os
import random
import requests


def load(config):
    santas = []

    with open(config, "r") as fh:
        for line in fh:
            line = line.strip()

            if " " in line:
                values = line.split(" ")
                santas += [Santa(*values)]

    return santas


def assign(santas):
    assignment = [i for i in range(0, len(santas))]
    random.shuffle(assignment)

    while not is_valid(santas, assignment):
        random.shuffle(assignment)

    return assignment


def is_valid(santas, assignment):
    for (i, index) in enumerate(assignment):
        gifter = santas[i]
        reciever = santas[index]
        back_reciever = santas[assignment[index]]

        # Prevent self-gifting
        if gifter == reciever:
            return False

        # Prevent 2 person cycle
        if gifter == back_reciever:
            return False

        # Enforce any exclusion groups
        if gifter.excludes(reciever):
            return False

    return True


def send_assignment(textbelt_key, dry_run, santas, assignment):
    for (i, index) in enumerate(assignment):
        gifter = santas[i]
        reciever = santas[index]

        message = \
        """🎅 HoHoHo Merry Christmas %s!
You have been selected as Secret Santa for %s.
Please make them a handmade card!
🦌🎁🎄
ps.  Don't pull a Michael Scott by getting someone an iPod!
pps. Don't reveal your assignment!
        """ % (gifter.name, reciever.name)
        send_sms(textbelt_key, dry_run, gifter.number, message)


def send_sms(textbelt_key, dry_run, number, message):
    body = {
        "phone": number,
        "key": "%s%s" % (textbelt_key, "_test" if dry_run else ""),
        "message": message,
    }
    response = requests.post("https://textbelt.com/text", body)

    if dry_run:
        logging.debug("textbelt: body: %s, response: %s" % (body, response.json()))
    else:
        logging.debug("textbelt: body: .., response: %s" % (response.json()))


class Santa:
    def __init__(self, name, number, exclusion_group=None):
        self.name = name
        self.number = number
        self.exclusion_group = exclusion_group

    def __repr__(self):
        return "(%s, %s, %s)" % (self.name, self.number, self.exclusion_group)

    def __eq__(self, other):
        # Assume same name+number, but different exclusion group, is actually the same santa.
        return self.name == other.name \
            and self.number == other.number

    def excludes(self, other):
        return self.exclusion_group is not None \
            and self.exclusion_group == other.exclusion_group

