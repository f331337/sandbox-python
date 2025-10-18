import os
from shutil import copyfile
from celery import Celery
import csv
import asyncio
import asyncpg
from app.models.bank_statement import Transaction

app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_SERVER = "postgres-db"
POSTGRES_PORT = 5432
POSTGRES_DB = "engine"


async def transaction_exists(conn: asyncpg.Connection, transaction_id: str) -> bool:
    query = "SELECT 1 FROM transaction_id WHERE id = $1"
    row = await conn.fetchrow(query, transaction_id)
    return row is not None


async def insert_transaction_ids(conn: asyncpg.Connection, ids: list[str]):
    query = "INSERT INTO transaction_id (id) VALUES ($1)"
    for tid in ids:
        await conn.execute(query, tid)


@app.task(name="tasks.read_file")
def read_file(file_path: str):
    async def process():
        valid_transactions = []
        errors = []

        conn = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            host=POSTGRES_SERVER,
            port=POSTGRES_PORT,
        )

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader, start=2):
                try:
                    transaction = Transaction.model_validate(row)
                    transaction_id = str(transaction.transaction_id).strip()

                    if await transaction_exists(conn, transaction_id):
                        errors.append(
                            {
                                "line": i,
                                "error": "transaction_id already exists in DB",
                                "row": {"TransactionId": transaction_id},
                            }
                        )
                    else:
                        valid_transactions.append(transaction_id)

                except Exception as e:
                    # Try to extract transaction_id if possible, else show unknown
                    transaction_id = row.get("TransactionId", "unknown")
                    errors.append(
                        {
                            "line": i,
                            "error": str(e),
                            "row": {"TransactionId": transaction_id},
                        }
                    )

        # Only insert if no validation or DB errors
        if not errors:
            async with conn.transaction():
                await insert_transaction_ids(conn, valid_transactions)
                # Save the validated file
            VALIDATED_FOLDER = "/app/validated"
            os.makedirs(VALIDATED_FOLDER, exist_ok=True)
            dest_file = os.path.join(VALIDATED_FOLDER, os.path.basename(file_path))
            copyfile(file_path, dest_file)

        await conn.close()

        return {
            "status": "completed",
            "valid_count": len(valid_transactions) if not errors else 0,
            "errors_count": len(errors),
            "errors": errors,
        }

    return asyncio.run(process())
