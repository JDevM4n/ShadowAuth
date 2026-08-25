from shadowauth.database.postgres_repository import PostgresRepository

repository = PostgresRepository()

sessions = repository.get_all_sessions()

print(sessions)