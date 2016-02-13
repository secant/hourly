drop table if exists users;
create table users (
    user text
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