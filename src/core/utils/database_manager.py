from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from src.core.utils.logger import logger

class DatabaseManager:
    """Utility for interacting with PostgreSQL and MySQL databases."""

    def __init__(self):
        self.engines: Dict[str, Any] = {}
        self.sessions: Dict[str, Session] = {}

    def connect_postgres(self, connection_id: str, connection_string: str) -> None:
        """
        Connect to a PostgreSQL database.
        Format: postgresql+psycopg2://user:password@host:port/dbname
        """
        try:
            engine = create_engine(connection_string)
            self.engines[connection_id] = engine
            self.sessions[connection_id] = sessionmaker(bind=engine)()
            logger.info(f"Connected to PostgreSQL database: {connection_id}")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL database '{connection_id}': {e}")
            raise

    def connect_mysql(self, connection_id: str, connection_string: str) -> None:
        """
        Connect to a MySQL database.
        Format: mysql+pymysql://user:password@host:port/dbname
        """
        try:
            engine = create_engine(connection_string)
            self.engines[connection_id] = engine
            self.sessions[connection_id] = sessionmaker(bind=engine)()
            logger.info(f"Connected to MySQL database: {connection_id}")
        except Exception as e:
            logger.error(f"Failed to connect to MySQL database '{connection_id}': {e}")
            raise

    def query(self, connection_id: str, query_string: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a SQL query and returns the results as a list of dictionaries."""
        if connection_id not in self.sessions:
            raise ValueError(f"Database connection '{connection_id}' not found.")

        session = self.sessions[connection_id]
        try:
            logger.info(f"Executing query on '{connection_id}': {query_string}")
            result = session.execute(text(query_string), parameters or {})
            if getattr(result, "returns_rows", False):
                # Convert rows to dict
                return [row._asdict() for row in result.fetchall()]
            session.commit()
            return []
        except Exception as e:
            session.rollback()
            logger.error(f"Query execution failed: {e}")
            raise

    def close(self, connection_id: Optional[str] = None) -> None:
        """Closes a specific connection or all connections if no ID is provided."""
        if connection_id:
            if connection_id in self.sessions:
                self.sessions[connection_id].close()
                self.engines[connection_id].dispose()
                del self.sessions[connection_id]
                del self.engines[connection_id]
                logger.info(f"Closed database connection: {connection_id}")
        else:
            for c_id, session in list(self.sessions.items()):
                session.close()
                self.engines[c_id].dispose()
                logger.info(f"Closed database connection: {c_id}")
            self.sessions.clear()
            self.engines.clear()

database_manager = DatabaseManager()
