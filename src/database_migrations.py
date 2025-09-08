"""
Simple database migration utility for Bio App.
Handles schema updates without Alembic complexity.
"""

import sqlite3
import os
from typing import List, Dict, Any
from logging_config import db_logger
from database import engine
from sqlalchemy import text


class SimpleMigration:
    """Simple migration handler for database schema updates."""
    
    def __init__(self):
        """Initialize migration handler."""
        self.migrations = [
            {
                'version': 1,
                'description': 'Add image_path column to users table',
                'sql': 'ALTER TABLE users ADD COLUMN image_path VARCHAR(500);'
            }
        ]
    
    def get_current_version(self) -> int:
        """Get current database schema version."""
        try:
            with engine.connect() as conn:
                # Try to get version from migrations table
                try:
                    result = conn.execute(text("SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1"))
                    row = result.fetchone()
                    return row[0] if row else 0
                except Exception:
                    # Migrations table doesn't exist, create it
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS schema_migrations (
                            version INTEGER PRIMARY KEY,
                            description TEXT,
                            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                    conn.commit()
                    return 0
        except Exception as e:
            db_logger.error(f"Failed to get current schema version: {str(e)}")
            return 0
    
    def check_column_exists(self, table: str, column: str) -> bool:
        """Check if a column exists in a table."""
        try:
            with engine.connect() as conn:
                # For SQLite, check table info
                result = conn.execute(text(f"PRAGMA table_info({table})"))
                columns = [row[1] for row in result.fetchall()]
                return column in columns
        except Exception as e:
            db_logger.error(f"Failed to check if column {column} exists in {table}: {str(e)}")
            return False
    
    def apply_migration(self, migration: Dict[str, Any]) -> bool:
        """Apply a single migration."""
        try:
            with engine.connect() as conn:
                # Apply the migration SQL
                conn.execute(text(migration['sql']))
                
                # Record the migration
                conn.execute(text("""
                    INSERT INTO schema_migrations (version, description)
                    VALUES (:version, :description)
                """), {
                    'version': migration['version'],
                    'description': migration['description']
                })
                
                conn.commit()
                db_logger.info(f"Applied migration {migration['version']}: {migration['description']}")
                return True
                
        except Exception as e:
            db_logger.error(f"Failed to apply migration {migration['version']}: {str(e)}")
            return False
    
    def run_migrations(self) -> bool:
        """Run all pending migrations."""
        try:
            current_version = self.get_current_version()
            db_logger.info(f"Current database schema version: {current_version}")
            
            pending_migrations = [m for m in self.migrations if m['version'] > current_version]
            
            if not pending_migrations:
                db_logger.info("No pending migrations")
                return True
            
            db_logger.info(f"Found {len(pending_migrations)} pending migrations")
            
            for migration in pending_migrations:
                # Special handling for image_path column
                if migration['version'] == 1:
                    if self.check_column_exists('users', 'image_path'):
                        db_logger.info("image_path column already exists, skipping migration")
                        # Just record the migration as applied
                        with engine.connect() as conn:
                            conn.execute(text("""
                                INSERT OR IGNORE INTO schema_migrations (version, description)
                                VALUES (:version, :description)
                            """), {
                                'version': migration['version'],
                                'description': migration['description']
                            })
                            conn.commit()
                        continue
                
                if not self.apply_migration(migration):
                    return False
            
            db_logger.info("All migrations applied successfully")
            return True
            
        except Exception as e:
            db_logger.error(f"Failed to run migrations: {str(e)}")
            return False


def run_database_migrations():
    """Run database migrations if needed."""
    try:
        migration = SimpleMigration()
        success = migration.run_migrations()
        
        if success:
            db_logger.info("Database migrations completed successfully")
        else:
            db_logger.error("Database migrations failed")
            
        return success
        
    except Exception as e:
        db_logger.error(f"Migration system error: {str(e)}")
        return False


if __name__ == "__main__":
    # Run migrations when script is executed directly
    run_database_migrations()