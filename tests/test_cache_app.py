from cache_app import app
import json
import requests

init_data = {
    "abc1" : "1",
    "abc2" : "2",
    "xyz1" : "3",
    "xyz2" : "4"
}

def test_set_key_value():
    response = app.test_client().post('/set', data=json.dumps(init_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == init_data

def test_empty_value():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'set data before' in response.data

def test_invalid_value():
    response = app.test_client().get('/random')
    assert response.status_code == 404

def test_get_value():
    response = app.test_client().get('/get/abc1')
    assert response.status_code == 200
    assert str(response.get_data(as_text=True)) == '1'

    response = app.test_client().get('/get/abc2')
    assert response.status_code == 200
    assert str(response.get_data(as_text=True)) == '2'

    response = app.test_client().get('/get/xyz1')
    assert response.status_code == 200
    assert str(response.get_data(as_text=True)) == '3'

    response = app.test_client().get('/get/xyz2')
    assert response.status_code == 200
    assert str(response.get_data(as_text=True)) == '4'

    response = app.test_client().get('/get/abcde')
    assert response.status_code == 200
    assert b'Invalid key' in response.data

def test_search_prefix():
    response = app.test_client().get('/search', query_string={"prefix":"abc"})
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '["abc1","abc2"]\n'

    response = app.test_client().get('/search', query_string={"prefix":"abcde"})
    assert response.status_code == 200
    assert b'Invalid prefix/suffix' in response.data

def test_search_suffix():
    response = app.test_client().get('/search', query_string={"suffix":"1"})
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '["abc1","xyz1"]\n'

    response = app.test_client().get('/search', query_string={"suffix":"12"})
    assert response.status_code == 200
    assert b'Invalid prefix/suffix' in response.data

def test_search_prefix_suffix():
    response = app.test_client().get('/search', query_string={"prefix":"abc","suffix":"1"})
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '["abc1"]\n'

    response = app.test_client().get('/search', query_string={"prefix":"","suffix":""})
    assert response.status_code == 200
    assert b'Invalid prefix/suffix' in response.data