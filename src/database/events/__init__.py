from sqlalchemy.orm.session import Session

def load_events(session: Session):
    from sqlalchemy.event import listen
    from .events import intercept_after_flush, intercept_before_flush
    listen(session, "before_flush", intercept_before_flush)
    listen(session, "pending_to_persistent", intercept_after_flush)
