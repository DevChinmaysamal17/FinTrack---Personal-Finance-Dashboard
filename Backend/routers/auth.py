from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from Backend import models, jwt_token, dependencies
from sqlalchemy.orm import Session
from Backend.hashing import Hash


router = APIRouter(
    tags=["Authentication"]
)

# Verification of the user credentials
@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials" )

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials" )
    
    access_token = jwt_token.create_access_token(data={"user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}