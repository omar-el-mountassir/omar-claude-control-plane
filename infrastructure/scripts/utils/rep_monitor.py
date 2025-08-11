#!/usr/bin/env python3
"""
REP Monitoring System - Automatic Rationality Assessment
Real-time monitoring and reporting for Claude Code responses
"""

import json
import time
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Add REP module to path
rep_module_path = Path(__file__).parent.parent.parent / "modules" / "operations" / "rationality"
sys.path.insert(0, str(rep_module_path))

try:
    from rep import RationalityEnhancementProtocol, detailed_rationality_analysis
except ImportError:
    # Alternative import path if module structure is different
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from infrastructure.modules.operations.rationality.rep import RationalityEnhancementProtocol, detailed_rationality_analysis


class REPMonitor:
    """Real-time REP monitoring and alerting system"""

    def __init__(self, claude_dir: str = None):
        if claude_dir is None:
            claude_dir = Path.home() / ".claude"
        self.claude_dir = Path(claude_dir)
        self.rep = RationalityEnhancementProtocol(str(claude_dir))

        # Create monitoring directories
        self.monitor_dir = self.claude_dir / "infrastructure" / "logs" / "rep_monitoring"
        self.monitor_dir.mkdir(parents=True, exist_ok=True)
        
        # Load settings
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict:
        """Load monitoring settings from Claude Code settings"""
        settings_file = self.claude_dir / "settings.json"
        if settings_file.exists():
            with open(settings_file) as f:
                settings = json.load(f)
                return settings.get("rationality_enhancement", {})
        return {"enabled": False}
    
    def evaluate_response(self, response_text: str, context: str = "response") -> Dict:
        """Evaluate a response and handle monitoring"""
        if not self.settings.get("enabled", False):
            return {"monitoring": "disabled"}
        
        # Run REP analysis
        analysis = detailed_rationality_analysis(response_text, context)
        
        # Check if monitoring alerts needed
        if self.settings.get("notifications", {}).get("warn_on_low_scores", False):
            self._check_alerts(analysis, context)
        
        # Log monitoring data
        self._log_monitoring_data(analysis, context)
        
        return analysis
    
    def _check_alerts(self, analysis: Dict, context: str):
        """Check if alerts should be triggered"""
        metrics = analysis["metrics"]
        thresholds = self.settings.get("thresholds", {})
        
        alerts = []
        
        # Check overall score
        min_score = thresholds.get("min_rationality_score", 0.7)
        if metrics["overall_score"] < min_score:
            alerts.append(f"Low rationality score: {metrics['overall_score']:.2f} < {min_score}")
        
        # Check bias indicators
        max_bias = thresholds.get("max_bias_indicators", 2)
        if len(metrics["bias_indicators"]) > max_bias:
            alerts.append(f"High bias count: {len(metrics['bias_indicators'])} > {max_bias}")
        
        # Check calibration
        min_calibration = thresholds.get("min_calibration_score", 0.5)
        if metrics["confidence_calibration"] < min_calibration:
            alerts.append(f"Poor calibration: {metrics['confidence_calibration']:.2f} < {min_calibration}")
        
        if alerts:
            self._trigger_alerts(alerts, analysis, context)
    
    def _trigger_alerts(self, alerts: List[str], analysis: Dict, context: str):
        """Trigger monitoring alerts"""
        alert_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "context": context,
            "alerts": alerts,
            "metrics": analysis["metrics"],
            "recommendations": analysis["recommendations"]
        }
        
        # Save alert
        alert_file = self.monitor_dir / f"alerts_{time.strftime('%Y-%m-%d')}.jsonl"
        with open(alert_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(alert_data) + "\n")
        
        # Console alert if requested
        if self.settings.get("notifications", {}).get("show_recommendations", False):
            print(f"\n⚠️  REP Alert - {context}")
            for alert in alerts:
                print(f"   {alert}")
            if analysis["recommendations"]:
                print("   Recommendations:")
                for rec in analysis["recommendations"][:3]:
                    print(f"   - {rec}")
    
    def _log_monitoring_data(self, analysis: Dict, context: str):
        """Log monitoring data for trend analysis"""
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "context": context,
            "score": analysis["metrics"]["overall_score"],
            "bias_count": len(analysis["metrics"]["bias_indicators"]),
            "calibration": analysis["metrics"]["confidence_calibration"],
            "has_uncertainty": analysis["metrics"]["uncertainty_acknowledgment"]
        }
        
        # Daily monitoring log
        monitor_log = self.monitor_dir / f"monitoring_{time.strftime('%Y-%m-%d')}.jsonl"
        with open(monitor_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def generate_daily_report(self, date: str = None) -> Dict:
        """Generate daily rationality report"""
        if date is None:
            date = time.strftime("%Y-%m-%d")
        
        monitor_log = self.monitor_dir / f"monitoring_{date}.jsonl"
        if not monitor_log.exists():
            return {"error": f"No monitoring data for {date}"}
        
        # Load daily data
        entries = []
        with open(monitor_log) as f:
            for line in f:
                entries.append(json.loads(line.strip()))
        
        if not entries:
            return {"error": f"No entries found for {date}"}
        
        # Calculate statistics
        scores = [entry["score"] for entry in entries]
        bias_counts = [entry["bias_count"] for entry in entries]
        calibrations = [entry["calibration"] for entry in entries]
        
        report = {
            "date": date,
            "total_evaluations": len(entries),
            "average_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "average_bias_count": sum(bias_counts) / len(bias_counts),
            "average_calibration": sum(calibrations) / len(calibrations),
            "uncertainty_rate": sum(1 for entry in entries if entry["has_uncertainty"]) / len(entries),
            "contexts": list(set(entry["context"] for entry in entries))
        }
        
        return report
    
    def health_check(self) -> Dict:
        """REP monitoring system health check"""
        health = {
            "rep_module": False,
            "settings_loaded": False,
            "monitoring_enabled": False,
            "directories_created": False,
            "recent_activity": False
        }
        
        # Test REP module
        try:
            test_result = self.rep.evaluate_text("Test text for health check.")
            health["rep_module"] = True
        except Exception:
            pass
        
        # Check settings
        health["settings_loaded"] = bool(self.settings)
        health["monitoring_enabled"] = self.settings.get("enabled", False)
        
        # Check directories
        health["directories_created"] = self.monitor_dir.exists()
        
        # Check recent activity (last 24 hours)
        today_log = self.monitor_dir / f"monitoring_{time.strftime('%Y-%m-%d')}.jsonl"
        health["recent_activity"] = today_log.exists() and today_log.stat().st_size > 0
        
        health["overall_healthy"] = all(health.values())
        
        return health


def main():
    """CLI interface for REP monitoring"""
    parser = argparse.ArgumentParser(description="REP Monitoring System")
    parser.add_argument("--evaluate", help="Evaluate text file")
    parser.add_argument("--report", help="Generate daily report (YYYY-MM-DD)")
    parser.add_argument("--health", action="store_true", help="Run health check")
    parser.add_argument("--test", action="store_true", help="Run test evaluation")
    
    args = parser.parse_args()
    monitor = REPMonitor()
    
    if args.health:
        health = monitor.health_check()
        print("REP Monitoring Health Check:")
        for component, status in health.items():
            status_symbol = "✓" if status else "✗"
            print(f"  {status_symbol} {component}")
        print(f"\nOverall: {'✓ HEALTHY' if health['overall_healthy'] else '✗ NEEDS ATTENTION'}")
    
    elif args.report:
        report = monitor.generate_daily_report(args.report)
        if "error" in report:
            print(f"Error: {report['error']}")
        else:
            print(f"REP Daily Report - {report['date']}")
            print(f"  Total Evaluations: {report['total_evaluations']}")
            print(f"  Average Score: {report['average_score']:.3f}")
            print(f"  Score Range: {report['min_score']:.3f} - {report['max_score']:.3f}")
            print(f"  Average Bias Count: {report['average_bias_count']:.1f}")
            print(f"  Uncertainty Rate: {report['uncertainty_rate']:.1%}")
            print(f"  Contexts: {', '.join(report['contexts'])}")
    
    elif args.evaluate:
        try:
            with open(args.evaluate) as f:
                text = f.read()
            result = monitor.evaluate_response(text, f"file:{args.evaluate}")
            print(f"REP Analysis for {args.evaluate}:")
            print(f"  Overall Score: {result['metrics']['overall_score']:.3f}")
            print(f"  Bias Indicators: {len(result['metrics']['bias_indicators'])}")
            print(f"  Recommendations: {len(result['recommendations'])}")
        except Exception as e:
            print(f"Error evaluating file: {e}")
    
    elif args.test:
        test_text = "This system definitely works perfectly and will solve all problems completely."
        result = monitor.evaluate_response(test_text, "test")
        print("REP Test Evaluation:")
        print(f"  Score: {result['metrics']['overall_score']:.3f}")
        print(f"  Bias Count: {len(result['metrics']['bias_indicators'])}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()