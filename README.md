# Flask_RESTful_API_with_SQL

This API is built with Flask, Flask_RESTful, Flask_JWT, and Flask-SQLAlchemy.
Then, deployed on Heroku.

## Feel free to test the Api
The easy way to test the API is using Postman to make http requests.
URL of API: https://wei-restful-api.herokuapp.com/

## HTTP methods
This API provide GET, POST, PUT, DELETE requests.  


## 1. POST request  
First of all, clients can register by making POST request.
```
https://wei-restful-api.herokuapp.com/register
```
The body of request should be json format.
For example,
```
{
	"username": "your_user_name",
	"password": "your_password"
}
```

After registering, it allow clients to login by making POST request
```
https://wei-restful-api.herokuapp.com/auth
```
The body of request should be json format.  
For example,
```
{
	"username": "your_user_name",
	"password": "your_password"
}
```

After login, it allow clients to create the store by making POST request
```
https://wei-restful-api.herokuapp.com/store/<store_name>
```
The response look like this
```
{
    "name": "<store_name>",
    "items": []
}
```

Then, clients can create item for the store by making POST request.
```
https://wei-restful-api.herokuapp.com/item/<item_name>
```
The post request should contain
```
{
	"price": 15.99,
	"store_id": 1
}
```

## 2. GET request  
Clients can retrieve all items in the system by making GET request.
```
https://wei-restful-api.herokuapp.com/items
```
The results look like This
```
{
    "items": [
        {
            "name": "<item_name>",
            "price": 15.99
        }
    ]
}
```

Likewise, all stores could be retrieved by GET request.
```
https://wei-restful-api.herokuapp.com/stores
```

## 3. DELETE request  
Stores and items could be delete by making DELETE requests.
However, all items should be deleted before deleting stores because items have foreign which refer to primary key of store table.
```
https://wei-restful-api.herokuapp.com/store/<store_name>
https://wei-restful-api.herokuapp.com/item/<item_name>
```

## 4. PUT request  
Finally, items could be create if not exist by making PUT requests.
In addition, PUT requests could update items if items already exist.
```
https://wei-restful-api.herokuapp.com/item/<item_name>
```
