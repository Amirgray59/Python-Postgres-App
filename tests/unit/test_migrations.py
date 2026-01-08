import os
import subprocess

ALEMBIC_CMD = ["alembic"]

def run(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )


def test_migrate_up_and_down():
    
    
    run(ALEMBIC_CMD + ["downgrade", "base"])

    run(ALEMBIC_CMD + ["upgrade", "head"])
