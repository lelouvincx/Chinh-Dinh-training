-- switch to the WideWorldImporters database
USE WideWorldImporters;
GO

-- view all stored procedures in curent database
SELECT SCHEMA_NAME(schema_id) AS SchemaName,
    name AS ProcedureName
FROM sys.procedures
ORDER BY SchemaName
;
GO

-- create a stored procedure to identify inventory
CREATE PROCEDURE Warehouse.uspLowInventory
AS
SELECT	Warehouse.StockItems.StockItemID AS ID,
		Warehouse.StockItems.StockItemName AS 'Item Name',
		Warehouse.StockItemHoldings.QuantityOnHand AS 'On Hand',
		Warehouse.StockItemHoldings.ReorderLevel AS 'Reorder Level'
FROM	Warehouse.StockItems INNER JOIN
		Warehouse.StockItemHoldings ON Warehouse.StockItems.StockItemID = Warehouse.StockItemHoldings.StockItemID
ORDER BY 'On Hand';
GO

-- execute the stored procedure
EXECUTE Warehouse.uspLowInventory

-- alter the procedure to locate low inventory
ALTER PROCEDURE Warehouse.uspLowInventory
AS
SELECT	Warehouse.StockItems.StockItemID AS ID,
		Warehouse.StockItems.StockItemName AS 'Item Name',
		Warehouse.StockItemHoldings.QuantityOnHand AS 'On Hand',
		Warehouse.StockItemHoldings.ReorderLevel AS 'Reorder Level'
FROM	Warehouse.StockItems INNER JOIN
		Warehouse.StockItemHoldings ON Warehouse.StockItems.StockItemID = Warehouse.StockItemHoldings.StockItemID
WHERE	ReorderLevel > QuantityOnHand
ORDER BY 'On Hand';
GO

-- execute the stored procedure
EXECUTE Warehouse.uspLowInventory

-- clean up the WideWorldImporters database
DROP PROCEDURE Warehouse.uspLowInventory;
GO