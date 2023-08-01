-- switch to the WideWorldImporters database
USE WideWorldImporters;
GO

-- create procedure with parameter
CREATE PROCEDURE Warehouse.uspSelectProductsByColor
    @paramColor char(20)
AS
SELECT	Warehouse.StockItems.StockItemID,
		Warehouse.StockItems.StockItemName,
		Warehouse.StockItemHoldings.QuantityOnHand,
		Warehouse.StockItems.RecommendedRetailPrice,
		Warehouse.Colors.ColorName
FROM	Warehouse.Colors INNER JOIN
		Warehouse.StockItems ON Warehouse.Colors.ColorID = Warehouse.StockItems.ColorID INNER JOIN
		Warehouse.StockItemHoldings ON Warehouse.StockItems.StockItemID = Warehouse.StockItemHoldings.StockItemID
WHERE ColorName = @paramColor
;
GO

-- execute the stored procedure with various parameters
EXEC Warehouse.uspSelectProductsByColor 'Black';
GO
EXEC Warehouse.uspSelectProductsByColor 'Blue';
GO
EXEC Warehouse.uspSelectProductsByColor;
GO

-- alter the procedure to include a default value and error handling
ALTER PROCEDURE Warehouse.uspSelectProductsByColor
    @paramColor char(20) = NULL
AS
IF @paramColor IS NULL
BEGIN
   PRINT 'A valid product color is required.'
   RETURN
END
SELECT  Warehouse.StockItems.StockItemID,
        Warehouse.StockItems.StockItemName,
        Warehouse.StockItemHoldings.QuantityOnHand,
        Warehouse.StockItems.RecommendedRetailPrice,
        Warehouse.Colors.ColorName
FROM    Warehouse.Colors INNER JOIN
        Warehouse.StockItems ON Warehouse.Colors.ColorID = Warehouse.StockItems.ColorID INNER JOIN
        Warehouse.StockItemHoldings ON Warehouse.StockItems.StockItemID = Warehouse.StockItemHoldings.StockItemID
WHERE ColorName = @paramColor
;
GO

EXEC Warehouse.uspSelectProductsByColor;
GO
EXEC Warehouse.uspSelectProductsByColor 'Red';
GO

-- clean up the WideWorldImporters database
DROP PROCEDURE Warehouse.uspSelectProductsByColor;
GO