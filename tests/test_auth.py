import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from Backend.oauth2 import get_current_user


def test_get_current_user():

  db = MagicMock()

  token_data = MagicMock()
  token_data.id = 1

  user = MagicMock()
  user.id =1

  db.query.return_value.filter.return_value.first.return_value = user

  with patch("Backend.oauth2.jwt_token.verify_token", return_value = token_data):
    result = get_current_user(token="fake_token", db=db)

    assert result is user
    assert result.id == 1


def test_get_current_user_invalid_token():
  db = MagicMock()

  credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  with patch(
    "Backend.oauth2.jwt_token.verify_token",
    side_effect=credentials_exception
  ):
    with pytest.raises(HTTPException) as exc:
      get_current_user(
      token="invalid_token",
      db=db
    )

  assert exc.value.status_code == 401
  assert exc.value.detail == "Could not validate credentials"
  assert exc.value.headers == {"WWW-Authenticate": "Bearer"}


def test_get_current_user_user_not_found():
  db = MagicMock()
  token_data = MagicMock()
  token_data.id = 1

  db.query.return_value.filter.return_value.first.return_value = None

  with patch(
      "Backend.oauth2.jwt_token.verify_token",
      return_value=token_data
  ):
    with pytest.raises(HTTPException) as exc:
      get_current_user(
        token="fake_token",
        db=db
      )
  assert exc.value.status_code == 401
  assert exc.value.detail == "Could not validate credentials"
  assert exc.value.headers == {"WWW-Authenticate": "Bearer"}


def test_get_current_user_no_user_id():

  db = MagicMock()
  token_data = MagicMock()
  token_data.id = None

  with patch(
    "Backend.oauth2.jwt_token.verify_token",
    return_value=token_data
  ):
    with pytest.raises(HTTPException) as exc:
      get_current_user(
        token="fake_token",
        db=db 
    )

  assert exc.value.status_code == 401

