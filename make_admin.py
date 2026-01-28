from database import SessionLocal
from models import User

db=SessionLocal()

user=db.query(User).filter(User.username=="ansh").first()

if user:
    user.is_admin=True
    db.commit()
    print(f"Success {user.username} is now an Admin.")
else:
    print("User not found")

db.close()