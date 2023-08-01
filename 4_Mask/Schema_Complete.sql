USE Red30Tech;
GO

-- create a new schema in the database
CREATE SCHEMA sales;
GO


-- move an existing table into the new schema
ALTER SCHEMA sales TRANSFER dbo.Customers;
GO


-- elevate Octavia's permissions within the schema 
GRANT INSERT ON SCHEMA :: sales TO Octavia;  -- can also GRANT UPDATE or GRANT DELETE
GO