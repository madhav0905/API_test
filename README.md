
tested on postman
api for products
http://127.0.0.1:8000/api/v1/products/#

sampel json 
{
    "data": [
        {
            "id": "65b6977f69326be64dbd311c",
            "name": "TV",
            "price": 29.99,
            "quantity": 100
        },
        {
            "id": "65b6973d585293a254a14c2f",
            "name": "Product Name",
            "price": 29.99,
            "quantity": 100
        },
       
        {
            "id": "65b696c296c66b98d195dd22",
            "name": "Product Name",
            "price": 29.99,
            "quantity": 100
        }
    ],
    "page": {
        "limit": 10,
        "nextOffset": null,
        "prevOffset": null,
        "total": 4
    }
}


for post call of orders
body

{
  "items": [{"productId":"65b696c296c66b98d195dd22","boughtQuantity":2}],
  "userAddress": {"city":"abc","zipCode":"random","country":"india"}

}

output
{
    "orderId":"65b696ec37f782537265db41"
}
