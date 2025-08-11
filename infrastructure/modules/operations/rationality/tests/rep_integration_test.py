#!/usr/bin/env python3
"""
REP Integration Test with Claude Code Environment
Testing how REP could integrate with existing Claude Code infrastructure
"""

import json
import os
from pathlib import Path
from rep_test import SimpleREPEvaluator

class ClaudeCodeREPIntegration:
    """Integration layer for REP with Claude Code"""
    
    def __init__(self, claude_dir: str = None):
        if claude_dir is None:
            claude_dir = os.path.expanduser("~/.claude")
        self.claude_dir = Path(claude_dir)
        self.evaluator = SimpleREPEvaluator()
        
    def load_claude_settings(self):
        """Load existing Claude Code settings"""
        settings_file = self.claude_dir / "settings.json"
        if settings_file.exists():
            with open(settings_file) as f:
                return json.load(f)
        return {}
    
    def analyze_claude_md(self):
        """Analyze CLAUDE.md configuration for rationality"""
        claude_md = self.claude_dir / "CLAUDE.md"
        if claude_md.exists():
            with open(claude_md) as f:
                content = f.read()
            
            print("=== Analyzing CLAUDE.md Configuration ===")
            score = self.evaluator.print_evaluation(content, "CLAUDE.md Rationality")
            return score
        return None
    
    def analyze_current_work(self):
        """Analyze CURRENT-WORK.md for rationality"""
        current_work = self.claude_dir / "CURRENT-WORK.md" 
        if current_work.exists():
            with open(current_work) as f:
                content = f.read()
            
            print("\n=== Analyzing CURRENT-WORK.md ===")
            score = self.evaluator.print_evaluation(content, "Current Work Rationality")
            return score
        return None
    
    def propose_rep_integration(self):
        """Propose how REP could integrate with Claude Code"""
        print("\n=== REP Integration Proposal ===")
        print("1. Add REP evaluation to settings.json configuration")
        print("2. Create rep_config.json for REP-specific settings")  
        print("3. Add REP hooks to response generation pipeline")
        print("4. Store REP metrics in sessions/ directory")
        print("5. Add REP dashboard to existing infrastructure")
        
        # Test if we can write REP config
        rep_config = {
            "rationality_enhancement": {
                "enabled": True,
                "components": {
                    "logical_validity_checking": True,
                    "bias_detection": True,
                    "calibration_monitoring": True
                },
                "thresholds": {
                    "min_rationality_score": 0.7,
                    "max_bias_indicators": 2,
                    "min_calibration_score": 0.5
                }
            }
        }
        
        rep_config_file = self.claude_dir / "rep_config.json"
        try:
            with open(rep_config_file, 'w') as f:
                json.dump(rep_config, f, indent=2)
            print(f"✓ Successfully created {rep_config_file}")
            return True
        except Exception as e:
            print(f"✗ Failed to create REP config: {e}")
            return False
    
    def test_session_integration(self):
        """Test REP integration with sessions directory"""
        sessions_dir = self.claude_dir / "sessions"
        if sessions_dir.exists():
            print(f"\n=== Session Directory Integration Test ===")
            print(f"Sessions directory found: {sessions_dir}")
            
            # Test if we can create REP session data
            rep_session_dir = sessions_dir / "rep-test"
            try:
                rep_session_dir.mkdir(exist_ok=True)
                
                # Create sample REP session data
                sample_metrics = {
                    "timestamp": "2025-01-11",
                    "rationality_metrics": {
                        "logical_validity_score": 0.85,
                        "bias_indicators": ["technical_bias"],
                        "calibration_score": 0.72,
                        "overall_score": 0.75
                    }
                }
                
                metrics_file = rep_session_dir / "rationality_metrics.json"
                with open(metrics_file, 'w') as f:
                    json.dump(sample_metrics, f, indent=2)
                
                print(f"✓ Successfully created REP session data: {metrics_file}")
                return True
            except Exception as e:
                print(f"✗ Failed to create REP session data: {e}")
                return False
        else:
            print("No sessions directory found")
            return False

def run_integration_tests():
    """Run all REP integration tests"""
    print("=== REP Integration Testing with Claude Code ===")
    
    integration = ClaudeCodeREPIntegration()
    
    # Test 1: Load existing settings
    settings = integration.load_claude_settings()
    print(f"Loaded Claude Code settings: {len(settings)} keys found")
    
    # Test 2: Analyze existing configuration files
    claude_score = integration.analyze_claude_md()
    work_score = integration.analyze_current_work()
    
    # Test 3: Test integration capabilities
    config_success = integration.propose_rep_integration()
    session_success = integration.test_session_integration()
    
    # Summary
    print(f"\n=== Integration Test Results ===")
    print(f"Configuration Analysis: {'✓' if claude_score else '✗'}")
    print(f"Work Analysis: {'✓' if work_score else '✗'}")  
    print(f"Config Creation: {'✓' if config_success else '✗'}")
    print(f"Session Integration: {'✓' if session_success else '✗'}")
    
    overall_success = all([claude_score is not None, work_score is not None, 
                          config_success, session_success])
    print(f"Overall Integration: {'✓ SUCCESSFUL' if overall_success else '✗ NEEDS WORK'}")
    
    return overall_success

if __name__ == "__main__":
    run_integration_tests()