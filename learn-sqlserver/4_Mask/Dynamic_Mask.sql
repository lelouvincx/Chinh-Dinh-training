USE Red30Tech;
GO

-- view the data
SELECT * FROM sales.Customers;
GO

-- add data masking to the Address field
ALTER TABLE sales.Customers
ALTER COLUMN Address ADD MASKED WITH (Function = 'default()');
								-- (Function = 'email()');
								-- (Function = 'random([start range], [end range])');
								-- (Function = 'partial(prefix, [padding], suffix)');
								-- (Function = 'partial(2, "-----", 1)');

-- view the data again
SELECT * FROM sales.Customers;
GO

-- remove data masking from Address column
ALTER TABLE sales.Customers
ALTER COLUMN Address DROP MASKED;