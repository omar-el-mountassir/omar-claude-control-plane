#!/usr/bin/env python3
"""
PADA Notification System - Intelligent Multi-Channel Notifications
Handles notifications across console, desktop, file, and webhook channels with learning
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Any
from pathlib import Path
import aiohttp
from dataclasses import dataclass

# Import PADA core types
from .pada_main import Event, ActionResult

logger = logging.getLogger(__name__)

# Optional desktop notifications
try:
    from plyer import notification as desktop_notification
    HAS_DESKTOP_NOTIFICATIONS = True
except ImportError:
    HAS_DESKTOP_NOTIFICATIONS = False
    logger.warning("plyer not available - desktop notifications disabled")

@dataclass
class NotificationDelivery:
    """Record of a notification delivery attempt"""
    event_id: str
    channel: str
    status: str  # sent, failed, filtered
    timestamp: datetime
    reason: Optional[str] = None

class NotificationChannel:
    """Base class for notification channels"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
        self.delivery_count = 0
        self.last_delivery = None
    
    async def send(self, title: str, message: str, severity: str, data: Dict[str, Any] = None) -> bool:
        """Send notification through this channel"""
        raise NotImplementedError
    
    async def health_check(self) -> bool:
        """Check if this channel is healthy"""
        return self.enabled

class ConsoleChannel(NotificationChannel):
    """Console/terminal notifications"""
    
    async def send(self, title: str, message: str, severity: str, data: Dict[str, Any] = None) -> bool:
        try:
            # Color coding for different severities
            colors = {
                'CRITICAL': '\033[91m',  # Red
                'IMPORTANT': '\033[93m', # Yellow
                'HELPFUL': '\033[92m',   # Green
                'LEARNING': '\033[94m'   # Blue
            }
            reset_color = '\033[0m'
            
            color = colors.get(severity, '')
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            print(f"{color}[{timestamp}] {severity} - {title}{reset_color}")
            print(f"  {message}")
            
            if data and self.config.get('show_details', False):
                print(f"  Details: {json.dumps(data, indent=2)}")
            
            print()  # Empty line for readability
            
            self.delivery_count += 1
            self.last_delivery = datetime.utcnow()
            return True
            
        except Exception as e:
            logger.error(f"Console notification failed: {e}")
            return False

class DesktopChannel(NotificationChannel):
    """Desktop system notifications"""
    
    async def send(self, title: str, message: str, severity: str, data: Dict[str, Any] = None) -> bool:
        if not HAS_DESKTOP_NOTIFICATIONS:
            logger.warning("Desktop notifications not available")
            return False
        
        try:
            # Truncate message for desktop notification
            max_length = self.config.get('max_message_length', 200)
            if len(message) > max_length:
                message = message[:max_length-3] + '...'
            
            # Set notification timeout based on severity
            timeout_map = {
                'CRITICAL': 10,
                'IMPORTANT': 7,
                'HELPFUL': 5,
                'LEARNING': 3
            }
            timeout = timeout_map.get(severity, 5)
            
            # Send desktop notification
            desktop_notification.notify(
                title=f"PADA - {title}",
                message=message,
                timeout=timeout,
                app_name='Personal AI Development Assistant'
            )
            
            self.delivery_count += 1
            self.last_delivery = datetime.utcnow()
            return True
            
        except Exception as e:
            logger.error(f"Desktop notification failed: {e}")
            return False

