drop table if exists users;
create table users (
    # MICHAEL FILL THIS OUT
);

drop table if exists food;
create table food (
	id integer primary key autoincrement,
	title text not null,
	description text,
	theme text not null
)
