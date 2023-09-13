create table public.test (
	id serial primary key,
	name varchar(20) not null,
	address varchar(100) not null,
	zipcode char(5),
	introduction text
);
