CREATE TABLE public.test (
	id SERIAL PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	address VARCHAR(100) NOT NULL,
	zipcode CHAR(5),
	introduction TEXT
);
