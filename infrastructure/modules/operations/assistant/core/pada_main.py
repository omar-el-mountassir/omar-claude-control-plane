#!/usr/bin/env python3
"""
Personal AI Development Assistant (PADA) - Main Service
A practical AI assistant for personal development workflow
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import json

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn

# Import our modules
from .database import PADADatabase
from .rep_integration import REPValidator
from .github_monitor import GitHubMonitor
from .notification_system import NotificationManager
from .learning_engine import PreferenceLearner
from .autonomous_actions import ActionExecutor

# Configuration
from .config import PADAConfig

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Event:
    """Core event structure for PADA"""
    id: str
    source: str
    type: str
    title: str
    description: str
    severity: str  # CRITICAL, IMPORTANT, HELPFUL, LEARNING
    timestamp: datetime
    data: Dict[str, Any]
    requires_action: bool
    suggested_actions: List[str]

@dataclass
class ActionResult:
    """Result of an autonomous action"""
    action_id: str
    action_type: str
    success: bool
    rep_score: float
    human_validation_needed: bool
    details: Dict[str, Any]
    timestamp: datetime

class PADAService:
    """Main PADA service orchestrator"""
    
    def __init__(self, config_path: str = "pada_config.json"):
        self.config = PADAConfig.load(config_path)
        
        # Initialize components
        self.db = PADADatabase(self.config.database_url)
        self.rep_validator = REPValidator(self.config.rep_config)
        self.github_monitor = GitHubMonitor(self.config.github_config)
        self.notification_manager = NotificationManager(self.config.notification_config)
        self.preference_learner = PreferenceLearner(self.db)
        self.action_executor = ActionExecutor(self.config.action_config, self.rep_validator)
        
        # Service state
        self.is_running = False
        self.processed_events = 0
        self.autonomous_actions_taken = 0
        self.startup_time = datetime.utcnow()
        
        logger.info("PADA service initialized")
    
    async def start(self):
        """Start all PADA components"""
        logger.info("Starting PADA service...")
        
        # Initialize database
        await self.db.initialize()
        
        # Start monitoring services
        await self.github_monitor.start()
        
        # Start background tasks
        asyncio.create_task(self.event_processor())
        asyncio.create_task(self.learning_updater())
        asyncio.create_task(self.health_monitor())
        
        self.is_running = True
        logger.info("PADA service started successfully")
    
    async def stop(self):
        """Gracefully stop PADA service"""
        logger.info("Stopping PADA service...")
        
        self.is_running = False
        
        # Stop monitoring services
        await self.github_monitor.stop()
        
        # Close database connections
        await self.db.close()
        
        logger.info("PADA service stopped")
    
    async def process_event(self, event: Event) -> Optional[ActionResult]:
        """Process a single event with REP validation and learning"""
        
        logger.info(f"Processing event: {event.type} - {event.title}")
        
        # Store event
        await self.db.store_event(event)
        self.processed_events += 1
        
        # Check user preferences for notification
        should_notify = await self.preference_learner.should_notify(event)
        
        if should_notify:
            # Send notification
            await self.notification_manager.send_notification(event)
            
            # Track notification for learning
            await self.db.track_notification(event.id, "sent")
        
        # Check if autonomous action is needed and safe
        if event.requires_action and len(event.suggested_actions) > 0:
            action_result = await self.execute_autonomous_action(event)
            return action_result
        
        return None
    
    async def execute_autonomous_action(self, event: Event) -> ActionResult:
        """Execute autonomous action with REP validation"""
        
        action_id = f"action_{event.id}_{datetime.utcnow().isoformat()}"
        
        # Get suggested action
        suggested_action = event.suggested_actions[0]  # Take first suggestion
        
        logger.info(f"Evaluating autonomous action: {suggested_action}")
        
        # Validate action with REP system
        rep_score = await self.rep_validator.validate_action(suggested_action, event.data)
        
        # Decision logic based on REP score
        if rep_score >= self.config.action_threshold:
            # Execute action
            try:
                result = await self.action_executor.execute(suggested_action, event.data)
                
                action_result = ActionResult(
                    action_id=action_id,
                    action_type=suggested_action,
                    success=result['success'],
                    rep_score=rep_score,
                    human_validation_needed=False,
                    details=result,
                    timestamp=datetime.utcnow()
                )
                
                # Store result
                await self.db.store_action_result(action_result)
                self.autonomous_actions_taken += 1
                
                # Notify about successful autonomous action
                await self.notification_manager.send_action_notification(action_result)
                
                logger.info(f"Autonomous action executed successfully: {suggested_action}")
                
            except Exception as e:
                logger.error(f"Autonomous action failed: {e}")
                action_result = ActionResult(
                    action_id=action_id,
                    action_type=suggested_action,
                    success=False,
                    rep_score=rep_score,
                    human_validation_needed=True,
                    details={'error': str(e)},
                    timestamp=datetime.utcnow()
                )
        else:
            # REP score too low - escalate to human
            logger.info(f"REP score too low ({rep_score:.3f}) for autonomous action: {suggested_action}")
            
            action_result = ActionResult(
                action_id=action_id,
                action_type=suggested_action,
                success=False,
                rep_score=rep_score,
                human_validation_needed=True,
                details={'reason': 'REP score below threshold', 'threshold': self.config.action_threshold},
                timestamp=datetime.utcnow()
            )
            
            # Send notification for human review
            await self.notification_manager.send_human_validation_request(event, action_result)
        
        return action_result
    
    async def event_processor(self):
        """Background task to process events continuously"""
        
        while self.is_running:
            try:
                # Check for new events from all sources
                new_events = []
                
                # GitHub events
                github_events = await self.github_monitor.get_new_events()
                new_events.extend(github_events)
                
                # Process each event
                for event in new_events:
                    await self.process_event(event)
                
                # Sleep between checks
                await asyncio.sleep(self.config.polling_interval)
                
            except Exception as e:
                logger.error(f"Error in event processor: {e}")
                await asyncio.sleep(60)  # Longer sleep on error
    
    async def learning_updater(self):
        """Background task to update learning models"""
        
        while self.is_running:
            try:
                # Update preference learning model
                await self.preference_learner.update_model()
                
                # Sleep for learning update interval
                await asyncio.sleep(self.config.learning_update_interval)
                
            except Exception as e:
                logger.error(f"Error in learning updater: {e}")
                await asyncio.sleep(3600)  # 1 hour sleep on error
    
    async def health_monitor(self):
        """Monitor PADA service health"""
        
        while self.is_running:
            try:
                # Check component health
                health_status = {
                    'database': await self.db.health_check(),
                    'github_monitor': await self.github_monitor.health_check(),
                    'notification_manager': await self.notification_manager.health_check(),
                    'processed_events': self.processed_events,
                    'autonomous_actions': self.autonomous_actions_taken,
                    'uptime_hours': (datetime.utcnow() - self.startup_time).total_seconds() / 3600
                }
                
                # Log health status
                logger.info(f"PADA Health: {health_status}")
                
                # Store health metrics
                await self.db.store_health_metrics(health_status)
                
                # Sleep for health check interval
                await asyncio.sleep(self.config.health_check_interval)
                
            except Exception as e:
                logger.error(f"Error in health monitor: {e}")
                await asyncio.sleep(300)  # 5 minute sleep on error

# FastAPI app for REST API and webhooks
app = FastAPI(title="PADA - Personal AI Development Assistant", version="1.0.0")

# Global service instance
pada_service: Optional[PADAService] = None

@app.on_event("startup")
async def startup_event():
    global pada_service
    pada_service = PADAService()
    await pada_service.start()

@app.on_event("shutdown")
async def shutdown_event():
    global pada_service
    if pada_service:
        await pada_service.stop()

# API Endpoints
class EventRequest(BaseModel):
    source: str
    type: str
    title: str
    description: str
    severity: str
    data: Dict[str, Any]
    requires_action: bool = False
    suggested_actions: List[str] = []

@app.post("/events")
async def create_event(event_request: EventRequest, background_tasks: BackgroundTasks):
    """Accept external events"""
    
    if not pada_service:
        raise HTTPException(status_code=503, detail="PADA service not ready")
    
    # Create event
    event = Event(
        id=f"ext_{datetime.utcnow().isoformat()}",
        source=event_request.source,
        type=event_request.type,
        title=event_request.title,
        description=event_request.description,
        severity=event_request.severity,
        timestamp=datetime.utcnow(),
        data=event_request.data,
        requires_action=event_request.requires_action,
        suggested_actions=event_request.suggested_actions
    )
    
    # Process in background
    background_tasks.add_task(pada_service.process_event, event)
    
    return {"status": "accepted", "event_id": event.id}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    if not pada_service:
        raise HTTPException(status_code=503, detail="PADA service not ready")
    
    return {
        "status": "healthy",
        "uptime_hours": (datetime.utcnow() - pada_service.startup_time).total_seconds() / 3600,
        "processed_events": pada_service.processed_events,
        "autonomous_actions": pada_service.autonomous_actions_taken
    }

@app.get("/stats")
async def get_stats():
    """Get PADA statistics"""
    
    if not pada_service:
        raise HTTPException(status_code=503, detail="PADA service not ready")
    
    stats = await pada_service.db.get_statistics()
    return stats

@app.post("/feedback")
async def user_feedback(event_id: str, feedback_type: str, helpful: bool):
    """User feedback for learning"""
    
    if not pada_service:
        raise HTTPException(status_code=503, detail="PADA service not ready")
    
    # Store feedback for learning
    await pada_service.db.store_user_feedback(event_id, feedback_type, helpful)
    
    # Update learning model
    await pada_service.preference_learner.process_feedback(event_id, feedback_type, helpful)
    
    return {"status": "feedback_received", "event_id": event_id}

def main():
    """Run PADA service"""
    
    print("🤖 Starting Personal AI Development Assistant (PADA)")
    print("=" * 60)
    
    # Run the FastAPI application
    uvicorn.run(
        "pada.core.pada_main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()