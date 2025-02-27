from alembic.config import Config
from alembic import command


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    print("Running Alembic migrations...")
    run_migrations()
    print("Database initialized.")
