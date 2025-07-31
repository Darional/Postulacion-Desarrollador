
valid_user = {
    "name": "Juan Rodriguez",
    "email": "juan@rodriguez.org",
    "password": "Hunter212",
    "phones": [
        { "number": "1234567", "citycode": "1", "contrycode": "57" }
    ]
}

bad_email = {
    **valid_user, "email": "no-email"
}

bad_password = {
    **valid_user, "password": "hunter"
}
