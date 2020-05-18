import flask
from flask import request, jsonify, Response
import sqlite3
import pandas as pd

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return '''<h1>Capstone API</h1>
	<p>aguscuk capstone project api</p>'''

@app.route('/docs', methods=['GET'])
def docs():
	return '''<h1>Capstone API Documentation</h1>
	<h2>Dependencies</h2>\
	<p>- Pandas    (pip install pandas)</p>\
	<p>- flask    (pip install flask)</p>\
	<p>- gunicorn    (pip install gunicorn)</p>\
	<p>- requests    (pip install requests)</p>\
	<p>- jsonify    (pip install jsonify)</p>\
	<br>
	<h3>HOW TO</h3>
	<p><strong>1. / , method = GET</strong></p>
	<p>Base Endpoint, returning welcoming string value.</p>
	Here's : <a href="https://aguscuk-capstone-api.herokuapp.com">https://aguscuk-capstone-api.herokuapp.com</a>
	<br><br>
	<p><strong>2. /api/v1/resources/<data_name>/all , method = GET</strong></p>
	<p>Return full data <data_name> in JSON format. Currently available data are:</p>
    <p>- products : <a href="https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/products/all">https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/products/all</a> </p>
    <p>- suppliers : <a href="https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/suppliers/all">https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/suppliers/all</a> </p>
	<p>- customers : <a href="https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/customers/all">https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/customers/all</a> </p>
	<br>
	<p><strong>3. /api/v1/resources/top5_countries/dow , method = GET</strong></P>
	<p>Return top5 countries that have total omzet from orders = UnitPrice * Quantity * Discount</p>
	<p> For EDA you can read this : <a href="https://github.com/aguscuk/capstone-api/blob/master/capstone-api-markdown.ipynb">https://github.com/aguscuk/capstone-api/blob/master/capstone-api-markdown.ipynb</a>
	<p> TOP 5 Countries Omzet Total from Orders : <a href="https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/top5_countries/dow">https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/top5_countries/dow</a></p>
	<p><strong>4. /api/v1/resources/filter/<values></strong></p>
	<p>Returns full data of orders filter by :</p>
	<p>- country=<values>, exp: <i>country=France</i></p>
	<p>- orderdate_start=<values>,  exp: <i>orderdate_start=2012-01-01</i></p>
	<p>- orderdate_end=<values>, exp: <i>orderdate_end=2012-12-31</i></p>
	<p>Filter implementation: <a href="https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/filter?country=France&orderdate_start=2012-01-01&orderdate_end=2012-12-31">https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/filter?country=France&orderdate_start=2012-01-01&orderdate_end=2012-12-31</a></p>
	'''
	


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

@app.route('/api/v1/resources/suppliers/all', methods=['GET'])
def list_suppliers():
	conn = sqlite3.connect("data_input/Northwind_small.sqlite")
	suppliers = pd.read_sql_query("SELECT Id SupplierId, \
			CompanyName, \
			ContactName, \
			ContactTitle, \
			Address, \
			City, \
			Region, \
			PostalCode, \
			Country, \
			Phone, \
			Fax \
			FROM Supplier;" \
			, conn)
	json_suppliers = suppliers.to_json()

	resp = Response(response=json_suppliers,status=200,mimetype="application/json")
	return(resp)

@app.route('/api/v1/resources/customers/all', methods=['GET'])
def list_customers():
	conn = sqlite3.connect("data_input/Northwind_small.sqlite")
	customers = pd.read_sql_query("SELECT * \
			FROM Customer;" \
			, conn)
	json_customers = customers.to_json()

	resp = Response(response=json_customers,status=200,mimetype="application/json")
	return(resp)

@app.route('/api/v1/resources/products/all', methods=['GET'])
def products_all():
	conn = sqlite3.connect("data_input/Northwind_small.sqlite")
	products = pd.read_sql_query("SELECT P.Id ProductId, \
			P.ProductName, \
			P.QuantityPerUnit, \
			P.UnitPrice, \
			P.UnitsInStock, \
			P.ReorderLevel, \
			P.Discontinued, \
			S.CompanyName SupplierName, \
			S.ContactName, \
			S.Address, \
			S.City, \
			S.Region \
			FROM Product P \
			LEFT JOIN \
			Supplier S ON P.SupplierId = S.Id \
			LEFT JOIN \
			Category C ON P.CategoryId = C.Id;", \
			conn)
	json_products = products.to_json()
	resp = Response(response=json_products,status=200,mimetype="application/json")
	return(resp)

