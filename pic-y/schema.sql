drop table if exists entries;
create table users (
    id integer primary key autoincrement,
    url text not null,
    title text not null,
    text text not null
);
