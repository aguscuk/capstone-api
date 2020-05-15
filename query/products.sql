SELECT P.Id ProductId,
       P.ProductName,
       P.QuantityPerUnit,
       P.UnitPrice,
       P.UnitsInStock,
       P.ReorderLevel,
       P.Discontinued,
       S.CompanyName SupplierName,
       S.ContactName,
       S.Address,
       S.City,
       S.Region,
       S.Phone,
       S.Fax
  FROM Product P
       LEFT JOIN
       Supplier S ON P.SupplierId = S.Id
       LEFT JOIN
       Category C ON P.CategoryId = C.Id;
