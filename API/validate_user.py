from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from get_db_connection import get_db_connection

router = APIRouter()


class ValidateUserRequest(BaseModel):
    username: str
    password: str


@router.post("/validate-user")
def validate_user(req: ValidateUserRequest):
    """Validate user credentials and return AppUserID on success."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)

        cursor.execute(
            "EXEC procValidateUser @username=%s, @password=%s",
            (req.username, req.password)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "valid": True,
                "message": "User authenticated successfully",
                "AppUserID": result.get("AppUserID"),
                "FullName": result.get("FullName"),
            }

        return {
            "valid": False,
            "message": "Invalid credentials"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
