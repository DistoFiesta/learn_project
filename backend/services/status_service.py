def get_status_data():
    return {
        "status": "OK",
        "message": "backend работает",
        "service": "backend-service",
        "items_count": 3
    }
def get_items_data():
    return {
        {id: 1, "name": "Товар 1"},
        {id: 2, "name": "Товар 2"},
        {id: 3, "name": "Товар 3"}
    }