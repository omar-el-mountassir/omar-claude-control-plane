#!/usr/bin/env python3
"""
PADA Configuration Management
Centralized configuration system for Personal AI Development Assistant
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class REPConfig:
    """REP system configuration"""
    min_score: float = 0.7
    max_bias_count: int = 2
    require_uncertainty: bool = False
    rep_module_path: str = "infrastructure/modules/operations/rationality"

@dataclass 
class GitHubConfig:
    """GitHub monitoring configuration"""
    token: Optional[str] = None
    repositories: list = None
    poll_interval_seconds: int = 300  # 5 minutes
    max_events_per_poll: int = 50
    
    def __post_init__(self):
        if self.repositories is None:
            self.repositories = []

@dataclass
class NotificationConfig:
    """Notification system configuration"""
    enabled: bool = True
    channels: list = None
    severity_filters: Dict[str, bool] = None
    quiet_hours: Dict[str, str] = None
    max_notifications_per_hour: int = 10
    
    def __post_init__(self):
        if self.channels is None:
            self.channels = ["console", "desktop"]
        if self.severity_filters is None:
            self.severity_filters = {
                "CRITICAL": True,
                "IMPORTANT": True, 
                "HELPFUL": True,
                "LEARNING": False
            }
        if self.quiet_hours is None:
            self.quiet_hours = {"start": "22:00", "end": "08:00"}

@dataclass
class ActionConfig:
    """Autonomous action configuration"""
    enabled: bool = True
    max_actions_per_hour: int = 5
    require_confirmation: list = None
    auto_approve: list = None
    
    def __post_init__(self):
        if self.require_confirmation is None:
            self.require_confirmation = [
                "merge_pr", "delete_branch", "update_dependencies"
            ]
        if self.auto_approve is None:
            self.auto_approve = [
                "format_code", "fix_linting", "backup_config"
            ]

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = "sqlite:///pada.db"
    max_connections: int = 10
    connection_timeout: int = 30
    enable_logging: bool = False

@dataclass
class LearningConfig:
    """Machine learning configuration"""
    enabled: bool = True
    update_interval_hours: int = 24
    min_samples_for_training: int = 50
    model_persistence_path: str = "pada_models/"

class PADAConfig:
    """Main PADA configuration manager"""
    
    def __init__(self):
        # Core configuration
        self.service_name = "PADA"
        self.version = "1.0.0"
        self.debug = False
        
        # Component configurations
        self.rep_config = REPConfig()
        self.github_config = GitHubConfig()
        self.notification_config = NotificationConfig()
        self.action_config = ActionConfig()
        self.database_config = DatabaseConfig()
        self.learning_config = LearningConfig()
        
        # Service timing
        self.polling_interval = 60  # seconds
        self.health_check_interval = 300  # 5 minutes
        self.learning_update_interval = 86400  # 24 hours
        
        # Decision thresholds
        self.action_threshold = 0.7  # Minimum REP score for autonomous actions
        self.notification_threshold = 0.0  # All events get considered for notification
        
        # Logging configuration
        self.log_level = "INFO"
        self.log_file = "pada.log"
        self.log_max_size_mb = 10
        self.log_backup_count = 5
    
    @property
    def database_url(self) -> str:
        """Database URL for database initialization"""
        return self.database_config.url
    
    @classmethod
    def load(cls, config_path: str = "pada_config.json") -> 'PADAConfig':
        """Load configuration from JSON file with defaults"""
        
        config = cls()
        config_file = Path(config_path)
        
        if config_file.exists():
            try:
                logger.info(f"Loading PADA configuration from {config_path}")
                
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Update configuration from file
                config._update_from_dict(config_data)
                
                logger.info("PADA configuration loaded successfully")
                
            except Exception as e:
                logger.error(f"Error loading configuration from {config_path}: {e}")
                logger.info("Using default configuration")
        else:
            logger.info(f"Configuration file {config_path} not found, using defaults")
            
            # Create default configuration file
            try:
                config.save(config_path)
                logger.info(f"Created default configuration file at {config_path}")
            except Exception as e:
                logger.warning(f"Could not create default configuration file: {e}")
        
        # Validate configuration
        config._validate()
        
        return config
    
    def _update_from_dict(self, config_data: Dict[str, Any]):
        """Update configuration from dictionary"""
        
        # Core settings
        self.debug = config_data.get('debug', self.debug)
        self.polling_interval = config_data.get('polling_interval', self.polling_interval)
        self.health_check_interval = config_data.get('health_check_interval', self.health_check_interval)
        self.learning_update_interval = config_data.get('learning_update_interval', self.learning_update_interval)
        self.action_threshold = config_data.get('action_threshold', self.action_threshold)
        self.notification_threshold = config_data.get('notification_threshold', self.notification_threshold)
        self.log_level = config_data.get('log_level', self.log_level)
        self.log_file = config_data.get('log_file', self.log_file)
        
        # Component configurations
        if 'rep' in config_data:
            self._update_rep_config(config_data['rep'])
        
        if 'github' in config_data:
            self._update_github_config(config_data['github'])
        
        if 'notifications' in config_data:
            self._update_notification_config(config_data['notifications'])
        
        if 'actions' in config_data:
            self._update_action_config(config_data['actions'])
        
        if 'database' in config_data:
            self._update_database_config(config_data['database'])
        
        if 'learning' in config_data:
            self._update_learning_config(config_data['learning'])
    
    def _update_rep_config(self, rep_data: Dict[str, Any]):
        """Update REP configuration"""
        self.rep_config.min_score = rep_data.get('min_score', self.rep_config.min_score)
        self.rep_config.max_bias_count = rep_data.get('max_bias_count', self.rep_config.max_bias_count)
        self.rep_config.require_uncertainty = rep_data.get('require_uncertainty', self.rep_config.require_uncertainty)
        self.rep_config.rep_module_path = rep_data.get('rep_module_path', self.rep_config.rep_module_path)
    
    def _update_github_config(self, github_data: Dict[str, Any]):
        """Update GitHub configuration"""
        self.github_config.token = github_data.get('token', self.github_config.token)
        self.github_config.repositories = github_data.get('repositories', self.github_config.repositories)
        self.github_config.poll_interval_seconds = github_data.get('poll_interval_seconds', self.github_config.poll_interval_seconds)
        self.github_config.max_events_per_poll = github_data.get('max_events_per_poll', self.github_config.max_events_per_poll)
    
    def _update_notification_config(self, notification_data: Dict[str, Any]):
        """Update notification configuration"""
        self.notification_config.enabled = notification_data.get('enabled', self.notification_config.enabled)
        self.notification_config.channels = notification_data.get('channels', self.notification_config.channels)
        self.notification_config.severity_filters = notification_data.get('severity_filters', self.notification_config.severity_filters)
        self.notification_config.quiet_hours = notification_data.get('quiet_hours', self.notification_config.quiet_hours)
        self.notification_config.max_notifications_per_hour = notification_data.get('max_notifications_per_hour', self.notification_config.max_notifications_per_hour)
    
    def _update_action_config(self, action_data: Dict[str, Any]):
        """Update action configuration"""
        self.action_config.enabled = action_data.get('enabled', self.action_config.enabled)
        self.action_config.max_actions_per_hour = action_data.get('max_actions_per_hour', self.action_config.max_actions_per_hour)
        self.action_config.require_confirmation = action_data.get('require_confirmation', self.action_config.require_confirmation)
        self.action_config.auto_approve = action_data.get('auto_approve', self.action_config.auto_approve)
    
    def _update_database_config(self, database_data: Dict[str, Any]):
        """Update database configuration"""
        self.database_config.url = database_data.get('url', self.database_config.url)
        self.database_config.max_connections = database_data.get('max_connections', self.database_config.max_connections)
        self.database_config.connection_timeout = database_data.get('connection_timeout', self.database_config.connection_timeout)
        self.database_config.enable_logging = database_data.get('enable_logging', self.database_config.enable_logging)
    
    def _update_learning_config(self, learning_data: Dict[str, Any]):
        """Update learning configuration"""
        self.learning_config.enabled = learning_data.get('enabled', self.learning_config.enabled)
        self.learning_config.update_interval_hours = learning_data.get('update_interval_hours', self.learning_config.update_interval_hours)
        self.learning_config.min_samples_for_training = learning_data.get('min_samples_for_training', self.learning_config.min_samples_for_training)
        self.learning_config.model_persistence_path = learning_data.get('model_persistence_path', self.learning_config.model_persistence_path)
    
    def _validate(self):
        """Validate configuration values"""
        
        # Validate thresholds
        if not 0 <= self.action_threshold <= 1:
            logger.warning(f"Action threshold {self.action_threshold} should be between 0 and 1")
            self.action_threshold = max(0, min(1, self.action_threshold))
        
        if not 0 <= self.notification_threshold <= 1:
            logger.warning(f"Notification threshold {self.notification_threshold} should be between 0 and 1")
            self.notification_threshold = max(0, min(1, self.notification_threshold))
        
        # Validate intervals
        if self.polling_interval < 10:
            logger.warning(f"Polling interval {self.polling_interval} too low, setting to 10 seconds")
            self.polling_interval = 10
        
        if self.health_check_interval < 60:
            logger.warning(f"Health check interval {self.health_check_interval} too low, setting to 60 seconds")
            self.health_check_interval = 60
        
        # Validate REP configuration
        if not 0 <= self.rep_config.min_score <= 1:
            logger.warning(f"REP min score {self.rep_config.min_score} should be between 0 and 1")
            self.rep_config.min_score = max(0, min(1, self.rep_config.min_score))
        
        # Validate GitHub configuration
        if self.github_config.repositories:
            for repo in self.github_config.repositories:
                if not isinstance(repo, dict) or 'owner' not in repo or 'name' not in repo:
                    logger.warning(f"Invalid repository configuration: {repo}")
    
    def save(self, config_path: str = "pada_config.json"):
        """Save current configuration to JSON file"""
        
        config_data = {
            'service_name': self.service_name,
            'version': self.version,
            'debug': self.debug,
            'polling_interval': self.polling_interval,
            'health_check_interval': self.health_check_interval,
            'learning_update_interval': self.learning_update_interval,
            'action_threshold': self.action_threshold,
            'notification_threshold': self.notification_threshold,
            'log_level': self.log_level,
            'log_file': self.log_file,
            'rep': asdict(self.rep_config),
            'github': asdict(self.github_config),
            'notifications': asdict(self.notification_config),
            'actions': asdict(self.action_config),
            'database': asdict(self.database_config),
            'learning': asdict(self.learning_config)
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, default=str)
        
        logger.info(f"Configuration saved to {config_path}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get configuration summary for debugging"""
        
        return {
            'service': f"{self.service_name} v{self.version}",
            'debug_mode': self.debug,
            'polling_interval': f"{self.polling_interval}s",
            'action_threshold': self.action_threshold,
            'github_repos': len(self.github_config.repositories),
            'notifications_enabled': self.notification_config.enabled,
            'actions_enabled': self.action_config.enabled,
            'learning_enabled': self.learning_config.enabled,
            'database_url': self.database_config.url
        }

