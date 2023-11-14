# Import Modules
from better_profanity import profanity

def filterProfanity(subject, message, filter_profanity):

    subject_contains_profanity = profanity.contains_profanity(subject)
    message_contains_profanity = profanity.contains_profanity(message)

    if filter_profanity:
        subject = profanity.censor(subject)
        message = profanity.censor(message)
    
    return subject, message, subject_contains_profanity, message_contains_profanity
