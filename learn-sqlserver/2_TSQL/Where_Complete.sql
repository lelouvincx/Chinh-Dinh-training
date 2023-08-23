SELECT CustomerID, FirstName, LastName, Address, City, State 
FROM dbo.Customers
WHERE State = 'CA' OR State = 'NY'
;