@app.route('/api/v1/resources/top5_countries/dow', methods=['GET'])
def orders_all():
	conn = sqlite3.connect("data_input/Northwind_small.sqlite")

	# query untuk Orders join table OrderDetail, Product, Customer, Category
	orders = pd.read_sql_query("SELECT O.Id OrderId, \
   O.OrderDate, \
   O.RequiredDate, \
   O.ShippedDate, \
   O.ShipRegion, \
   O.ShipCountry, \
   Od.UnitPrice, \
   Od.Quantity, \
   Od.Discount, \
   P.ProductName, \
   ROUND(Od.UnitPrice * Od.Quantity, 2) AS SubTotal, \
   (Od.UnitPrice * Od.Quantity * Od.Discount) AS DiscPrice, \
   (Od.UnitPrice * Od.Quantity) - (Od.UnitPrice * Od.Quantity * Od.Discount) AS Total, \
   Cu.CompanyName AccountName, \
   Cu.ContactName, \
   Cu.ContactTitle, \
   Cu.Address, \
   Cu.City, \
   Cu.Region, \
   Cu.PostalCode, \
   Cu.Country, \
   Cu.Phone, \
   Cu.Fax, \
   Ca.CategoryName, \
   Ca.Description \
FROM [Order] O \
   LEFT JOIN \
   OrderDetail Od ON O.Id = Od.OrderId \
   LEFT JOIN \
   Product P ON Od.ProductId = P.Id \
   LEFT JOIN \
   Customer Cu ON O.CustomerId = Cu.Id \
   LEFT JOIN \
   Category Ca ON P.CategoryId = Ca.Id;" \
   , conn, parse_dates=["OrderDate", "RequiredDate", "ShippedDate"], index_col = "OrderId")
	
	# Ubah tipe data object beberapa field dibawah menjadi tipe Categorical
	orders[['ShipRegion', \
		'ShipCountry', \
		'ProductName', \
		'City', 'Region', \
		'Country', \
		'CategoryName']] = \
		orders[['ShipRegion', \
		'ShipCountry', \
		'ProductName' , \
		'City', \
		'Region', \
		'Country', \
		'CategoryName']].astype('category')

	# tambahkan field baru dari extract OrderDate untuk analisa datetime
	orders['OrderDate_dayname'] = orders['OrderDate'].dt.day_name()
	orders['OrderDate_week'] = orders['OrderDate'].dt.week
	orders['OrderDate_month'] = orders['OrderDate'].dt.month
	orders['OrderDate_year'] = orders['OrderDate'].dt.year
	orders['OrderDate_quarter'] = orders['OrderDate'].dt.to_period('Q')
	
	# urutkan kategori DOW nya
	dayorder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	orders['OrderDate_dayname'] = pd.Categorical(orders['OrderDate_dayname'],categories=dayorder,ordered=True)

	# query top5 countries groupby
	top5_orders = pd.read_sql_query(
		"SELECT \
		Od.UnitPrice, \
		Od.Quantity, \
		Od.Discount, \
		SUM((Od.UnitPrice * Od.Quantity) - (Od.UnitPrice * Od.Quantity * Od.Discount)) AS Total, \
		Cu.Country \
		FROM [Order] O \
		LEFT JOIN \
		OrderDetail Od ON O.Id = Od.OrderId \
		LEFT JOIN \
		Product P ON Od.ProductId = P.Id \
		LEFT JOIN \
		Customer Cu ON O.CustomerId = Cu.Id \
		LEFT JOIN \
		Category Ca ON P.CategoryId = Ca.Id \
		GROUP BY Cu.Country \
		ORDER BY Total DESC;" \
		, conn)

	# cari index list top5 countries
	top5 = top5_orders.groupby('Country').Total.sum().sort_values(ascending=False).head().index.to_list()

	# ambil data Orders hanya dari index list top5 
	top5_data = orders[orders['Country'].isin(top5)].copy()

	# analisa data menggunakan pivot dengan agg SUM dari Total = UnitPrice x Quantity x Discount
	pivot_top5_data = pd.pivot_table(
    data=top5_data,
    index='OrderDate_dayname',
    columns=['Country'],
    values='Total',
    aggfunc='sum',
    margins = True
	)


	json_orders = pivot_top5_data.to_json()
	resp = Response(response=json_orders,status=200,mimetype="application/json")
	return(resp)

@app.errorhandler(404)
def page_not_found(e):
	return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/filter', methods=['GET'])
def api_filter():
	query_parameters = request.args
	country = query_parameters.get('country')
	orderdate_start = query_parameters.get('orderdate_start')
	orderdate_end = query_parameters.get('orderdate_end')

	query = "SELECT O.Id OrderId, \
		O.OrderDate, \
		O.RequiredDate, \
		O.ShippedDate, \
		O.ShipRegion, \
		O.ShipCountry, \
		Od.UnitPrice, \
		Od.Quantity, \
		Od.Discount, \
		P.ProductName, \
		ROUND(Od.UnitPrice * Od.Quantity, 2) AS SubTotal, \
		(Od.UnitPrice * Od.Quantity * Od.Discount) AS DiscPrice, \
		(Od.UnitPrice * Od.Quantity) - (Od.UnitPrice * Od.Quantity * Od.Discount) AS Total, \
		Cu.CompanyName AccountName, \
		Cu.ContactName, \
		Cu.ContactTitle, \
		Cu.Address, \
		Cu.City, \
		Cu.Region, \
		Cu.PostalCode, \
		Cu.Country, \
		Cu.Phone, \
		Cu.Fax, \
		Ca.CategoryName, \
		Ca.Description \
		FROM [Order] O \
		LEFT JOIN \
		OrderDetail Od ON O.Id = Od.OrderId \
		LEFT JOIN \
		Product P ON Od.ProductId = P.Id \
		LEFT JOIN \
		Customer Cu ON O.CustomerId = Cu.Id \
		LEFT JOIN \
		Category Ca ON P.CategoryId = Ca.Id WHERE"
	to_filter = []

	if country:
		query += ' Country=? AND'
		to_filter.append(country)

	if orderdate_start:
		query += ' OrderDate BETWEEN ? AND'
		to_filter.append(orderdate_start)

	if orderdate_end:
		query += ' ? AND'
		to_filter.append(orderdate_end)

	if not (country or orderdate_start or orderdate_end):
		return page_not_found(404)

	query = query[:-4] + ';'
	conn = sqlite3.connect("data_input/Northwind_small.sqlite")
	conn.row_factory = dict_factory
	cur = conn.cursor()

	results = cur.execute(query, to_filter).fetchall()

	return jsonify(results)

if __name__ == '__main__':
	app.run(debug=True, port=5000) #run app in debug mode on port 5000