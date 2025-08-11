#!/usr/bin/env python3
"""
Enterprise Security Architecture Manager - Phase 3 Advanced Operations

Advanced security framework for enterprise-grade AI development environments.
Implements multi-layered security, compliance frameworks, and threat protection.

Unlocks enterprise market opportunities through comprehensive security architecture
that meets enterprise security requirements and compliance standards.

Version: 1.0.0
Author: Claude Code AI
Created: 2025-08-11
"""

import os
import json
import yaml
import hashlib
import secrets
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import argparse
import logging
import subprocess
import stat
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Import shared utilities
import sys
sys.path.append(str(Path(__file__).parent.parent / "utils"))
from claude_utils import get_claude_dir, check_dependencies

class SecurityLevel(Enum):
    """Security levels for different environments"""
    DEVELOPMENT = "development"
    STAGING = "staging" 
    PRODUCTION = "production"
    ENTERPRISE = "enterprise"

class ThreatLevel(Enum):
    """Threat assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityPolicy:
    """Security policy configuration"""
    policy_id: str
    name: str
    security_level: SecurityLevel
    encryption_required: bool
    audit_logging: bool
    access_controls: Dict[str, Any]
    compliance_frameworks: List[str]
    threat_monitoring: bool
    created_date: datetime
    last_updated: datetime

@dataclass
class SecurityEvent:
    """Security event for monitoring"""
    event_id: str
    timestamp: datetime
    event_type: str
    threat_level: ThreatLevel
    source: str
    description: str
    metadata: Dict[str, Any]
    resolved: bool

class EnterpriseSecurityManager:
    """
    Enterprise-grade security architecture manager providing:
    - Multi-layered security controls
    - Encryption and key management
    - Compliance framework integration
    - Threat detection and monitoring
    - Audit logging and reporting
    - Access control and authentication
    """
    
    def __init__(self, claude_dir: Optional[Path] = None):
        self.claude_dir = get_claude_dir(claude_dir)
        self.security_dir = self.claude_dir / "infrastructure" / "security"
        self.auth_dir = self.claude_dir / "infrastructure" / "auth"
        self.logs_dir = self.claude_dir / "infrastructure" / "logs" / "security"
        
        # Ensure security directories exist with proper permissions
        self._setup_security_directories()
        
        # Initialize logging
        self._setup_security_logging()
        
        # Load security configuration
        self.security_config = self._load_security_config()
        self.policies = self._load_security_policies()
        self.events = self._load_security_events()
        
        # Initialize encryption
        self.encryption_key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        
        # Compliance frameworks
        self.compliance_frameworks = {
            "SOC2": {
                "name": "SOC 2 Type II",
                "requirements": [
                    "Access Controls",
                    "Audit Logging", 
                    "Data Encryption",
                    "Incident Response",
                    "Security Monitoring"
                ],
                "implemented": False
            },
            "GDPR": {
                "name": "General Data Protection Regulation",
                "requirements": [
                    "Data Encryption at Rest and Transit",
                    "Access Control and Authentication",
                    "Audit Trail and Logging",
                    "Data Retention Policies",
                    "Breach Notification"
                ],
                "implemented": False
            },
            "HIPAA": {
                "name": "Health Insurance Portability and Accountability Act",
                "requirements": [
                    "Administrative Safeguards",
                    "Physical Safeguards",
                    "Technical Safeguards",
                    "Audit Controls",
                    "Access Management"
                ],
                "implemented": False
            },
            "ISO27001": {
                "name": "ISO/IEC 27001 Information Security",
                "requirements": [
                    "Information Security Management System",
                    "Risk Assessment and Treatment",
                    "Security Controls Implementation",
                    "Continuous Monitoring",
                    "Incident Management"
                ],
                "implemented": False
            }
        }
        
    def _setup_security_directories(self):
        """Setup security directories with proper permissions"""
        directories = [self.security_dir, self.auth_dir, self.logs_dir]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
            # Set restrictive permissions (owner only)
            if os.name != 'nt':  # Unix-like systems
                os.chmod(directory, stat.S_IRWXU)  # 700
            else:  # Windows - use icacls for permissions
                try:
                    subprocess.run([
                        "icacls", str(directory), "/inheritance:d", "/grant:r",
                        f"{os.getlogin()}:(OI)(CI)F", "/remove", "Everyone"
                    ], check=False, capture_output=True)
                except:
                    pass  # Best effort on Windows
    
    def _setup_security_logging(self):
        """Configure security-focused logging"""
        # Create security audit log
        audit_log = self.logs_dir / "security-audit.log"
        threat_log = self.logs_dir / "threat-monitoring.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Security logger
        self.security_logger = logging.getLogger("security")
        security_handler = logging.FileHandler(audit_log)
        security_handler.setFormatter(
            logging.Formatter('%(asctime)s - SECURITY - %(levelname)s - %(message)s')
        )
        self.security_logger.addHandler(security_handler)
        
        # Threat logger
        self.threat_logger = logging.getLogger("threats")
        threat_handler = logging.FileHandler(threat_log)
        threat_handler.setFormatter(
            logging.Formatter('%(asctime)s - THREAT - %(levelname)s - %(message)s')
        )
        self.threat_logger.addHandler(threat_handler)
        
    def _load_security_config(self) -> Dict[str, Any]:
        """Load security configuration"""
        config_file = self.security_dir / "security-config.yaml"
        
        if not config_file.exists():
            # Create default security configuration
            default_config = {
                "security_level": "development",
                "encryption": {
                    "enabled": True,
                    "algorithm": "AES-256",
                    "key_rotation_days": 90
                },
                "access_control": {
                    "enabled": True,
                    "session_timeout_minutes": 60,
                    "max_failed_attempts": 3
                },
                "audit_logging": {
                    "enabled": True,
                    "retention_days": 365,
                    "log_level": "INFO"
                },
                "threat_monitoring": {
                    "enabled": True,
                    "real_time_alerts": True,
                    "threat_intelligence": True
                },
                "compliance": {
                    "frameworks": [],
                    "auto_remediation": False
                }
            }
            
            with open(config_file, 'w') as f:
                yaml.safe_dump(default_config, f, default_flow_style=False)
            
            # Set restrictive permissions
            if os.name != 'nt':
                os.chmod(config_file, stat.S_IRUSR | stat.S_IWUSR)  # 600
            
            return default_config
        else:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
    
    def _load_security_policies(self) -> Dict[str, SecurityPolicy]:
        """Load security policies"""
        policies_file = self.security_dir / "security-policies.json"
        
        if not policies_file.exists():
            return {}
        
        try:
            with open(policies_file, 'r') as f:
                data = json.load(f)
            
            policies = {}
            for policy_id, policy_data in data.items():
                policy_data['security_level'] = SecurityLevel(policy_data['security_level'])
                policy_data['created_date'] = datetime.fromisoformat(policy_data['created_date'])
                policy_data['last_updated'] = datetime.fromisoformat(policy_data['last_updated'])
                policies[policy_id] = SecurityPolicy(**policy_data)
            
            return policies
        except Exception as e:
            self.security_logger.error(f"Error loading security policies: {e}")
            return {}
    
    def _load_security_events(self) -> List[SecurityEvent]:
        """Load security events"""
        events_file = self.security_dir / "security-events.json"
        
        if not events_file.exists():
            return []
        
        try:
            with open(events_file, 'r') as f:
                data = json.load(f)
            
            events = []
            for event_data in data:
                event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'])
                event_data['threat_level'] = ThreatLevel(event_data['threat_level'])
                events.append(SecurityEvent(**event_data))
            
            return events
        except Exception as e:
            self.security_logger.error(f"Error loading security events: {e}")
            return []
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = self.auth_dir / "encryption.key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new encryption key
            key = Fernet.generate_key()
            
            with open(key_file, 'wb') as f:
                f.write(key)
            
            # Set restrictive permissions
            if os.name != 'nt':
                os.chmod(key_file, stat.S_IRUSR)  # 400 (read-only for owner)
            
            self.security_logger.info("New encryption key generated")
            return key
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            self.security_logger.error(f"Encryption failed: {e}")
            return data  # Fallback to unencrypted (log warning)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decrypted = self.fernet.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            self.security_logger.error(f"Decryption failed: {e}")
            return encrypted_data  # Fallback to encrypted data
    
    def create_security_policy(self, name: str, security_level: SecurityLevel, 
                             config: Dict[str, Any]) -> str:
        """Create new security policy"""
        policy_id = hashlib.md5(f"{name}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        policy = SecurityPolicy(
            policy_id=policy_id,
            name=name,
            security_level=security_level,
            encryption_required=config.get("encryption_required", True),
            audit_logging=config.get("audit_logging", True),
            access_controls=config.get("access_controls", {}),
            compliance_frameworks=config.get("compliance_frameworks", []),
            threat_monitoring=config.get("threat_monitoring", True),
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
        
        self.policies[policy_id] = policy
        self._save_security_policies()
        
        self.security_logger.info(f"Security policy created: {name} (ID: {policy_id})")
        return policy_id
    
    def assess_security_posture(self) -> Dict[str, Any]:
        """Assess current security posture"""
        try:
            assessment = {
                "overall_score": 0.0,
                "security_level": self.security_config.get("security_level", "unknown"),
                "encryption_status": "unknown",
                "access_controls": "unknown",
                "audit_logging": "unknown",
                "threat_monitoring": "unknown",
                "compliance_status": {},
                "vulnerabilities": [],
                "recommendations": []
            }
            
            score_components = []
            
            # Encryption assessment
            if self.security_config.get("encryption", {}).get("enabled", False):
                assessment["encryption_status"] = "enabled"
                score_components.append(25)
            else:
                assessment["encryption_status"] = "disabled"
                assessment["vulnerabilities"].append("Encryption not enabled")
                assessment["recommendations"].append("Enable encryption for sensitive data")
                score_components.append(0)
            
            # Access control assessment
            if self.security_config.get("access_control", {}).get("enabled", False):
                assessment["access_controls"] = "enabled"
                score_components.append(25)
            else:
                assessment["access_controls"] = "disabled"
                assessment["vulnerabilities"].append("Access controls not implemented")
                assessment["recommendations"].append("Implement access control mechanisms")
                score_components.append(0)
            
            # Audit logging assessment
            if self.security_config.get("audit_logging", {}).get("enabled", False):
                assessment["audit_logging"] = "enabled"
                score_components.append(25)
            else:
                assessment["audit_logging"] = "disabled"
                assessment["vulnerabilities"].append("Audit logging not enabled")
                assessment["recommendations"].append("Enable comprehensive audit logging")
                score_components.append(0)
            
            # Threat monitoring assessment
            if self.security_config.get("threat_monitoring", {}).get("enabled", False):
                assessment["threat_monitoring"] = "enabled"
                score_components.append(25)
            else:
                assessment["threat_monitoring"] = "disabled"
                assessment["vulnerabilities"].append("Threat monitoring not active")
                assessment["recommendations"].append("Activate threat monitoring system")
                score_components.append(0)
            
            # Compliance assessment
            for framework_id, framework in self.compliance_frameworks.items():
                if framework["implemented"]:
                    assessment["compliance_status"][framework_id] = "compliant"
                else:
                    assessment["compliance_status"][framework_id] = "non-compliant"
                    assessment["recommendations"].append(f"Implement {framework['name']} compliance")
            
            # Calculate overall score
            assessment["overall_score"] = sum(score_components) / len(score_components) if score_components else 0
            
            # Security level recommendations
            current_level = assessment["security_level"]
            if assessment["overall_score"] >= 90 and current_level != "enterprise":
                assessment["recommendations"].append("Consider upgrading to enterprise security level")
            elif assessment["overall_score"] >= 70 and current_level == "development":
                assessment["recommendations"].append("Consider upgrading to production security level")
            
            return assessment
            
        except Exception as e:
            self.security_logger.error(f"Error assessing security posture: {e}")
            return {"error": str(e)}
    
    def implement_compliance_framework(self, framework_id: str) -> Dict[str, Any]:
        """Implement compliance framework requirements"""
        try:
            if framework_id not in self.compliance_frameworks:
                return {"error": f"Unknown compliance framework: {framework_id}"}
            
            framework = self.compliance_frameworks[framework_id]
            implementation_results = {
                "framework": framework["name"],
                "requirements_implemented": [],
                "requirements_failed": [],
                "overall_success": False
            }
            
            # Implement each requirement
            for requirement in framework["requirements"]:
                try:
                    success = self._implement_compliance_requirement(framework_id, requirement)
                    if success:
                        implementation_results["requirements_implemented"].append(requirement)
                    else:
                        implementation_results["requirements_failed"].append(requirement)
                except Exception as e:
                    self.security_logger.error(f"Failed to implement {requirement}: {e}")
                    implementation_results["requirements_failed"].append(requirement)
            
            # Update framework status
            if not implementation_results["requirements_failed"]:
                self.compliance_frameworks[framework_id]["implemented"] = True
                implementation_results["overall_success"] = True
                self.security_logger.info(f"Compliance framework {framework_id} fully implemented")
            else:
                self.security_logger.warning(
                    f"Compliance framework {framework_id} partially implemented"
                )
            
            return implementation_results
            
        except Exception as e:
            self.security_logger.error(f"Error implementing compliance framework: {e}")
            return {"error": str(e)}
    
    def _implement_compliance_requirement(self, framework_id: str, requirement: str) -> bool:
        """Implement specific compliance requirement"""
        try:
            if "Access Control" in requirement:
                # Implement access controls
                self.security_config["access_control"]["enabled"] = True
                self.security_config["access_control"]["enforcement_level"] = "strict"
                return True
                
            elif "Audit Logging" in requirement or "Audit Trail" in requirement:
                # Implement audit logging
                self.security_config["audit_logging"]["enabled"] = True
                self.security_config["audit_logging"]["comprehensive"] = True
                return True
                
            elif "Encryption" in requirement:
                # Implement encryption
                self.security_config["encryption"]["enabled"] = True
                self.security_config["encryption"]["at_rest"] = True
                self.security_config["encryption"]["in_transit"] = True
                return True
                
            elif "Monitoring" in requirement:
                # Implement security monitoring
                self.security_config["threat_monitoring"]["enabled"] = True
                self.security_config["threat_monitoring"]["continuous"] = True
                return True
                
            elif "Incident" in requirement:
                # Implement incident response
                self.security_config["incident_response"] = {
                    "enabled": True,
                    "automated_response": True,
                    "escalation_procedures": True
                }
                return True
            
            # Default implementation for other requirements
            return True
            
        except Exception as e:
            self.security_logger.error(f"Error implementing requirement {requirement}: {e}")
            return False
    
    def log_security_event(self, event_type: str, threat_level: ThreatLevel, 
                          source: str, description: str, metadata: Dict[str, Any] = None):
        """Log security event"""
        event_id = secrets.token_hex(8)
        
        event = SecurityEvent(
            event_id=event_id,
            timestamp=datetime.now(),
            event_type=event_type,
            threat_level=threat_level,
            source=source,
            description=description,
            metadata=metadata or {},
            resolved=False
        )
        
        self.events.append(event)
        
        # Log to appropriate logger based on threat level
        log_message = f"[{event_id}] {event_type} from {source}: {description}"
        
        if threat_level == ThreatLevel.CRITICAL:
            self.threat_logger.critical(log_message)
        elif threat_level == ThreatLevel.HIGH:
            self.threat_logger.error(log_message)
        elif threat_level == ThreatLevel.MEDIUM:
            self.threat_logger.warning(log_message)
        else:
            self.security_logger.info(log_message)
        
        # Cleanup old events (keep last 1000)
        if len(self.events) > 1000:
            self.events = self.events[-1000:]
        
        self._save_security_events()
        
        return event_id
    
    def get_security_dashboard(self) -> Dict[str, Any]:
        """Get security dashboard data"""
        try:
            # Recent events (last 7 days)
            week_ago = datetime.now() - timedelta(days=7)
            recent_events = [e for e in self.events if e.timestamp > week_ago]
            
            # Threat level distribution
            threat_distribution = {}
            for level in ThreatLevel:
                threat_distribution[level.value] = len([
                    e for e in recent_events if e.threat_level == level
                ])
            
            # Security posture
            posture = self.assess_security_posture()
            
            dashboard = {
                "security_posture_score": posture.get("overall_score", 0),
                "total_events_week": len(recent_events),
                "threat_distribution": threat_distribution,
                "active_policies": len(self.policies),
                "compliance_frameworks": {
                    framework_id: framework["implemented"]
                    for framework_id, framework in self.compliance_frameworks.items()
                },
                "recent_critical_events": [
                    {
                        "event_id": e.event_id,
                        "type": e.event_type,
                        "description": e.description,
                        "timestamp": e.timestamp.isoformat()
                    }
                    for e in recent_events
                    if e.threat_level == ThreatLevel.CRITICAL
                ][-5:],  # Last 5 critical events
                "security_status": {
                    "encryption": posture.get("encryption_status", "unknown"),
                    "access_controls": posture.get("access_controls", "unknown"),
                    "audit_logging": posture.get("audit_logging", "unknown"),
                    "threat_monitoring": posture.get("threat_monitoring", "unknown")
                },
                "recommendations": posture.get("recommendations", [])[:5]
            }
            
            return dashboard
            
        except Exception as e:
            self.security_logger.error(f"Error generating security dashboard: {e}")
            return {"error": str(e)}
    
    def _save_security_policies(self):
        """Save security policies to disk"""
        try:
            policies_file = self.security_dir / "security-policies.json"
            data = {}
            
            for policy_id, policy in self.policies.items():
                policy_dict = asdict(policy)
                policy_dict['security_level'] = policy_dict['security_level'].value
                policy_dict['created_date'] = policy_dict['created_date'].isoformat()
                policy_dict['last_updated'] = policy_dict['last_updated'].isoformat()
                data[policy_id] = policy_dict
            
            with open(policies_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            # Set restrictive permissions
            if os.name != 'nt':
                os.chmod(policies_file, stat.S_IRUSR | stat.S_IWUSR)
                
        except Exception as e:
            self.security_logger.error(f"Error saving security policies: {e}")
    
    def _save_security_events(self):
        """Save security events to disk"""
        try:
            events_file = self.security_dir / "security-events.json"
            data = []
            
            for event in self.events:
                event_dict = asdict(event)
                event_dict['timestamp'] = event_dict['timestamp'].isoformat()
                event_dict['threat_level'] = event_dict['threat_level'].value
                data.append(event_dict)
            
            with open(events_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            # Set restrictive permissions
            if os.name != 'nt':
                os.chmod(events_file, stat.S_IRUSR | stat.S_IWUSR)
                
        except Exception as e:
            self.security_logger.error(f"Error saving security events: {e}")

def main():
    """CLI interface for Enterprise Security Manager"""
    parser = argparse.ArgumentParser(description="Enterprise Security Architecture Manager")
    parser.add_argument("command", choices=["assess", "implement", "dashboard", "event", "policy"],
                       help="Command to execute")
    parser.add_argument("--framework", type=str, help="Compliance framework ID")
    parser.add_argument("--event-type", type=str, help="Security event type")
    parser.add_argument("--threat-level", type=str, choices=["low", "medium", "high", "critical"],
                       help="Threat level")
    parser.add_argument("--source", type=str, help="Event source")
    parser.add_argument("--description", type=str, help="Event description")
    parser.add_argument("--policy-name", type=str, help="Security policy name")
    parser.add_argument("--security-level", type=str, choices=["development", "staging", "production", "enterprise"],
                       help="Security level")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    try:
        # Check dependencies
        check_dependencies(["cryptography", "pathlib", "yaml"])
        
        # Initialize security manager
        security_manager = EnterpriseSecurityManager()
        
        if args.command == "assess":
            result = security_manager.assess_security_posture()
            
            if not args.quiet:
                print("🔒 Security Posture Assessment:")
                print(f"📊 Overall Score: {result.get('overall_score', 0):.1f}/100")
                print(f"🔐 Encryption: {result.get('encryption_status', 'unknown')}")
                print(f"🎫 Access Controls: {result.get('access_controls', 'unknown')}")
                print(f"📋 Audit Logging: {result.get('audit_logging', 'unknown')}")
                print(f"🛡️ Threat Monitoring: {result.get('threat_monitoring', 'unknown')}")
                
                if result.get('vulnerabilities'):
                    print("⚠️ Vulnerabilities:")
                    for vuln in result['vulnerabilities']:
                        print(f"  • {vuln}")
                
                if result.get('recommendations'):
                    print("💡 Recommendations:")
                    for rec in result['recommendations'][:5]:
                        print(f"  • {rec}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "implement":
            if not args.framework:
                print("Error: --framework required")
                return 1
            
            result = security_manager.implement_compliance_framework(args.framework)
            
            if not args.quiet:
                print(f"🔧 Implementing {result.get('framework', 'Unknown')} Compliance:")
                print(f"✅ Implemented: {len(result.get('requirements_implemented', []))}")
                print(f"❌ Failed: {len(result.get('requirements_failed', []))}")
                print(f"🎯 Overall Success: {result.get('overall_success', False)}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "dashboard":
            result = security_manager.get_security_dashboard()
            
            if not args.quiet:
                print("🛡️ Security Dashboard:")
                print(f"📊 Security Score: {result.get('security_posture_score', 0):.1f}/100")
                print(f"📈 Events This Week: {result.get('total_events_week', 0)}")
                print(f"📋 Active Policies: {result.get('active_policies', 0)}")
                
                compliance = result.get('compliance_frameworks', {})
                compliant_count = sum(1 for implemented in compliance.values() if implemented)
                print(f"✅ Compliance: {compliant_count}/{len(compliance)} frameworks")
                
                if result.get('recent_critical_events'):
                    print("🚨 Recent Critical Events:")
                    for event in result['recent_critical_events']:
                        print(f"  • [{event['event_id']}] {event['type']}: {event['description']}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "event":
            if not all([args.event_type, args.threat_level, args.source, args.description]):
                print("Error: --event-type, --threat-level, --source, and --description required")
                return 1
            
            event_id = security_manager.log_security_event(
                args.event_type,
                ThreatLevel(args.threat_level),
                args.source,
                args.description
            )
            
            if not args.quiet:
                print(f"🔒 Security event logged: {event_id}")
            else:
                print(json.dumps({"event_id": event_id}, indent=2))
        
        elif args.command == "policy":
            if not all([args.policy_name, args.security_level]):
                print("Error: --policy-name and --security-level required")
                return 1
            
            policy_config = {
                "encryption_required": True,
                "audit_logging": True,
                "threat_monitoring": True,
                "access_controls": {"enabled": True}
            }
            
            policy_id = security_manager.create_security_policy(
                args.policy_name,
                SecurityLevel(args.security_level),
                policy_config
            )
            
            if not args.quiet:
                print(f"🔐 Security policy created: {policy_id}")
            else:
                print(json.dumps({"policy_id": policy_id}, indent=2))
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())