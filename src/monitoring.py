"""
Monitoring and health check functionality.
Provides metrics collection and health check endpoints.
"""

import psutil
from datetime import datetime
from typing import Dict, Any, Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from logging_config import app_logger
from database import engine
from sqlalchemy import text


# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_SESSIONS = Gauge('active_sessions_total', 'Total active sessions')
DATABASE_CONNECTIONS = Gauge('database_connections_active', 'Active database connections')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')


class HealthChecker:
    """Health check functionality for the application."""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
    
    def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and health."""
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
            
            return {
                "status": "healthy",
                "message": "Database connection successful",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            app_logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check system resource health."""
        try:
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('/')
            
            # Update Prometheus metrics
            MEMORY_USAGE.set(memory.used)
            CPU_USAGE.set(cpu_percent)
            
            return {
                "status": "healthy",
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent_used": memory.percent
                },
                "cpu": {
                    "percent_used": cpu_percent
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "percent_used": (disk.used / disk.total) * 100
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            app_logger.error(f"System health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": f"System health check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_application_health(self) -> Dict[str, Any]:
        """Get overall application health status."""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        db_health = self.check_database_health()
        system_health = self.check_system_health()
        
        overall_status = "healthy"
        if db_health["status"] != "healthy" or system_health["status"] != "healthy":
            overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "uptime_seconds": uptime,
            "start_time": self.start_time.isoformat(),
            "database": db_health,
            "system": system_health,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_metrics(self) -> str:
        """Get Prometheus metrics in text format."""
        return generate_latest()


# Global health checker instance
health_checker = HealthChecker()


def record_request_metrics(method: str, endpoint: str, status_code: int, duration: float):
    """Record request metrics for monitoring."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
    REQUEST_DURATION.observe(duration)


def update_session_metrics(active_count: int = None):
    """Update active session metrics."""
    try:
        if active_count is None:
            # Get count from session store
            from session_store import session_store
            active_count = session_store.get_active_session_count()
        
        ACTIVE_SESSIONS.set(active_count)
        app_logger.debug(f"Updated session metrics: {active_count} active sessions")
    except Exception as e:
        app_logger.warning(f"Failed to update session metrics: {str(e)}")


def update_database_metrics():
    """Update database connection metrics."""
    try:
        pool = engine.pool
        DATABASE_CONNECTIONS.set(pool.size() - pool.checkedout())
    except Exception as e:
        app_logger.warning(f"Failed to update database metrics: {str(e)}")
