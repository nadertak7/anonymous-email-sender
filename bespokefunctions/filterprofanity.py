# Import Modules
from better_profanity import profanity

def filterProfanity(subject, 
                    message, 
                    filter_profanity):

    # Determines whether subject and message contain profanity. Bool will be inerted in db in bespokefuncitons/db.py
    subject_contains_profanity = profanity.contains_profanity(subject)
    message_contains_profanity = profanity.contains_profanity(message)

    # If filter profanity is selected in homepage, censor. 
    if filter_profanity:
        subject = profanity.censor(subject)
        message = profanity.censor(message)    
    
    return (subject, 
            message, 
            subject_contains_profanity, 
            message_contains_profanity)