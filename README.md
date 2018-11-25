# Flask_RESTful_API_with_SQL

This API is built with Flask, Flask_RESTful, Flask_JWT, and Flask-SQLAlchemy.
Then, deployed on Heroku.

## Feel free to test the Api
The easy way to test the API is using Postman to make http requests.
URL of documentation: https://documenter.getpostman.com/view/4215311/RzfZQtLb
Dom

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
https://wei-restful-api.herokuapp.com/login
```
The body of request should be json format.  
For example,
```
{
	"username": "your_user_name",
	"password": "your_password"
}
```
After login, clients will get the response look like below
````
{
    "access_token": "your_access_token",
    "refresh_token": "your_refresh_token"
}
````
User can logout by making post request.
The Header of logout post request should contain the access token of current user.

After login, it allow clients to create stores and items by making POST request
```
https://wei-restful-api.herokuapp.com/store/<store_name>
```
The response of creating stores look like this
```
{
    "id": 1,
    "name": "store_name",
    "items": []
}
```

Likewise, clients can create item for the store by making POST request.
```
https://wei-restful-api.herokuapp.com/item/<item_name>
```
The post request should contain
```
{
	"price": "price_of_item",
	"store_id": "store_id"
}
```
After successfully creating a item in store, clients will get response look like this
```
{
    "id": "item_id",
    "name": "item_name",
    "price": "price_of_item",
    "store_id": "store_id"
}
```

If access token is expired, users can get non-fresh token by make refresh post request in order to get the new access token.
```
https://wei-restful-api.herokuapp.com/refresh
```
After refreshing, clients will get a response which contain new access token like below
{
    "access_token": "your_new_access_token"
}

## 2. GET request  
Clients can retrieve all items in the system by making GET request.  
Note: The access token is required if users want to make get request for finding all items.
```
https://wei-restful-api.herokuapp.com/items
```
The response look like This
```
{
    "item": [
        {
            "id": 1,
            "name": "table",
            "price": 15.99,
            "store_id": 1
        }
    ]
}
```

Likewise, all stores could be retrieved by GET request.
```
https://wei-restful-api.herokuapp.com/stores
```
The response look like below.
```
{
    "store": [
        {
            "id": "item_id",
            "name": "store_name",
            "items": [
                {
                    "id": 1,
                    "name": "item_name",
                    "price": price_of_item,
                    "store_id": "store_id"
                }
            ]
        }
    ]
}
```

Clients are able to retrieve single item, store and user by making following get requests.  
Note: The access token is required is clients want to get single item data.  
```
https://wei-restful-api.herokuapp.com/store/<store_name>
https://wei-restful-api.herokuapp.com/item/<item_name>
https://wei-restful-api.herokuapp.com/user/<user_id>
```
## 3. DELETE request  
Stores and items could be delete by making DELETE requests.
However, all items should be deleted before deleting stores because items have foreign which refer to primary key of store table. In addition, the access token is required if clients want to delete items and stores. Client can get new access token by refreshing token.
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
The body of put request should look like This
```
{
	"store_id": "store_id",
	"price": 18.99
}
```
