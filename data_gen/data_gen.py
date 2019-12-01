# Author: Jeremy Gluck
""" 
Script to generate lorum ipsum for a database
with entities: event, venue, chairs, reviewers, authors, papers
the entities have attributes:
 paper names, people names, dates, phone numbers, addresses, event names 
"""
from random import choice, randint

# Functions output strings for storage in csv files

def make_phone_number() -> str: 
    rand_dig = lambda: str(randint(0,9))
    area_code = rand_dig() + rand_dig() + rand_dig()
    first_three = rand_dig() + rand_dig() + rand_dig()
    last_four = rand_dig() + rand_dig() + rand_dig() + rand_dig()
    return "(" + area_code + ")" + first_three + "-"  + last_four


# 00 Month 20XX Format
def make_date() -> str:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "October", "November", "December"]
    day = lambda: str(randint(1,28))
    month = lambda: choice(months)
    year = lambda: str(randint(2020,2099))
    return day() + " " + month() + " " + year()


# name list credit: https://github.com/dominictarr/random-name/edit/master/first-names.txt
# I factored the name_list out globally to hopefully prevent it from reloading after every function call
# the interpreter handles lazily evaluating the load when the function is first called (I think)
name_list = []
with open("names.rawtext", 'r') as names:
    name_list = [name.rstrip() for name in list(names)]
def make_person_name() -> str:
    return choice(name_list) + ' ' + choice(name_list)


subjects = ['Biology', 'Chemistry', 'Physics', 'Computer Science', 'Psychology', 'AI', 'Robotics', 'Memes', 'Mechatronics', 'Game Theory', 'Math', 'Category Theory', 'Genetics', 'Botany', 'Cloning', 'Machine Learning', 'Biometrics']
def make_paper_name() -> str:
    return choice(subjects) + " study utilizing " + choice(subjects)

address_postfixes = ["Street", "Avenue", "Boulevard", "Court", "Circle"]
def make_address() -> str:
    house_number = lambda: str(randint(1,9999))
    street_number = lambda: str(randint(1, 100))
    return house_number() + " " + street_number() + "th " + choice(address_postfixes)
