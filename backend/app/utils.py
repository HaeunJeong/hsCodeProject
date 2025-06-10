import random
import string

def generate_account_code(length: int = 6) -> str:
    """
    알파벳 대문자와 숫자로 구성된 랜덤 계정 코드를 생성합니다.
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length)) 