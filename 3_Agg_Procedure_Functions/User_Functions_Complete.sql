USE WideWorldImporters;

-- create a custom function to convert degrees celsius into degrees fahrenheit
CREATE FUNCTION Warehouse.ToFahrenheit (@Celsius decimal(10,2))
RETURNS decimal(10,2)
AS
BEGIN
	DECLARE @Fahrenheit decimal(10,2);
	SET @Fahrenheit = (@Celsius * 1.8 + 32);
	RETURN @Fahrenheit
END;

-- use the custom function in a select statement
SELECT TOP 100 VehicleTemperatureID,
	Temperature AS Celsius,
	Warehouse.ToFahrenheit(Temperature) AS Fahrenheit
FROM Warehouse.VehicleTemperatures;