class FileChannel(NotificationChannel):
    """File-based persistent notifications"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.log_file = Path(config.get('log_file', 'pada_notifications.log'))
        
        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    async def send(self, title: str, message: str, severity: str, data: Dict[str, Any] = None) -> bool:
        try:
            timestamp = datetime.utcnow().isoformat()
            
            log_entry = {
                'timestamp': timestamp,
                'severity': severity,
                'title': title,
                'message': message,
                'data': data
            }
            
            # Append to log file
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            self.delivery_count += 1
            self.last_delivery = datetime.utcnow()
            return True
            
        except Exception as e:
            logger.error(f"File notification failed: {e}")
            return False

class WebhookChannel(NotificationChannel):
    """Webhook notifications for external integrations"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.webhook_url = config.get('url')
        self.session = None
    
    async def _ensure_session(self):
        """Ensure HTTP session exists"""
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
    
    async def send(self, title: str, message: str, severity: str, data: Dict[str, Any] = None) -> bool:
        if not self.webhook_url:
            logger.warning("Webhook URL not configured")
            return False
        
        try:
            await self._ensure_session()
            
            payload = {
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'PADA',
                'severity': severity,
                'title': title,
                'message': message,
                'data': data or {}
            }
            
            async with self.session.post(self.webhook_url, json=payload) as response:
                if response.status < 400:
                    self.delivery_count += 1
                    self.last_delivery = datetime.utcnow()
                    return True
                else:
                    logger.error(f"Webhook notification failed: {response.status}")
                    return False
            
        except Exception as e:
            logger.error(f"Webhook notification failed: {e}")
            return False
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

