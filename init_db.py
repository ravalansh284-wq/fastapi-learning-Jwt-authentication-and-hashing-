from database import SessionLocal
from models import Role

def init_roles():
    db = SessionLocal()
    if not db.query(Role).filter(Role.name == "Admin").first():
        admin_role = Role(name="Admin")
        db.add(admin_role)
        print("Created Admin Role")
        
    if not db.query(Role).filter(Role.name == "User").first():
        user_role = Role(name="User")
        db.add(user_role)
        print("Created User Role")
        
    db.commit()
    db.close()

if __name__ == "__main__":
    print("Initializing Roles...")
    init_roles()
    print("Done!")