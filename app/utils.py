from passlib.context import CryptContext
# password protector
pwd_content=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash(password: str):
    return pwd_content.hash(password)