class NotificationManager:
    """Intelligent notification manager with learning and filtering"""
    
    def __init__(self, notification_config: Dict[str, Any]):
        self.config = notification_config
        self.channels = {}
        self.delivery_history = []
        self.rate_limit_window = timedelta(hours=1)
        
        # Initialize channels
        self._initialize_channels()
        
        # Rate limiting
        self.max_notifications_per_hour = self.config.get('max_notifications_per_hour', 10)
        
        # Quiet hours
        quiet_hours = self.config.get('quiet_hours', {})
        self.quiet_start = self._parse_time(quiet_hours.get('start', '22:00'))
        self.quiet_end = self._parse_time(quiet_hours.get('end', '08:00'))
        
        # Severity filtering
        self.severity_filters = self.config.get('severity_filters', {
            'CRITICAL': True,
            'IMPORTANT': True,
            'HELPFUL': True,
            'LEARNING': False
        })
        
        logger.info(f"Notification manager initialized with {len(self.channels)} channels")
    
    def _initialize_channels(self):
        """Initialize notification channels based on configuration"""
        
        channel_configs = self.config.get('channels', ['console'])
        
        for channel_name in channel_configs:
            if isinstance(channel_name, str):
                channel_config = {'enabled': True}
                name = channel_name
            else:
                name = channel_name.get('name')
                channel_config = channel_name
            
            # Create channel instance
            if name == 'console':
                self.channels[name] = ConsoleChannel(name, channel_config)
            elif name == 'desktop':
                self.channels[name] = DesktopChannel(name, channel_config)
            elif name == 'file':
                self.channels[name] = FileChannel(name, channel_config)
            elif name == 'webhook':
                self.channels[name] = WebhookChannel(name, channel_config)
            else:
                logger.warning(f"Unknown notification channel: {name}")
    
    def _parse_time(self, time_str: str) -> time:
        """Parse time string (HH:MM) to time object"""
        try:
            hour, minute = map(int, time_str.split(':'))
            return time(hour, minute)
        except Exception as e:
            logger.error(f"Invalid time format '{time_str}': {e}")
            return time(22, 0)  # Default to 10 PM
    
    def _is_quiet_hours(self) -> bool:
        """Check if current time is within quiet hours"""
        now = datetime.now().time()
        
        if self.quiet_start <= self.quiet_end:
            # Same day quiet hours (e.g., 22:00 to 23:00)
            return self.quiet_start <= now <= self.quiet_end
        else:
            # Overnight quiet hours (e.g., 22:00 to 08:00)
            return now >= self.quiet_start or now <= self.quiet_end
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = datetime.utcnow()
        cutoff = now - self.rate_limit_window
        
        # Count recent notifications
        recent_count = len([
            delivery for delivery in self.delivery_history
            if delivery.timestamp > cutoff and delivery.status == 'sent'
        ])
        
        return recent_count < self.max_notifications_per_hour
    
    def _should_notify(self, severity: str) -> tuple[bool, str]:
        """Determine if notification should be sent based on filters"""
        
        # Check severity filter
        if not self.severity_filters.get(severity, True):
            return False, f"severity {severity} filtered"
        
        # Check quiet hours (except for critical)
        if severity != 'CRITICAL' and self._is_quiet_hours():
            return False, "quiet hours"
        
        # Check rate limit
        if not self._check_rate_limit():
            return False, "rate limit exceeded"
        
        return True, "approved"
    
    async def send_notification(self, event: Event) -> List[NotificationDelivery]:
        """Send notification for an event"""
        
        # Check if we should notify
        should_notify, reason = self._should_notify(event.severity)
        
        if not should_notify:
            # Record filtered notification
            delivery = NotificationDelivery(
                event_id=event.id,
                channel="filter",
                status="filtered",
                timestamp=datetime.utcnow(),
                reason=reason
            )
            self.delivery_history.append(delivery)
            logger.debug(f"Notification filtered: {reason}")
            return [delivery]
        
        # Prepare notification content
        title = f"{event.source.upper()}: {event.title}"
        message = event.description
        
        # Send to all enabled channels
        deliveries = []
        
        for channel_name, channel in self.channels.items():
            if not channel.enabled:
                continue
            
            try:
                success = await channel.send(title, message, event.severity, event.data)
                
                delivery = NotificationDelivery(
                    event_id=event.id,
                    channel=channel_name,
                    status="sent" if success else "failed",
                    timestamp=datetime.utcnow(),
                    reason=None if success else "channel_error"
                )
                
                deliveries.append(delivery)
                self.delivery_history.append(delivery)
                
                if success:
                    logger.debug(f"Notification sent via {channel_name}: {event.title}")
                
            except Exception as e:
                logger.error(f"Notification channel {channel_name} failed: {e}")
                
                delivery = NotificationDelivery(
                    event_id=event.id,
                    channel=channel_name,
                    status="failed",
                    timestamp=datetime.utcnow(),
                    reason=str(e)
                )
                
                deliveries.append(delivery)
                self.delivery_history.append(delivery)
        
        return deliveries
    
    async def send_action_notification(self, action_result: ActionResult):
        """Send notification about autonomous action result"""
        
        if action_result.success:
            title = f"✅ Action Completed: {action_result.action_type}"
            message = f"Autonomous action '{action_result.action_type}' completed successfully (REP score: {action_result.rep_score:.2f})"
            severity = "HELPFUL"
        else:
            title = f"❌ Action Failed: {action_result.action_type}"
            message = f"Autonomous action '{action_result.action_type}' failed"
            if action_result.human_validation_needed:
                message += " - human review required"
            severity = "IMPORTANT"
        
        # Create synthetic event for notification
        event = Event(
            id=action_result.action_id,
            source="pada_actions",
            type="action_result",
            title=title,
            description=message,
            severity=severity,
            timestamp=action_result.timestamp,
            data=action_result.details,
            requires_action=action_result.human_validation_needed,
            suggested_actions=[]
        )
        
        return await self.send_notification(event)
    
    async def send_human_validation_request(self, event: Event, action_result: ActionResult):
        """Send notification requesting human validation"""
        
        title = f"🤔 Human Review Needed: {event.title}"
        message = f"Action '{action_result.action_type}' needs human validation (REP score: {action_result.rep_score:.2f} below threshold)"
        
        # Create synthetic event for notification
        validation_event = Event(
            id=f"validation_{action_result.action_id}",
            source="pada_validation",
            type="human_validation",
            title=title,
            description=message,
            severity="IMPORTANT",
            timestamp=datetime.utcnow(),
            data={
                'original_event': event.id,
                'action_id': action_result.action_id,
                'action_type': action_result.action_type,
                'rep_score': action_result.rep_score,
                'reason': action_result.details.get('reason', 'Unknown')
            },
            requires_action=True,
            suggested_actions=['review_action']
        )
        
        return await self.send_notification(validation_event)
    
    async def health_check(self) -> bool:
        """Check notification system health"""
        
        try:
            healthy_channels = 0
            total_channels = len(self.channels)
            
            for channel_name, channel in self.channels.items():
                try:
                    health = await channel.health_check()
                    if health:
                        healthy_channels += 1
                    else:
                        logger.warning(f"Notification channel {channel_name} unhealthy")
                except Exception as e:
                    logger.error(f"Health check failed for channel {channel_name}: {e}")
            
            # Consider healthy if at least one channel is working
            health_status = healthy_channels > 0
            
            logger.debug(f"Notification health: {healthy_channels}/{total_channels} channels healthy")
            return health_status
            
        except Exception as e:
            logger.error(f"Notification health check failed: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get notification statistics"""
        
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)
        
        # Count deliveries by time period
        hour_deliveries = [d for d in self.delivery_history if d.timestamp > last_hour]
        day_deliveries = [d for d in self.delivery_history if d.timestamp > last_day]
        
        # Count by status
        hour_sent = len([d for d in hour_deliveries if d.status == 'sent'])
        hour_failed = len([d for d in hour_deliveries if d.status == 'failed'])
        hour_filtered = len([d for d in hour_deliveries if d.status == 'filtered'])
        
        day_sent = len([d for d in day_deliveries if d.status == 'sent'])
        day_failed = len([d for d in day_deliveries if d.status == 'failed'])
        day_filtered = len([d for d in day_deliveries if d.status == 'filtered'])
        
        # Channel statistics
        channel_stats = {}
        for name, channel in self.channels.items():
            channel_stats[name] = {
                'enabled': channel.enabled,
                'delivery_count': channel.delivery_count,
                'last_delivery': channel.last_delivery.isoformat() if channel.last_delivery else None
            }
        
        return {
            'last_hour': {
                'sent': hour_sent,
                'failed': hour_failed,
                'filtered': hour_filtered,
                'total': len(hour_deliveries)
            },
            'last_day': {
                'sent': day_sent,
                'failed': day_failed,
                'filtered': day_filtered,
                'total': len(day_deliveries)
            },
            'channels': channel_stats,
            'rate_limit': {
                'max_per_hour': self.max_notifications_per_hour,
                'current_hour_count': hour_sent
            },
            'quiet_hours': {
                'start': self.quiet_start.strftime('%H:%M'),
                'end': self.quiet_end.strftime('%H:%M'),
                'is_quiet_now': self._is_quiet_hours()
            }
        }
    
    async def close(self):
        """Close notification manager and cleanup resources"""
        
        for channel in self.channels.values():
            if hasattr(channel, 'close'):
                await channel.close()
        
        logger.info("Notification manager closed")

