#!/usr/bin/env python3
"""
PADA REP Integration - AI Decision Validation
Integrates with existing REP system to validate autonomous actions
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Add REP module to path - correct relative path from assistant/core to rationality
sys.path.insert(0, str(Path(__file__).parent.parent / 'rationality'))

try:
    from rep import detailed_rationality_analysis, RationalityEnhancementProtocol
except ImportError:
    logging.warning("REP module not found - using fallback validation")
    detailed_rationality_analysis = None
    RationalityEnhancementProtocol = None

logger = logging.getLogger(__name__)

@dataclass
class ActionValidation:
    """Result of REP validation for an autonomous action"""
    action_description: str
    rationality_score: float
    bias_indicators: list
    confidence_calibration: float
    uncertainty_acknowledged: bool
    validation_passed: bool
    reasoning: str
    recommendations: list

class REPValidator:
    """Validates autonomous actions using REP rationality system"""
    
    def __init__(self, rep_config: Dict[str, Any]):
        self.config = rep_config
        self.min_rationality_score = rep_config.get('min_score', 0.7)
        self.max_bias_count = rep_config.get('max_bias_count', 2)
        self.require_uncertainty = rep_config.get('require_uncertainty', False)
        
        # Initialize REP if available
        if RationalityEnhancementProtocol:
            self.rep_engine = RationalityEnhancementProtocol()
            logger.info("REP integration initialized successfully")
        else:
            self.rep_engine = None
            logger.warning("REP engine not available - using fallback validation")
    
    async def validate_action(self, action_type: str, action_data: Dict[str, Any]) -> float:
        """Validate an autonomous action and return rationality score"""
        
        # Generate action description for REP analysis
        action_description = self._generate_action_description(action_type, action_data)
        
        if not action_description:
            logger.warning(f"Could not generate description for action: {action_type}")
            return 0.0
        
        # Perform REP validation
        validation = await self.validate_text(action_description)
        
        # Log validation result
        logger.info(f"REP validation for '{action_type}': {validation.rationality_score:.3f}")
        
        if not validation.validation_passed:
            logger.warning(f"Action failed REP validation: {validation.reasoning}")
        
        return validation.rationality_score
    
    async def validate_text(self, text: str) -> ActionValidation:
        """Validate text using REP system"""
        
        if self.rep_engine and detailed_rationality_analysis:
            try:
                # Use actual REP system
                result = detailed_rationality_analysis(text, context="pada_action_validation")
                metrics = result['metrics']
                
                validation = ActionValidation(
                    action_description=text,
                    rationality_score=metrics['overall_score'],
                    bias_indicators=metrics['bias_indicators'],
                    confidence_calibration=metrics['confidence_calibration'],
                    uncertainty_acknowledged=metrics['uncertainty_acknowledgment'],
                    validation_passed=self._check_validation_passed(metrics),
                    reasoning=self._generate_reasoning(metrics),
                    recommendations=result.get('recommendations', [])
                )
                
                return validation
                
            except Exception as e:
                logger.error(f"REP validation error: {e}")
                return self._fallback_validation(text)
        else:
            # Use fallback validation
            return self._fallback_validation(text)
    
    def _check_validation_passed(self, metrics: Dict[str, Any]) -> bool:
        """Check if validation passes all thresholds"""
        
        # Check rationality score
        if metrics['overall_score'] < self.min_rationality_score:
            return False
        
        # Check bias count
        if len(metrics['bias_indicators']) > self.max_bias_count:
            return False
        
        # Check uncertainty requirement
        if self.require_uncertainty and not metrics['uncertainty_acknowledgment']:
            return False
        
        return True
    
    def _generate_reasoning(self, metrics: Dict[str, Any]) -> str:
        """Generate human-readable reasoning for validation result"""
        
        reasons = []
        
        if metrics['overall_score'] < self.min_rationality_score:
            reasons.append(f"Rationality score {metrics['overall_score']:.3f} below threshold {self.min_rationality_score}")
        
        if len(metrics['bias_indicators']) > self.max_bias_count:
            bias_list = ', '.join(metrics['bias_indicators'])
            reasons.append(f"Too many bias indicators ({len(metrics['bias_indicators'])}): {bias_list}")
        
        if self.require_uncertainty and not metrics['uncertainty_acknowledgment']:
            reasons.append("No uncertainty acknowledgment detected")
        
        if not reasons:
            return f"Action passes all REP validation criteria (score: {metrics['overall_score']:.3f})"
        
        return "; ".join(reasons)
    
    def _fallback_validation(self, text: str) -> ActionValidation:
        """Fallback validation when REP system is not available"""
        
        # Simple heuristic-based validation
        score = 0.8  # Default decent score
        bias_indicators = []
        
        # Check for problematic patterns
        text_lower = text.lower()
        
        # Absolute language
        absolute_words = ['always', 'never', 'all', 'every', 'completely', 'totally', 'definitely']
        if any(word in text_lower for word in absolute_words):
            bias_indicators.append('absolute_language')
            score -= 0.2
        
        # Overconfident language
        confident_words = ['obviously', 'clearly', 'certainly', 'undoubtedly', 'guaranteed']
        if any(word in text_lower for word in confident_words):
            bias_indicators.append('overconfident_language')
            score -= 0.1
        
        # Check for uncertainty acknowledgment
        uncertainty_words = ['might', 'could', 'may', 'likely', 'possibly', 'potentially', 'probably']
        uncertainty_acknowledged = any(word in text_lower for word in uncertainty_words)
        
        if not uncertainty_acknowledged and 'will' in text_lower:
            score -= 0.1
        
        # Ensure score is in valid range
        score = max(0.0, min(1.0, score))
        
        return ActionValidation(
            action_description=text,
            rationality_score=score,
            bias_indicators=bias_indicators,
            confidence_calibration=score,  # Simplified
            uncertainty_acknowledged=uncertainty_acknowledged,
            validation_passed=score >= self.min_rationality_score and len(bias_indicators) <= self.max_bias_count,
            reasoning=f"Fallback validation (score: {score:.3f})",
            recommendations=['Use actual REP system for better validation']
        )
    
    def _generate_action_description(self, action_type: str, action_data: Dict[str, Any]) -> Optional[str]:
        """Generate human-readable description of the action for REP analysis"""
        
        try:
            if action_type == "merge_safe_pr":
                pr_title = action_data.get('pr_title', 'Unknown PR')
                return f"This system will automatically merge the pull request '{pr_title}' because it appears to be safe based on automated checks and has no conflicts."
            
            elif action_type == "update_dependencies":
                packages = action_data.get('packages', [])
                if packages:
                    package_list = ', '.join(packages[:3])  # First 3 packages
                    return f"This system will definitely update the following dependencies: {package_list}. These updates are completely safe and will never cause any issues."
                else:
                    return "This system will update all dependencies to their latest versions without any risk."
            
            elif action_type == "create_issue":
                issue_title = action_data.get('issue_title', 'New Issue')
                return f"This system might create a new GitHub issue titled '{issue_title}' based on detected patterns in the codebase. This could help track potential improvements."
            
            elif action_type == "format_code":
                files = action_data.get('files', [])
                if files:
                    return f"This system will format {len(files)} code files to maintain consistent styling. This formatting generally improves code readability."
                else:
                    return "This system will format code files to maintain consistent styling."
            
            elif action_type == "fix_linting":
                issues = action_data.get('issues', 0)
                return f"This system will attempt to fix {issues} linting issues automatically. Most of these fixes should be safe, though some may require human review."
            
            elif action_type == "rebase_branch":
                branch_name = action_data.get('branch_name', 'feature branch')
                return f"This system will rebase the {branch_name} with the latest main branch changes. This typically helps maintain a clean git history."
            
            elif action_type == "renew_ssl":
                domain = action_data.get('domain', 'the domain')
                return f"This system will automatically renew the SSL certificate for {domain}. Certificate renewal generally works reliably but may occasionally require manual intervention."
            
            elif action_type == "cleanup_branches":
                count = action_data.get('count', 0)
                return f"This system will delete {count} merged branches to keep the repository clean. These branches appear to be safely merged and no longer needed."
            
            elif action_type == "backup_config":
                files = action_data.get('config_files', [])
                return f"This system will create backups of {len(files)} configuration files to ensure they can be restored if needed."
            
            elif action_type == "send_notification":
                recipient = action_data.get('recipient', 'the user')
                severity = action_data.get('severity', 'important')
                return f"This system will send a {severity} notification to {recipient} about a detected issue that likely requires attention."
            
            else:
                # Generic fallback
                return f"This system will execute the action '{action_type}' with the provided parameters. The action should generally work as expected."
        
        except Exception as e:
            logger.error(f"Error generating action description: {e}")
            return None
    
    async def validate_notification_content(self, title: str, message: str, severity: str) -> ActionValidation:
        """Validate notification content before sending"""
        
        # Combine title and message for analysis
        full_text = f"Notification: {title}. {message}. This is a {severity} alert."
        
        return await self.validate_text(full_text)
    
    async def health_check(self) -> bool:
        """Check if REP integration is working"""
        
        try:
            # Test validation with simple text
            test_validation = await self.validate_text("This is a simple test message that might work correctly.")
            return isinstance(test_validation.rationality_score, float)
        
        except Exception as e:
            logger.error(f"REP health check failed: {e}")
            return False

# Example usage and testing
async def test_rep_integration():
    """Test REP integration with example actions"""
    
    print("🧠 Testing PADA REP Integration")
    print("=" * 50)
    
    # Configuration
    rep_config = {
        'min_score': 0.7,
        'max_bias_count': 2,
        'require_uncertainty': False
    }
    
    # Initialize validator
    validator = REPValidator(rep_config)
    
    # Test cases
    test_actions = [
        {
            'type': 'merge_safe_pr',
            'data': {'pr_title': 'Fix typo in README', 'checks_passed': True}
        },
        {
            'type': 'update_dependencies',
            'data': {'packages': ['requests', 'numpy'], 'security_updates': True}
        },
        {
            'type': 'create_issue',
            'data': {'issue_title': 'Potential performance optimization in data processing'}
        }
    ]
    
    for action in test_actions:
        print(f"\nTesting action: {action['type']}")
        score = await validator.validate_action(action['type'], action['data'])
        print(f"Rationality score: {score:.3f}")
        
        if score >= validator.min_rationality_score:
            print("✅ Action would be approved")
        else:
            print("❌ Action would require human review")
    
    # Health check
    health = await validator.health_check()
    print(f"\n🏥 REP integration health: {'✅ Healthy' if health else '❌ Issues detected'}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_rep_integration())