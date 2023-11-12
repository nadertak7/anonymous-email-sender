# Checks if email, subject, message variables are populated
def checkFields(email, subject, message):
    if not (email and subject and message):
        return False
    else: 
        return True