SELECT CustomerID, FirstName, LastName, Address, City, State 
FROM dbo.Customers
WHERE State = 'CA'
ORDER BY FirstName DESC, LastName
;