# Testing
async def test_notification_system():
    """Test notification system functionality"""
    
    print("🔔 Testing PADA Notification System")
    print("=" * 50)
    
    # Test configuration
    test_config = {
        'enabled': True,
        'channels': [
            'console',
            {'name': 'desktop', 'enabled': HAS_DESKTOP_NOTIFICATIONS},
            {'name': 'file', 'log_file': 'test_notifications.log'}
        ],
        'severity_filters': {
            'CRITICAL': True,
            'IMPORTANT': True,
            'HELPFUL': True,
            'LEARNING': False
        },
        'quiet_hours': {'start': '22:00', 'end': '08:00'},
        'max_notifications_per_hour': 10
    }
    
    # Initialize notification manager
    manager = NotificationManager(test_config)
    
    try:
        # Test health check
        health = await manager.health_check()
        print(f"🏥 Health check: {'✅ Healthy' if health else '❌ Issues'}")
        
        # Test notification
        test_event = Event(
            id="test_notification",
            source="test",
            type="test_event",
            title="Test Notification",
            description="This is a test notification to verify the system works correctly.",
            severity="HELPFUL",
            timestamp=datetime.utcnow(),
            data={"test": True},
            requires_action=False,
            suggested_actions=[]
        )
        
        deliveries = await manager.send_notification(test_event)
        print(f"📤 Sent {len(deliveries)} notifications:")
        
        for delivery in deliveries:
            status_icon = "✅" if delivery.status == "sent" else "❌" if delivery.status == "failed" else "🔇"
            print(f"   {status_icon} {delivery.channel}: {delivery.status}")
        
        # Get statistics
        stats = manager.get_statistics()
        print(f"📊 Statistics: Sent {stats['last_hour']['sent']}, Filtered {stats['last_hour']['filtered']}")
        
        # Cleanup
        await manager.close()
        
        # Remove test log file
        import os
        if os.path.exists('test_notifications.log'):
            os.remove('test_notifications.log')
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        await manager.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_notification_system())