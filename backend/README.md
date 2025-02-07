# Basic Crud to test Fast API with SQLAlchemy and alembic

- run fastApi server
  $ app/

```
uvicorn main:app
```

- Make migrations

```
alembic revision --autogenerate -m "Commit"
```

- run migration

```
alembic upgrade head
```

- revert changes

```
alembic downgrade -1
```

- revert to specif version

```
alembic downgrade <version_id>
```
