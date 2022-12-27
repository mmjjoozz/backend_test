# backend_test - Michal Jozwiak

## Prerequisites
- Python 3.10
- Flask

## Setting up

- Set up a virtual environment using virtualenv, Pipenv etc.
- If using virtualenv, run `pip install -r requirements.txt`
- Once requirements are installed, go to project's root, run `export FLASK_APP=app/api.py` and following that, the app can be run using `flask run`. Running with wsgi is also an option
- SQLAlchemy will automatically create a sqlite3 database in the `/instance` directory. On the first application run several `Products` will be inserted into the DB for convenient testing. Those are based on the schema and data I've been given as part of this challenge.

## Unit testing
- Tests can be found in the `/tests` directory
- To run the unit tests, simply run the `pytest tests` command

## Assumptions, notes, caveats
- Since DRF was mentioned in the initial interview, I thought it would be a good idea to use a similar framework here - the project is built with Flask-Restful, allowing me to structure the code in a much more readable and clean way than if I used pure Flask. Thus the `orders.py` file became `resources.py`. 
- I took the liberty to remove the `init_db.py` file and included the same functionality on application startup - data prepopulation is still there, via SQLAlchemy ORM (again - ORM's were talked about during the initial interview).
- I've kept the database design pretty much the same. Some unique constraints are placed on the combination of boat name + price to avoid any accidental redundancy.
- In a real life scenario the tables would be much more complex - we'd probably want some extra fields for keeping track of the amount of boats we've got available, creation and update times etc., however, I've decided against any extras to keep the project as close to the original boilerplate as possible.
- With the above in mind, I've decided to allow an unlimited amount of orders to be made per each boat type. This is intentional - in my mind I was building an API for a proper store with lots of boats.
- I've assumed that each boat's sale price will depend on negotiations, therefore e.g. a Catamaran can have different discounts depending on whatever the customer has negotiated. The `/metrics` endpoint returns the average of all discounts for a boat.
- On a flipside, if a boat regularly sells for more than its list price, the discount is displayed as 0 - the API does not consider price increases in these metrics. NB. if a boat regularly goes over the list price and the total for actual prices and the average are higher than the list price, it'll be displayed as 0 - on average, the boat does not get discounted.
- A sqlite3 database is included with the project for convenience' sake. This already contains the Product data. Feel free to delete if testing, it'll be recreated with the data next time the application is run.
