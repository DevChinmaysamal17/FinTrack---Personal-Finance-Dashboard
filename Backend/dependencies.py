from Backend.database import SessionLocal

# Get the stored db for local storage
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()