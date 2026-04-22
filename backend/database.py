from sqlmodel import SQLModel, create_engine, Session

# HIER NICHTS ÄNDERN, SQLite-Datei liegt im Render-Filesystem
DATABASE_URL = "sqlite:///./ludara.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from import models  # wichtig, damit Tabellen bekannt sind
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
