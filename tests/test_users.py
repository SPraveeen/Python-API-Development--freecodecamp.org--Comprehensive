from app import schemas
from .database import client,session


def test_root(client):
    res=client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message')=='Welcome'
    assert res.status_code==200


def test_create_user(client):
    res=client.post("/users/",json={"email":"hello123@gmail.com","password":"123456"})

    new_user=schemas.Userout(**res.json())
    assert new_user.email=="hello123@gmail.com"
    assert res.status_code==201

def test_login_user(client):
    res=client.post("/login",data={"username":"hello123@gmail.com","password":"123456"})
    assert res.status_code==200