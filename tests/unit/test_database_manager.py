import pytest
from unittest.mock import Mock, patch
from src.core.utils.database_manager import DatabaseManager

@pytest.fixture
def db_manager():
    return DatabaseManager()

@patch('src.core.utils.database_manager.create_engine')
@patch('src.core.utils.database_manager.sessionmaker')
def test_connect_postgres(mock_sessionmaker, mock_create_engine, db_manager):
    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine
    mock_session = Mock()
    mock_sessionmaker.return_value = Mock(return_value=mock_session)

    db_manager.connect_postgres('pg_db', 'postgresql+psycopg2://user:pass@localhost:5432/testdb')

    mock_create_engine.assert_called_once_with('postgresql+psycopg2://user:pass@localhost:5432/testdb')
    assert 'pg_db' in db_manager.engines
    assert 'pg_db' in db_manager.sessions
    assert db_manager.engines['pg_db'] == mock_engine
    assert db_manager.sessions['pg_db'] == mock_session

@patch('src.core.utils.database_manager.create_engine')
@patch('src.core.utils.database_manager.sessionmaker')
def test_connect_mysql(mock_sessionmaker, mock_create_engine, db_manager):
    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine
    mock_session = Mock()
    mock_sessionmaker.return_value = Mock(return_value=mock_session)

    db_manager.connect_mysql('mysql_db', 'mysql+pymysql://user:pass@localhost:3306/testdb')

    mock_create_engine.assert_called_once_with('mysql+pymysql://user:pass@localhost:3306/testdb')
    assert 'mysql_db' in db_manager.engines
    assert 'mysql_db' in db_manager.sessions

def test_query_raises_error_if_not_connected(db_manager):
    with pytest.raises(ValueError, match="Database connection 'unknown_db' not found."):
        db_manager.query('unknown_db', 'SELECT * FROM users')

@patch('src.core.utils.database_manager.create_engine')
@patch('src.core.utils.database_manager.sessionmaker')
def test_query_returns_results(mock_sessionmaker, mock_create_engine, db_manager):
    mock_session = Mock()
    mock_sessionmaker.return_value = Mock(return_value=mock_session)
    
    mock_result = Mock()
    mock_result.returns_rows = True
    
    # Mocking rows that have _asdict method
    mock_row1 = Mock()
    mock_row1._asdict.return_value = {"id": 1, "name": "Alice"}
    mock_row2 = Mock()
    mock_row2._asdict.return_value = {"id": 2, "name": "Bob"}
    
    mock_result.fetchall.return_value = [mock_row1, mock_row2]
    mock_session.execute.return_value = mock_result

    db_manager.connect_postgres('test_db', 'sqlite:///:memory:')
    results = db_manager.query('test_db', 'SELECT * FROM users')

    assert len(results) == 2
    assert results[0]['name'] == 'Alice'
    assert results[1]['name'] == 'Bob'
    mock_session.execute.assert_called_once()

@patch('src.core.utils.database_manager.create_engine')
@patch('src.core.utils.database_manager.sessionmaker')
def test_close_connection(mock_sessionmaker, mock_create_engine, db_manager):
    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine
    mock_session = Mock()
    mock_sessionmaker.return_value = Mock(return_value=mock_session)

    db_manager.connect_postgres('db1', 'sqlite:///:memory:')
    db_manager.connect_postgres('db2', 'sqlite:///:memory:')

    # Close specific connection
    db_manager.close('db1')
    mock_session.close.assert_called_once()
    mock_engine.dispose.assert_called_once()
    assert 'db1' not in db_manager.sessions
    assert 'db2' in db_manager.sessions

    # Close all remaining connections
    db_manager.close()
    assert mock_session.close.call_count == 2
    assert mock_engine.dispose.call_count == 2
    assert len(db_manager.sessions) == 0
