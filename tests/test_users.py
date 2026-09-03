import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from Backend.routers.users import create_user, destroy_user
from Backend.schemas import UserCreate


# def test_get_current_user():

#   db = MagicMock()

#   token_data = MagicMock()
#   token_data.id = 1

#   user = MagicMock()
#   user.id =1

#   db.query.return_value.filter.return_value.first.return_value = user

#   with patch("Backend.oauth2.jwt_token.verify_token", return_value = token_data):
#     result = get_current_user(token="fake_token", db=db)

#     assert result is user
#     assert result.id == 1


@patch("Backend.routers.users.Hash.bcrypt")
def test_create_user(mock_bcrypt):
  db = MagicMock()

  db.query.return_value.filter.return_value.first.return_value = None

  mock_bcrypt.return_value = "hashed_password"

  request = UserCreate(
    name="Chinmay",
    email="chinmay@example.com",
    password="password123"
  )

  result = create_user(request, db)
  assert db.add.called

  db.commit.assert_called()

  db.refresh.assert_called_once()
  assert result.name == "Chinmay"
  assert result.email == "chinmay@example.com"

