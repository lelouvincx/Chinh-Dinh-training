USE WideWorldImporters;

SELECT * 
FROM Application.StateProvinces;


-- Counting Records
SELECT COUNT(*) 
FROM Application.StateProvinces;

SELECT COUNT(*) AS CountOfStates
FROM Application.StateProvinces;

SELECT COUNT(*) AS CountOfStates
FROM Application.StateProvinces
WHERE SalesTerritory = 'Southwest';

SELECT COUNT(*) AS CountOfStates
FROM Application.StateProvinces
WHERE LatestRecordedPopulation > 5000000;


-- Grouping Records
SELECT SalesTerritory, StateProvinceName
FROM Application.StateProvinces
ORDER BY SalesTerritory;

SELECT SalesTerritory, Count(StateProvinceName) AS NumberOfStates
FROM Application.StateProvinces
GROUP BY SalesTerritory
ORDER BY SalesTerritory;


-- Maximum, Minimum, and Average
SELECT MAX(*) 
FROM Application.StateProvinces;

SELECT MAX(LatestRecordedPopulation) AS MaxPopulation,
	MIN(LatestRecordedPopulation) AS MinPopulation,
	AVG(LatestRecordedPopulation) AS AvgPopulation
FROM Application.StateProvinces;


-- Subquery
SELECT StateProvinceName, LatestRecordedPopulation
FROM Application.StateProvinces
WHERE LatestRecordedPopulation =
	(SELECT MAX(LatestRecordedPopulation) FROM Application.StateProvinces)
;

SELECT StateProvinceName, LatestRecordedPopulation
FROM Application.StateProvinces
WHERE LatestRecordedPopulation >
	(SELECT AVG(LatestRecordedPopulation) FROM Application.StateProvinces)
;