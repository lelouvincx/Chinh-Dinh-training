-- Creates a nonclustered index on the LastName column of the Red30Tech Customers table.

USE Red30Tech;
GO

CREATE NONCLUSTERED INDEX IX_Customers_LastName
ON dbo.Customers (LastName ASC);
