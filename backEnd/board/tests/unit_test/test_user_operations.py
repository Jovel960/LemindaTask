def test_rate_questions(valid_credentials, test_client):
    valid_user_op = {'rating':'1'}
    invalid_user_op = {'rating':'10'}

    response = test_client.post('/auth/login', json=valid_credentials)
    assert response.status_code == 200
    assert b"ok" in response.data  
    response = test_client.patch('/feedback/rate/1', json=valid_user_op)
    assert response.status_code == 200
    assert b'{"updated":true}' in response.data  
    response = test_client.patch('/feedback/rate/1', json=invalid_user_op)
    assert response.status_code == 400
    assert b'{"error":"rating is missing"}' in response.data 

def test_comment_question(valid_credentials, test_client):
    response = test_client.post('/auth/login', json=valid_credentials)
    assert response.status_code == 200
    assert b"ok" in response.data  
    feedback = {"feedback": "Great"} 
    response = test_client.post('/feedback/comment/3', json=feedback)
    assert response.status_code == 200
    assert b'{"updated":true}' in response.data  

    