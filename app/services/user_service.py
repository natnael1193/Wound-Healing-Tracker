

from app.db.models.user import User
from app.utils.response import success_response
from app.schemas.user import UserMe
from uuid import UUID

def update_user( 
    db = None,
    current_user=None,
    name: str = None,
    # email: str = None,
):  
    # return current_user['name']
    logged_in_user = db.query(User).filter(User.id == UUID(current_user['id'])).first()
    
    if not logged_in_user:
        return success_response(None, "User not found", 404)
        
    # Update the existing user instead of creating a new one
    logged_in_user.name = name
    
    db.commit()
    db.refresh(logged_in_user)
    
    # Use UserMe model for proper serialization
    user_data = UserMe.from_user(logged_in_user)
    return success_response(user_data, "User updated successfully")  