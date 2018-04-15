Where Shall We Have Lunch

## Table Schema

> CREATE TABLE lunches (id integer primary key, lunch text, lastdate date, distance float);

> CREATE TABLE history (lunchid, timestamp date, foreign key(lunchid) references lunch(id));

> CREATE TABLE people (id integer primary key, name string);

> CREATE TABLE ratings (lunchid int, personid int, rating float, foreign key(lunchid) references lunch(id), foreign key(personid) references person(id));

