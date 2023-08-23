SELECT * FROM Customers;
SELECT * FROM Orders;
SELECT * FROM Products;

SELECT Customers.FirstName,
		Customers.LastName,
		Orders.OrderDate,
		Orders.Quantity,
		Products.Name,
		Products.RetailPrice
FROM Customers INNER JOIN Orders
	ON Customers.CustomerID = Orders.CustomerID
	INNER JOIN Products
	ON Orders.ProductID = Products.ProductID
;
