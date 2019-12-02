CREATE TABLE Event(date text, title text primary key, phone_number text)
CREATE TABLE Paper(abstract text, pub_date text, title text primary key)
CREATE TABLE Person(name text primary key, degree text, title text, email text)
CREATE TABLE Venue(address text, name text primary key, seats integer)
CREATE TABLE hosted_at_and_where_by_whom_with_peer_reviewed_by_and_as(event text not null, venue text not null,chair text not null, paper text not null, author text not null, reviewed_by text not null,FOREIGN KEY (event) REFERENCES Event(title), 
FOREIGN KEY (chair) REFERENCES Person(name),  
FOREIGN KEY (paper) REFERENCES Paper(title), FOREIGN KEY (reviewed_by) REFERENCES Person(name),FOREIGN KEY (event) REFERENCES Event(title), 
FOREIGN KEY (venue) REFERENCES Venue(name), FOREIGN KEY (chair) REFERENCES Person(name), primary key(event,paper,author,reviewed_by))

