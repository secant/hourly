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
	title text not null,
	description text,
	theme text not null
)
