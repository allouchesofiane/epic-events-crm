import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")


# Initialiser Sentry
def init_sentry():
    if SENTRY_DSN:
        sentry_sdk.init(dsn=SENTRY_DSN)
        print("Sentry activé")
    else:
        print("Sentry désactivé")


# Envoyer une erreur
def log_error(error):
    if SENTRY_DSN:
        sentry_sdk.capture_exception(error)
    else:
        print("Erreur :", error)


# Envoyer un message simple
def log_message(message):
    if SENTRY_DSN:
        sentry_sdk.capture_message(message)
    else:
        print("Message :", message)
