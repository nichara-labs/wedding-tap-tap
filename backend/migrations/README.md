# Alembic Setup

## From an empty DB or an existing DB already onboarded to Alembic

Run `alembic revision --autogenerate -m "your commit message"`.

Then, actually apply the migrations with `alembic upgrade head`.

## From an existing DB, not onboarded to Alembic

First, connect to a new DB without any tables.

Run `alembic revision --autogenerate -m "your commit message"`.

Connect to your existing DB and run `alembic stamp head`. This tells Alembic to mark the current state of the DB with the latest revision number.

This marks the state of the current DB as being identical to the state after having run the recently generated migration.

## Upgrades

After making changes to the schema, autogenerate migrations as per above and then run:

```bash
rev=$(alembic heads | cut -d ' ' -f 1) prev=$(alembic history | head -1 | cut -f1 -d' '); alembic upgrade $prev:$rev --sql > alembic/versions/$rev.sql
```

This saves a `.sql` file with the raw SQL commands to be executed in the same directory as the migration `.py` file.

To actually run the migration script, do:

```bash
alembic upgrade head
```

## Check if DB is at latest revision

Run `alembic check`.

Note: This also checks if additional upgrade operations would be generated.

## Show current revision for a database

`alembic current`
