# p4da-capstone-api @aguscuk
This is Algoritma's Python for Data Analysis Capstone Project. 
This project aims to create a simple API to fetch data from Heroku Server.

As a Data Scientist, we demand data to be accessible. 
And as a data owner, we are careful with our data. 
As the answer, data owner create an API for anyone who are granted access to the data to collect them. 
In this capstone project, we will create Flask Application as an API and deploy it to Heroku Web Hosting. 

We provide a brief guideline to create the API and how to Deploy in `capstone-api-markdown.ipynb` using Bahasa Indonesia. 

___
## Dependencies : 
- Pandas    (pip install pandas)
- Flask     (pip install flask)
- Gunicorn  (pip install gunicorn)
- Requests	(pip install requests)
- jsonify	(pip install jsonify)
___
## Goal 
- Create Flask API App
- Deploy to Heroku
- Build API Documentation of how your API works
- Implements the data analysis and wrangling behind the works

___
We have deployed a simple example on : https://aguscuk-capstone-api.herokuapp.com
Here's the list of its endpoints: 
```
1. / , method = GET
Base Endpoint, returning welcoming string value. 

2. /api/v1/resources/<data_name>/all , method = GET
Return full data <data_name> in JSON format. Currently available data are:
    - products
    - suppliers
	- customers
    
3. /api/v1/resources/top5_countries/dow , method = GET
Return top5 countries that have total omzet from orders = UnitPrice * Quantity * Discount

4. /api/v1/resources/filter/<values>
Returns full data of orders filter by :
	- country=<values>, exp: country=Germany
	- orderdate_start=<values>,  exp: orderdate_start=2012-01-01
	- orderdate_end=<values>, exp: orderdate_end=2012-12-31

```

If you want to try it, you can access (copy-paste it) : 
- https://aguscuk-capstone-api.herokuapp.com
- https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/products/all
- https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/suppliers/all
- https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/customers/all
- https://aguscuk-capstone-api.herokuapp.com/api/v1/resources/filter?country=France&orderdate_start=2012-01-01&orderdate_end=2012-12-31
- and so on, just follow the endpoint's pattern