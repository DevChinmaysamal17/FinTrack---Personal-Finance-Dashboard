from unittest.mock import MagicMock
from Backend.routers.categories import create_category
from Backend.schemas import (
    CategoryCreate,
    CategoryResponse,
)

def test_create_category():
    db = MagicMock()
    user = MagicMock(id=1)

    request = CategoryCreate(name="Food",category_type="expense")

    result = create_category(request=request, db=db, current_user=user)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    assert result.user_id == 1
    assert result.name == "Food"