from fastapi import APIRouter, HTTPException
from get_db_connection import get_db_connection

router = APIRouter()

@router.post("/validate-user")
def validate_user(username: str, password: str):
    """Validate user credentials"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "EXEC procValidateUser @Username=?, @Password=?",
            (username, password)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "valid": True,
                "message": "User authenticated successfully"
            }
        else:
            return {
                "valid": False,
                "message": "Invalid credentials"
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))