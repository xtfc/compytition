drop table if exists users;
create table users (
	id integer primary key autoincrement,
	username text not null
);

drop table if exists status;
create table status (
	id integer primary key autoincrement,
	username text not null,
	status integer not null,
	message text not null
);
