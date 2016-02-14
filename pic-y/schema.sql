drop table if exists users;
create table users (
    user text
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

insert into food values(1, 'bob', 'title', 'desc', 'loc', 'potato', '1.jpg');

