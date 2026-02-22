import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")


def init_sentry():
    """Initialise Sentry."""
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            traces_sample_rate=0.0,
            profiles_sample_rate=0.0,
        )
        print("✓ Sentry activé pour la journalisation")
    else:
        print("⚠ Sentry DSN non configuré - journalisation désactivée")


def log_event(event_name, data=None):
    """
    Journalise un événement métier.
    """
    if SENTRY_DSN:
        with sentry_sdk.configure_scope() as scope:
            if data:
                scope.set_context("event_data", data)
            sentry_sdk.capture_message(event_name, level="info")


def log_error(error, context=None):
    """
    Journalise une erreur.
    """
    if SENTRY_DSN:
        with sentry_sdk.configure_scope() as scope:
            if context:
                scope.set_context("error_context", context)
            sentry_sdk.capture_exception(error)