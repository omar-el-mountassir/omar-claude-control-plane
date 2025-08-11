#!/usr/bin/env python3
"""
PADA Database - Personal AI Development Assistant Data Layer
SQLite-based async database for storing events, actions, learning data, and metrics
"""

import aiosqlite
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import uuid

# Import PADA core types
from .pada_main import Event, ActionResult

logger = logging.getLogger(__name__)

class PADADatabase:
    """Async SQLite database for PADA data storage"""
    
    def __init__(self, database_url: str):
        # Parse database URL (supports sqlite:///path format)
        if database_url.startswith('sqlite:///'):
            self.db_path = database_url[10:]  # Remove 'sqlite:///'
        elif database_url.startswith('sqlite://'):
            self.db_path = database_url[9:]   # Remove 'sqlite://'
        else:
            self.db_path = database_url
        
        # Ensure directory exists
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.db = None
        logger.info(f"PADA database initialized: {self.db_path}")
    
    async def initialize(self):
        """Initialize database connection and create tables"""
        
        logger.info("Initializing PADA database...")
        
        # Connect to database
        self.db = await aiosqlite.connect(self.db_path)
        
        # Enable foreign keys
        await self.db.execute("PRAGMA foreign_keys = ON")
        
        # Create tables
        await self._create_tables()
        
        # Create indexes for performance
        await self._create_indexes()
        
        await self.db.commit()
        
        logger.info("PADA database initialized successfully")
    
    async def _create_tables(self):
        """Create all database tables"""
        
        # Events table - stores all incoming events
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                severity TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                data TEXT,  -- JSON data
                requires_action BOOLEAN DEFAULT 0,
                suggested_actions TEXT,  -- JSON array
                processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Action results table - stores autonomous action outcomes
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS action_results (
                action_id TEXT PRIMARY KEY,
                event_id TEXT,
                action_type TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                rep_score REAL NOT NULL,
                human_validation_needed BOOLEAN DEFAULT 0,
                details TEXT,  -- JSON details
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        ''')
        
        # Notifications table - tracks notification delivery
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                status TEXT NOT NULL,  -- sent, delivered, failed, dismissed
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                delivered_at DATETIME,
                user_action TEXT,  -- dismissed, clicked, ignored
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        ''')
        
        # User feedback table - for learning system
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id TEXT PRIMARY KEY,
                event_id TEXT,
                action_id TEXT,
                feedback_type TEXT NOT NULL,  -- notification, action, suggestion
                helpful BOOLEAN NOT NULL,
                rating INTEGER,  -- 1-5 scale
                comment TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (action_id) REFERENCES action_results (action_id)
            )
        ''')
        
        # Learning patterns table - stores learned user preferences
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,  -- notification_preference, action_preference
                pattern_data TEXT NOT NULL,  -- JSON pattern data
                confidence_score REAL NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                times_applied INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0
            )
        ''')
        
        # Health metrics table - system health tracking
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS health_metrics (
                id TEXT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                component TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                status TEXT,  -- healthy, warning, critical
                details TEXT  -- JSON details
            )
        ''')
        
        # Statistics table - aggregated statistics
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id TEXT PRIMARY KEY,
                stat_type TEXT NOT NULL,  -- daily, weekly, monthly
                stat_date DATE NOT NULL,
                stat_data TEXT NOT NULL,  -- JSON statistics data
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    async def _create_indexes(self):
        """Create database indexes for performance"""
        
        # Events indexes
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events (timestamp)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON events (type)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_events_severity ON events (severity)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_events_source ON events (source)')
        
        # Action results indexes
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_actions_timestamp ON action_results (timestamp)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_actions_type ON action_results (action_type)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_actions_success ON action_results (success)')
        
        # Notifications indexes
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_notifications_sent_at ON notifications (sent_at)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications (status)')
        
        # Feedback indexes
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_feedback_timestamp ON user_feedback (timestamp)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_feedback_type ON user_feedback (feedback_type)')
        
        # Health metrics indexes
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_health_timestamp ON health_metrics (timestamp)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_health_component ON health_metrics (component)')
    
    async def store_event(self, event: Event):
        """Store an event in the database"""
        
        await self.db.execute('''
            INSERT INTO events (
                id, source, type, title, description, severity, 
                timestamp, data, requires_action, suggested_actions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event.id,
            event.source,
            event.type,
            event.title,
            event.description,
            event.severity,
            event.timestamp.isoformat(),
            json.dumps(event.data) if event.data else None,
            event.requires_action,
            json.dumps(event.suggested_actions) if event.suggested_actions else None
        ))
        
        await self.db.commit()
        logger.debug(f"Stored event: {event.id}")
    
    async def store_action_result(self, action_result: ActionResult):
        """Store an action result in the database"""
        
        await self.db.execute('''
            INSERT INTO action_results (
                action_id, action_type, success, rep_score,
                human_validation_needed, details, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            action_result.action_id,
            action_result.action_type,
            action_result.success,
            action_result.rep_score,
            action_result.human_validation_needed,
            json.dumps(action_result.details) if action_result.details else None,
            action_result.timestamp.isoformat()
        ))
        
        await self.db.commit()
        logger.debug(f"Stored action result: {action_result.action_id}")
    
    async def track_notification(self, event_id: str, status: str, channel: str = "default"):
        """Track notification delivery status"""
        
        notification_id = f"notif_{event_id}_{int(datetime.utcnow().timestamp())}"
        
        await self.db.execute('''
            INSERT INTO notifications (id, event_id, channel, status)
            VALUES (?, ?, ?, ?)
        ''', (notification_id, event_id, channel, status))
        
        await self.db.commit()
        logger.debug(f"Tracked notification: {notification_id}")
    
    async def store_user_feedback(self, event_id: str, feedback_type: str, helpful: bool, 
                                action_id: Optional[str] = None, rating: Optional[int] = None,
                                comment: Optional[str] = None):
        """Store user feedback for learning"""
        
        feedback_id = str(uuid.uuid4())
        
        await self.db.execute('''
            INSERT INTO user_feedback (
                id, event_id, action_id, feedback_type, helpful, rating, comment
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (feedback_id, event_id, action_id, feedback_type, helpful, rating, comment))
        
        await self.db.commit()
        logger.debug(f"Stored user feedback: {feedback_id}")
    
    async def store_health_metrics(self, health_data: Dict[str, Any]):
        """Store system health metrics"""
        
        timestamp = datetime.utcnow()
        
        for component, value in health_data.items():
            metric_id = f"health_{component}_{int(timestamp.timestamp())}"
            
            # Determine status based on value type
            status = "healthy"
            metric_value = None
            
            if isinstance(value, bool):
                status = "healthy" if value else "critical"
                metric_value = 1.0 if value else 0.0
            elif isinstance(value, (int, float)):
                metric_value = float(value)
                status = "healthy"
            
            await self.db.execute('''
                INSERT INTO health_metrics (
                    id, component, metric_name, metric_value, status, details
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                metric_id,
                component,
                component,
                metric_value,
                status,
                json.dumps({'original_value': value}) if not isinstance(value, (bool, int, float)) else None
            ))
        
        await self.db.commit()
        logger.debug(f"Stored health metrics: {len(health_data)} components")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        
        stats = {}
        
        # Event statistics
        cursor = await self.db.execute('''
            SELECT 
                COUNT(*) as total_events,
                COUNT(CASE WHEN severity = 'CRITICAL' THEN 1 END) as critical_events,
                COUNT(CASE WHEN severity = 'IMPORTANT' THEN 1 END) as important_events,
                COUNT(CASE WHEN requires_action = 1 THEN 1 END) as actionable_events
            FROM events
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        event_stats = await cursor.fetchone()
        
        stats['events'] = {
            'total_last_7_days': event_stats[0],
            'critical_last_7_days': event_stats[1],
            'important_last_7_days': event_stats[2],
            'actionable_last_7_days': event_stats[3]
        }
        
        # Action statistics
        cursor = await self.db.execute('''
            SELECT 
                COUNT(*) as total_actions,
                COUNT(CASE WHEN success = 1 THEN 1 END) as successful_actions,
                AVG(rep_score) as avg_rep_score,
                COUNT(CASE WHEN human_validation_needed = 1 THEN 1 END) as human_validation_needed
            FROM action_results
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        action_stats = await cursor.fetchone()
        
        stats['actions'] = {
            'total_last_7_days': action_stats[0] or 0,
            'successful_last_7_days': action_stats[1] or 0,
            'avg_rep_score': round(action_stats[2] or 0, 3),
            'human_validation_needed': action_stats[3] or 0
        }
        
        # Notification statistics
        cursor = await self.db.execute('''
            SELECT 
                COUNT(*) as total_notifications,
                COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent_notifications,
                COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_notifications
            FROM notifications
            WHERE sent_at > datetime('now', '-7 days')
        ''')
        notif_stats = await cursor.fetchone()
        
        stats['notifications'] = {
            'total_last_7_days': notif_stats[0] or 0,
            'sent_last_7_days': notif_stats[1] or 0,
            'delivered_last_7_days': notif_stats[2] or 0
        }
        
        # Learning statistics
        cursor = await self.db.execute('''
            SELECT 
                COUNT(*) as total_feedback,
                COUNT(CASE WHEN helpful = 1 THEN 1 END) as positive_feedback,
                AVG(CASE WHEN rating IS NOT NULL THEN rating END) as avg_rating
            FROM user_feedback
            WHERE timestamp > datetime('now', '-30 days')
        ''')
        feedback_stats = await cursor.fetchone()
        
        stats['learning'] = {
            'total_feedback_30_days': feedback_stats[0] or 0,
            'positive_feedback_30_days': feedback_stats[1] or 0,
            'avg_rating': round(feedback_stats[2] or 0, 1)
        }
        
        # System uptime (approximate from health metrics)
        cursor = await self.db.execute('''
            SELECT MIN(timestamp) as earliest_health_check
            FROM health_metrics
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        uptime_result = await cursor.fetchone()
        
        if uptime_result[0]:
            earliest = datetime.fromisoformat(uptime_result[0])
            uptime_hours = (datetime.utcnow() - earliest).total_seconds() / 3600
            stats['system'] = {
                'uptime_hours': round(uptime_hours, 1)
            }
        else:
            stats['system'] = {'uptime_hours': 0}
        
        return stats
    
    async def get_events(self, limit: int = 100, offset: int = 0, 
                        event_type: Optional[str] = None, severity: Optional[str] = None) -> List[Event]:
        """Get events with optional filtering"""
        
        query = '''
            SELECT id, source, type, title, description, severity, 
                   timestamp, data, requires_action, suggested_actions
            FROM events
        '''
        params = []
        conditions = []
        
        if event_type:
            conditions.append('type = ?')
            params.append(event_type)
        
        if severity:
            conditions.append('severity = ?')
            params.append(severity)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor = await self.db.execute(query, params)
        rows = await cursor.fetchall()
        
        events = []
        for row in rows:
            event = Event(
                id=row[0],
                source=row[1],
                type=row[2],
                title=row[3],
                description=row[4],
                severity=row[5],
                timestamp=datetime.fromisoformat(row[6]),
                data=json.loads(row[7]) if row[7] else {},
                requires_action=bool(row[8]),
                suggested_actions=json.loads(row[9]) if row[9] else []
            )
            events.append(event)
        
        return events
    
    async def get_learning_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get data for machine learning"""
        
        # Get notification feedback patterns
        cursor = await self.db.execute('''
            SELECT e.type, e.severity, e.source, f.helpful, f.rating
            FROM user_feedback f
            JOIN events e ON f.event_id = e.id
            WHERE f.feedback_type = 'notification'
            AND f.timestamp > datetime('now', '-90 days')
        ''')
        notification_feedback = await cursor.fetchall()
        
        # Get action feedback patterns
        cursor = await self.db.execute('''
            SELECT ar.action_type, ar.rep_score, f.helpful, f.rating
            FROM user_feedback f
            JOIN action_results ar ON f.action_id = ar.action_id
            WHERE f.feedback_type = 'action'
            AND f.timestamp > datetime('now', '-90 days')
        ''')
        action_feedback = await cursor.fetchall()
        
        return {
            'notification_patterns': [
                {
                    'event_type': row[0],
                    'severity': row[1],
                    'source': row[2],
                    'helpful': bool(row[3]),
                    'rating': row[4]
                } for row in notification_feedback
            ],
            'action_patterns': [
                {
                    'action_type': row[0],
                    'rep_score': row[1],
                    'helpful': bool(row[2]),
                    'rating': row[3]
                } for row in action_feedback
            ]
        }
    
    async def store_learning_pattern(self, pattern_type: str, pattern_data: Dict[str, Any], 
                                   confidence_score: float):
        """Store a learned pattern"""
        
        pattern_id = str(uuid.uuid4())
        
        await self.db.execute('''
            INSERT INTO learning_patterns (
                id, pattern_type, pattern_data, confidence_score
            ) VALUES (?, ?, ?, ?)
        ''', (pattern_id, pattern_type, json.dumps(pattern_data), confidence_score))
        
        await self.db.commit()
        logger.debug(f"Stored learning pattern: {pattern_id}")
    
    async def get_learning_patterns(self, pattern_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get stored learning patterns"""
        
        if pattern_type:
            cursor = await self.db.execute('''
                SELECT pattern_data, confidence_score, times_applied, success_rate
                FROM learning_patterns
                WHERE pattern_type = ?
                ORDER BY confidence_score DESC
            ''', (pattern_type,))
        else:
            cursor = await self.db.execute('''
                SELECT pattern_type, pattern_data, confidence_score, times_applied, success_rate
                FROM learning_patterns
                ORDER BY confidence_score DESC
            ''')
        
        rows = await cursor.fetchall()
        
        patterns = []
        for row in rows:
            if pattern_type:
                pattern = {
                    'data': json.loads(row[0]),
                    'confidence': row[1],
                    'times_applied': row[2],
                    'success_rate': row[3]
                }
            else:
                pattern = {
                    'type': row[0],
                    'data': json.loads(row[1]),
                    'confidence': row[2],
                    'times_applied': row[3],
                    'success_rate': row[4]
                }
            patterns.append(pattern)
        
        return patterns
    
    async def health_check(self) -> bool:
        """Check database health"""
        
        try:
            # Test basic database connectivity
            cursor = await self.db.execute('SELECT 1')
            result = await cursor.fetchone()
            
            if result[0] == 1:
                logger.debug("Database health check passed")
                return True
            else:
                logger.error("Database health check failed: unexpected result")
                return False
        
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def close(self):
        """Close database connection"""
        
        if self.db:
            await self.db.close()
            logger.info("Database connection closed")

# Testing and utilities
async def test_database():
    """Test database functionality"""
    
    print("🗄️  Testing PADA Database")
    print("=" * 40)
    
    # Initialize test database
    db = PADADatabase("test_pada.db")
    await db.initialize()
    
    # Test event storage
    test_event = Event(
        id="test_event_1",
        source="test",
        type="test_event",
        title="Test Event",
        description="This is a test event",
        severity="HELPFUL",
        timestamp=datetime.utcnow(),
        data={"test": True},
        requires_action=False,
        suggested_actions=[]
    )
    
    await db.store_event(test_event)
    print("✅ Event storage test passed")
    
    # Test statistics
    stats = await db.get_statistics()
    print(f"📊 Statistics: {stats}")
    
    # Test health check
    health = await db.health_check()
    print(f"🏥 Health check: {'✅ Healthy' if health else '❌ Issues'}")
    
    # Cleanup
    await db.close()
    
    # Remove test database
    import os
    if os.path.exists("test_pada.db"):
        os.remove("test_pada.db")
    
    print("✅ Database test complete")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_database())