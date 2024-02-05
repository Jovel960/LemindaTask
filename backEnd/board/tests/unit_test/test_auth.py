# test_auth.py
def test_login_route(test_client):
    # Data for a valid login attempt
    invalid_credentials = {
        'userid': 'yovel',
        'password': '12345'
    }

    valid_credentials = {
        'userid': 'jovel',
        'password': '1243'
    }

    

    # Test invalid login
    response = test_client.post('/auth/login', json=invalid_credentials)
    assert response.status_code == 400 
    assert b"error" in response.data  

    response = test_client.post('/auth/login', json=valid_credentials)
    assert response.status_code == 200
    assert b"ok" in response.data  

def test_is_logged_route(test_client):
    response = test_client.get('/auth/islogged')
    assert response.status_code == 200


def test_logout_route(test_client):
    response = test_client.post('/auth/logout')
    assert response.status_code == 200
