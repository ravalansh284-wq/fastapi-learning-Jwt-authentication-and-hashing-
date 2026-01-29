from database import SessionLocal
from models import User, Role, UserRole

def make_user_admin(username_to_promote):
    db = SessionLocal()

    user = db.query(User).filter(User.username == username_to_promote).first()
    if not user:
        print(f"User {username_to_promote} not found!")
        return

    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    existing_link = db.query(UserRole).filter(
        UserRole.user_id == user.id,
        UserRole.role_id == admin_role.id
    ).first()

    if existing_link:
        print(f"{user.username} is already an Admin.")
    else:
        new_link = UserRole(user_id=user.id, role_id=admin_role.id)
        db.add(new_link)
        db.commit()
        print(f"Success! {user.username} is now an Admin.")

    db.close()

if __name__ == "__main__":
    make_user_admin("testuser")