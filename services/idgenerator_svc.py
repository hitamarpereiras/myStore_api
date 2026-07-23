import uuid


def generate_id():
    return uuid.uuid4().hex[:6].upper()

def generate_idStore():
    return uuid.uuid4().hex[:10].upper()

def generate_idProduct():
    return uuid.uuid4().hex[:14].lower()

def generate_Code():
    return uuid.uuid4().hex[:4].lower()