SELECT O.Id OrderId,
       O.OrderDate,
       O.RequiredDate,
       O.ShippedDate,
       O.ShipRegion,
       O.ShipCountry,
       Od.UnitPrice,
       Od.Quantity,
       Od.Discount,
       P.ProductName,
       ROUND(Od.UnitPrice * Od.Quantity, 2) AS SubTotal,
       (Od.UnitPrice * Od.Quantity * Od.Discount) AS DiscPrice,
       (Od.UnitPrice * Od.Quantity) - (Od.UnitPrice * Od.Quantity * Od.Discount) AS Total,
       Cu.CompanyName AccountName,
       Cu.ContactName,
       Cu.ContactTitle,
       Cu.Address,
       Cu.City,
       Cu.Region,
       Cu.PostalCode,
       Cu.Country,
       Cu.Phone,
       Cu.Fax,
       Ca.CategoryName,
       Ca.Description
  FROM [Order] O
       LEFT JOIN
       OrderDetail Od ON O.Id = Od.OrderId
       LEFT JOIN
       Product P ON Od.ProductId = P.Id
       LEFT JOIN
       Customer Cu ON O.CustomerId = Cu.Id
       LEFT JOIN
       Category Ca ON P.CategoryId = Ca.Id
 LIMIT 10;