def create_example_config() -> Dict[str, Any]:
    """Create example configuration for documentation"""
    
    return {
        "service_name": "PADA",
        "version": "1.0.0", 
        "debug": False,
        "polling_interval": 60,
        "health_check_interval": 300,
        "learning_update_interval": 86400,
        "action_threshold": 0.7,
        "notification_threshold": 0.0,
        "log_level": "INFO",
        "log_file": "pada.log",
        "rep": {
            "min_score": 0.7,
            "max_bias_count": 2,
            "require_uncertainty": False,
            "rep_module_path": "infrastructure/modules/operations/rationality"
        },
        "github": {
            "token": "YOUR_GITHUB_TOKEN_HERE",
            "repositories": [
                {
                    "owner": "yourusername",
                    "name": "your-repo",
                    "events": ["push", "pull_request", "workflow_run", "issues"],
                    "priority": "HIGH"
                }
            ],
            "poll_interval_seconds": 300,
            "max_events_per_poll": 50
        },
        "notifications": {
            "enabled": True,
            "channels": ["console", "desktop"],
            "severity_filters": {
                "CRITICAL": True,
                "IMPORTANT": True,
                "HELPFUL": True,
                "LEARNING": False
            },
            "quiet_hours": {
                "start": "22:00",
                "end": "08:00"
            },
            "max_notifications_per_hour": 10
        },
        "actions": {
            "enabled": True,
            "max_actions_per_hour": 5,
            "require_confirmation": [
                "merge_pr", "delete_branch", "update_dependencies"
            ],
            "auto_approve": [
                "format_code", "fix_linting", "backup_config"
            ]
        },
        "database": {
            "url": "sqlite:///pada.db",
            "max_connections": 10,
            "connection_timeout": 30,
            "enable_logging": False
        },
        "learning": {
            "enabled": True,
            "update_interval_hours": 24,
            "min_samples_for_training": 50,
            "model_persistence_path": "pada_models/"
        }
    }

# Testing and CLI
def main():
    """Test configuration system"""
    
    print("🔧 Testing PADA Configuration System")
    print("=" * 50)
    
    # Load configuration
    config = PADAConfig.load("test_pada_config.json")
    
    # Display summary
    summary = config.get_summary()
    print("\n📋 Configuration Summary:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    # Save example configuration
    example_config = create_example_config()
    with open("pada_config_example.json", 'w') as f:
        json.dump(example_config, f, indent=2)
    
    print(f"\n💾 Example configuration saved to pada_config_example.json")
    print(f"📁 Test configuration saved to test_pada_config.json")
    
    print("\n✅ Configuration system test complete")

if __name__ == "__main__":
    main()