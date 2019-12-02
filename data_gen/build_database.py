import os
import random
import sqlite3
import string
from datetime import datetime as time
from data_gen import make_person_name, make_date, make_paper_name, make_address, force_unique, make_phone_number


def timeCall(method, *args) -> int:
    ts = time.now().microsecond
    method(*args)
    te = time.now().microsecond

    return abs(te - ts)


@force_unique
def randomString():
    stringLength = 60
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class Event:
    def __init__(self):
        self.date = make_date()
        self.title = randomString()
        self.phone_number = make_phone_number()


class Venue:
    def __init__(self):
        self.address = make_address()
        self.name = randomString()
        self.seats = random.randint(1, 1000)


class Person:
    def __init__(self):
        self.name = make_person_name()
        self.title = randomString()
        self.email = randomString()
        self.degree = randomString()


class Paper:
    def __init__(self):
        self.abstract = randomString()
        self.title = make_paper_name()
        self.pub_date = make_date()


event_table = '''create table Event(date text, title text primary key, phone_number text)'''
venue_table = '''create table Venue(address text, name text primary key, seats integer)'''
person_table = '''create table Person(name text primary key, degree text, title text, email text)'''
paper_table = '''create table Paper(abstract text, pub_date text, title text primary key)'''
hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as = """create table 
hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as""" + """(event text not null, venue text not null,chair text not null, paper text not null, author text not null, reviewed_by text not null,FOREIGN KEY (event) REFERENCES Event(title), 
FOREIGN KEY (chair) REFERENCES Person(name),  
FOREIGN KEY (paper) REFERENCES Paper(title), FOREIGN KEY (reviewed_by) REFERENCES Person(name),FOREIGN KEY (event) REFERENCES Event(title), 
FOREIGN KEY (venue) REFERENCES Venue(name), FOREIGN KEY (chair) REFERENCES Person(name), primary key(event,paper,author,reviewed_by));"""

entities = [event_table, venue_table, person_table, paper_table]


def build_entities(c):
    for entity in entities:
        c.execute(entity)


def insert_paper(paper, cursor):
    cursor.execute(f"insert into Paper values('{paper.abstract}', '{paper.pub_date}', '{paper.title}')")


def insert_venue(venue, cursor):
    cursor.execute(f"insert into Venue values('{venue.address}', '{venue.name}', {venue.seats})")


def insert_person(person, cursor):
    cursor.execute(f"insert into Person values('{person.name}','{person.degree}','{person.title}','{person.email}' )")


def insert_event(event, cursor):
    cursor.execute(f"insert into Event values('{event.date}','{event.title}','{event.phone_number}')")


def select_query(query, cursor):
    cursor.execute(query)
    return cursor.fetchall()


def average_time(function, *args):
    return sum([timeCall(function, *args) for _ in range(1000)]) / 1000


def add_row(relationship_row, c):
    paper = Paper()
    insert_paper(paper, c)
    event = Event()
    insert_event(event, c)
    venue = Venue()
    insert_venue(venue, c)
    author = Person()
    insert_person(author, c)
    reviewer = Person()
    insert_person(reviewer, c)
    chair = Person()
    insert_person(chair, c)
    relationship_row(paper, reviewer, author, chair, venue, event)


query1_1 = """select abstract from Paper inner join hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as on Paper.title=hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as.paper inner join Venue on Venue.name=hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as.venue where (instr(chair,'a')>0 and instr(Venue.address, '100')>0);"""
query1_2 = """select abstract from Paper inner join the_peer_review_process on Paper.title=the_peer_review_process.paper natural join hosted_at_where_and_by_whom inner join Venue on Venue.name=hosted_at_where_and_by_whom.venue where(instr(chair,'a')>0 and instr(Venue.address, '100')>0);"""
query1_3 = """select abstract from Paper inner join the_peer_review_process on Paper.title=the_peer_review_process.paper inner join hosted_at_where on the_peer_review_process.event = hosted_at_where.event inner join and_by_whom on and_by_whom.event = the_peer_review_process.event inner join Venue on Venue.name=hosted_at_where.venue where(instr(chair,'a')>0 and instr(Venue.address, '100')>0);"""
query2_1 = """select abstract from Paper inner join hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as on Paper.title=hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as.paper inner join Venue on Venue.name=hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as.venue inner join Person on chair = person.name where (instr(chair,'1')>0 and instr(Venue.address, '100')>0);"""
query2_2 = """select abstract from Paper inner join the_peer_review_process on Paper.title=the_peer_review_process.paper inner join hosted_at_where_and_by_whom inner join Venue on Venue.name=hosted_at_where_and_by_whom.venue inner join Person on chair = person.name where (instr(chair,'1')>0 and instr(Venue.address, '100')>0);"""
query2_3 = """select abstract from Paper inner join the_peer_review_process on Paper.title=the_peer_review_process.paper inner join hosted_at_where on the_peer_review_process.event = hosted_at_where.event inner join and_by_whom on and_by_whom.event = the_peer_review_process.event inner join Venue on Venue.name=hosted_at_where.venue inner join Person on chair = person.name where (instr(chair,'1')>0 and instr(Venue.address, '100')>0);"""
query3_1 = """select email from Person inner join hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as on Person.name = hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as.chair inner join Venue on hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as.venue = Venue.name where (instr(Venue.address, 'Boulevard')>0);"""
query3_2 = """select email from Person inner join hosted_at_where_and_by_whom on Person.name = hosted_at_where_and_by_whom.chair inner join Venue on hosted_at_where_and_by_whom.venue = Venue.name where (instr(Venue.address, 'Boulevard')>0);"""
query3_3 = """select email from Person inner join and_by_whom on Person.name = and_by_whom.chair inner join hosted_at_where on and_by_whom.event=hosted_at_where.event inner join Venue on hosted_at_where.venue = Venue.name where (instr(Venue.address, 'Boulevard')>0);"""


def main():
    try:
        os.remove("d1.db")
        os.remove("d2.db")
        os.remove("d3.db")
    except OSError:
        pass


    conn = sqlite3.connect("d1.db")

    c = conn.cursor()
    build_entities(c)
    c.execute(hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as)

    def insert_entity(paper, reviewer, author, chair, venue, event):
        c.execute(
            f"insert into hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as values('{event.title}', '{venue.name}', '{chair.name}', '{paper.title}', '{author.name}', '{reviewer.name}' )")

    for i in range(1000):
        add_row(insert_entity, c)
    conn.commit()
    with open(file="Transformation_scripts") as tscripts:
        for line in tscripts:
            c.execute(line)
        conn.commit()

    conn2 = sqlite3.connect("d2.db")
    conn3 = sqlite3.connect("d3.db")
    print(average_time(select_query, query1_1, c))
    print(average_time(select_query, query1_2, conn2.cursor()))
    print(average_time(select_query, query1_3, conn3.cursor()))
    print("")
    print(average_time(select_query, query2_1, c))
    print(average_time(select_query, query2_2, conn2.cursor()))
    print(average_time(select_query, query2_3, conn3.cursor()))
    print("")
    print(average_time(select_query, query3_1, c))
    print(average_time(select_query, query3_2, conn2.cursor()))
    print(average_time(select_query, query3_3, conn3.cursor()))


main()

