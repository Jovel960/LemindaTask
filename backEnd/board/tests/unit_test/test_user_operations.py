def test_rate_questions(test_client):
    user_op = {'rating':'1'}
    valid_credentials = {
        'userid': 'jovel',
        'password': '1243'
    }
    response = test_client.post('/auth/login', json=valid_credentials)
    assert response.status_code == 200
    assert b"ok" in response.data  
    response = test_client.patch('/feedback/rate/1', json=user_op)
    assert response.status_code == 200
    assert b'{"updated":true}' in response.data  