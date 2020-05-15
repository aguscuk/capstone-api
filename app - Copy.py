import flask
from flask import request, jsonify, Response
import sqlite3
import pandas as pd

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Capstone API</h1>
<p>aguscuk capstone project api</p>'''



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

@app.route('/api/v1/resources/orders/all', methods=['GET'])
def orders_all():
	conn = sqlite3.connect("data_input/Northwind_small.sqlite")
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
							   Category Ca ON P.CategoryId = Ca.Id;",conn)
	json_orders = orders.to_json()
	resp = Response(response=json_orders,status=200,mimetype="application/json")
	return(resp)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000