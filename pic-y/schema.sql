drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    favfood text not null,
    firstname text not null,
    lastname text not null
);

drop table if exists food;
create table food (
    id integer primary key autoincrement,
    user text not null,
    title text not null,
    description text,
    location text,
    theme text not null,
    url text not null
);

drop table if exists theme;
create table theme (
    year integer not null,
    month integer not null,
    day integer not null,
    hour integer not null,
    minute integer not null,
    theme text not null
);

insert into food values(1, 'bob', 'title', 'desc', 'loc', 'potato', '1.jpg');
insert into theme values(2015, 1, 1, 0, 0, "mac and cheese");

