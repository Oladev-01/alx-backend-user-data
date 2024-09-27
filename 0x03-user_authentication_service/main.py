#!/usr/bin/env python3
"""
Main file
"""
import requests

url = "http://localhost:5000/"


def register_user(email: str, password: str) -> None:
    """checking the register endpoint"""
    reg_url = f"{url}/users"
    response = requests.post(reg_url, data={'email': email,
                                            'password': password})
    if response.status_code == 200:
        expected = {"email": email, "message": "user created"}
        assert response.json() == expected
    elif response.status_code == 400:
        expected = {"message": "email already registered"}
        assert response.json() == expected


def log_in_wrong_password(email: str, password: str) -> None:
    """checking login"""
    log_url = f'{url}/sessions'
    response = requests.post(log_url, data={'email': email,
                                            'password': password})
    assert response.status_code == 401


def profile_unlogged():
    """check profile"""
    log_url = f'{url}/profile'
    cookies = {'session_id': None}
    response = requests.get(log_url, cookies=cookies)
    assert response.status_code == 403
    cookies = {'session_id': 'invalid'}
    response = requests.get(log_url, cookies=cookies)
    assert response.status_code == 403


def log_in(EMAIL: str, PASSWD: str) -> str:
    """check login"""
    log_url = f'{url}/sessions'
    response = requests.post(log_url, data={'email': EMAIL,
                                            'password': PASSWD})
    assert response.status_code == 200
    expected = {"email": EMAIL, "message": "logged in"}
    assert response.json() == expected
    assert 'session_id' in response.cookies
    return response.cookies.get('session_id')


def profile_logged(session_id: str):
    """should get profile"""
    log_url = f'{url}/profile'
    cookies = {'session_id': session_id}
    response = requests.get(log_url, cookies=cookies)
    assert response.status_code == 200
    expected = {"email": EMAIL}
    assert response.json() == expected


def log_out(session_id: str) -> None:
    """Logging out"""
    log_url = f'{url}/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(log_url, cookies=cookies)

    # Expect a 302 status code for redirect
    assert response.status_code == 200
    cookies = {'session_id': None}
    response = requests.delete(log_url, cookies=cookies)
    assert response.status_code == 403
    cookies = {'session_id': 'invalid'}
    response = requests.delete(log_url, cookies=cookies)
    assert response.status_code == 403


def reset_password_token(EMAIL: str) -> str:
    """get reset token for password"""
    log_url = f'{url}/reset_password'
    response = requests.post(log_url, data={'email': EMAIL})
    assert response.status_code == 200
    assert 'reset_token' in response.json()
    return response.json().get('reset_token')


def update_password(EMAIL: str, reset_token: str, NEW_PASSWD: str) -> None:
    """reset and update password"""
    log_url = f'{url}/reset_password'
    response = requests.put(log_url, data={'email': EMAIL,
                                           'reset_token': reset_token,
                                           'new_password': NEW_PASSWD})
    expected = {"email": EMAIL, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == expected


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
