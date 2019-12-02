CREATE TABLE Event(date text, title text primary key, phone_number text)
CREATE TABLE Paper (abstract text, pub_date text, title text primary key)
CREATE TABLE Person(name text primary key, degree text, title text, email text)
CREATE TABLE Venue(address text, name text primary key, seats integer)
CREATE TABLE and_by_whom(event text primary key, chair text, FOREIGN KEY (event) REFERENCES Event(title),FOREIGN KEY (chair) REFERENCES Person(name))
CREATE TABLE hosted_at_where(event text primary key, venue text,FOREIGN KEY (event) REFERENCES Event(title), FOREIGN KEY (venue) REFERENCES Venue(name))
CREATE TABLE the_peer_review_process(event text, paper text, author text, reviewed_by text,  FOREIGN KEY (event) REFERENCES Event(title), FOREIGN KEY (author) REFERENCES Person(name),  FOREIGN KEY (paper) REFERENCES Paper(title), FOREIGN KEY (reviewed_by) REFERENCES Person(name), PRIMARY Key (event, paper, author, reviewed_by))

