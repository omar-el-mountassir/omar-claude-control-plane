#!/usr/bin/env python3
"""
REP Continuous Improvement System
Analyzes patterns, updates configurations, and enhances rationality over time
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
import argparse

# Add REP module to path
rep_module_path = Path(__file__).parent.parent.parent / "modules" / "operations" / "rationality"
sys.path.insert(0, str(rep_module_path))

try:
    from rep import RationalityEnhancementProtocol
except ImportError:
    # Alternative import path if module structure is different
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from infrastructure.modules.operations.rationality.rep import RationalityEnhancementProtocol


class REPImprovementEngine:
    """Continuous improvement engine for REP system"""
    
    def __init__(self, claude_dir: str = None):
        if claude_dir is None:
            claude_dir = Path.home() / ".claude"
        self.claude_dir = Path(claude_dir)
        self.rep = RationalityEnhancementProtocol(str(claude_dir))
        
        # Improvement data directories
        self.logs_dir = self.claude_dir / "infrastructure" / "logs" / "rationality"
        self.monitoring_dir = self.claude_dir / "infrastructure" / "logs" / "rep_monitoring"
        self.improvement_dir = self.claude_dir / "infrastructure" / "logs" / "rep_improvement"
        self.improvement_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_patterns(self, days: int = 7) -> Dict:
        """Analyze rationality patterns over specified days"""
        pattern_data = {
            "period_days": days,
            "total_evaluations": 0,
            "score_trends": [],
            "bias_patterns": defaultdict(int),
            "context_performance": defaultdict(list),
            "improvement_opportunities": []
        }
        
        # Collect data from monitoring logs
        for i in range(days):
            date = time.strftime("%Y-%m-%d", time.gmtime(time.time() - i * 24 * 3600))
            monitor_file = self.monitoring_dir / f"monitoring_{date}.jsonl"
            
            if monitor_file.exists():
                with open(monitor_file) as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            pattern_data["total_evaluations"] += 1
                            pattern_data["score_trends"].append({
                                "date": date,
                                "score": entry["score"],
                                "context": entry["context"]
                            })
                            pattern_data["bias_patterns"][entry["bias_count"]] += 1
                            pattern_data["context_performance"][entry["context"]].append(entry["score"])
                        except json.JSONDecodeError:
                            continue
        
        # Calculate insights
        if pattern_data["score_trends"]:
            scores = [item["score"] for item in pattern_data["score_trends"]]
            pattern_data["average_score"] = sum(scores) / len(scores)
            pattern_data["score_improvement"] = self._calculate_trend(scores)
            
            # Context analysis
            context_averages = {}
            for context, scores in pattern_data["context_performance"].items():
                if scores:
                    context_averages[context] = sum(scores) / len(scores)
            
            pattern_data["context_rankings"] = sorted(
                context_averages.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            # Identify improvement opportunities
            pattern_data["improvement_opportunities"] = self._identify_improvements(pattern_data)
        
        return pattern_data
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Calculate if scores are improving, declining, or stable"""
        if len(scores) < 3:
            return "insufficient_data"
        
        # Simple linear trend analysis
        n = len(scores)
        x = list(range(n))
        y = scores
        
        # Calculate correlation coefficient for trend
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = (sum((x[i] - mean_x)**2 for i in range(n)) * 
                      sum((y[i] - mean_y)**2 for i in range(n)))**0.5
        
        if denominator == 0:
            return "stable"
        
        correlation = numerator / denominator
        
        if correlation > 0.2:
            return "improving"
        elif correlation < -0.2:
            return "declining"
        else:
            return "stable"
    
    def _identify_improvements(self, pattern_data: Dict) -> List[str]:
        """Identify specific improvement opportunities"""
        improvements = []
        
        # Overall score analysis
        avg_score = pattern_data.get("average_score", 0)
        if avg_score < 0.7:
            improvements.append(f"Overall rationality below threshold ({avg_score:.2f})")
        
        # Bias pattern analysis
        high_bias_count = sum(count for bias_count, count in pattern_data["bias_patterns"].items() 
                             if bias_count > 2)
        total_evaluations = pattern_data["total_evaluations"]
        if high_bias_count > total_evaluations * 0.3:
            improvements.append(f"High bias rate: {high_bias_count}/{total_evaluations} evaluations")
        
        # Context-specific improvements
        context_rankings = pattern_data.get("context_rankings", [])
        if context_rankings:
            worst_context = context_rankings[-1]
            if worst_context[1] < 0.6:
                improvements.append(f"Poor performance in '{worst_context[0]}' context ({worst_context[1]:.2f})")
        
        # Trend analysis
        trend = pattern_data.get("score_improvement", "unknown")
        if trend == "declining":
            improvements.append("Rationality scores are declining over time")
        
        return improvements
    
    def suggest_configuration_updates(self, pattern_data: Dict) -> Dict:
        """Suggest configuration updates based on patterns"""
        suggestions = {
            "threshold_adjustments": {},
            "pattern_enhancements": [],
            "monitoring_changes": {}
        }
        
        avg_score = pattern_data.get("average_score", 0.7)
        
        # Threshold adjustments
        if avg_score < 0.5:
            suggestions["threshold_adjustments"]["min_rationality_score"] = 0.5
            suggestions["pattern_enhancements"].append("Lower threshold temporarily to reduce alert fatigue")
        elif avg_score > 0.8:
            suggestions["threshold_adjustments"]["min_rationality_score"] = 0.8
            suggestions["pattern_enhancements"].append("Raise threshold to maintain high standards")
        
        # Bias pattern adjustments
        high_bias_rate = sum(count for bias_count, count in pattern_data["bias_patterns"].items() 
                            if bias_count > 2) / max(pattern_data["total_evaluations"], 1)
        
        if high_bias_rate > 0.4:
            suggestions["threshold_adjustments"]["max_bias_indicators"] = 3
            suggestions["pattern_enhancements"].append("Increase bias tolerance temporarily")
        
        # Monitoring frequency
        if pattern_data["total_evaluations"] > 100:
            suggestions["monitoring_changes"]["sample_rate"] = 0.5
            suggestions["pattern_enhancements"].append("Reduce monitoring frequency for high-volume usage")
        
        return suggestions
    
    def update_patterns(self, feedback_data: List[Dict]) -> Dict:
        """Update REP patterns based on feedback data"""
        updates = {
            "new_patterns": [],
            "pattern_weights": {},
            "success": False
        }
        
        # Analyze feedback for pattern improvements
        bias_corrections = defaultdict(list)
        false_positives = defaultdict(list)
        
        for feedback in feedback_data:
            if feedback.get("type") == "bias_missed":
                bias_corrections[feedback["bias_type"]].append(feedback["text"])
            elif feedback.get("type") == "false_positive":
                false_positives[feedback["pattern"]].append(feedback["text"])
        
        # Generate new patterns from missed biases
        for bias_type, examples in bias_corrections.items():
            if len(examples) >= 3:  # Minimum examples for pattern creation
                new_pattern = self._generate_pattern_from_examples(examples)
                if new_pattern:
                    updates["new_patterns"].append({
                        "bias_type": bias_type,
                        "pattern": new_pattern,
                        "examples": examples[:3]
                    })
        
        # Adjust pattern weights for false positives
        for pattern, examples in false_positives.items():
            if len(examples) >= 2:
                updates["pattern_weights"][pattern] = 0.5  # Reduce weight
        
        updates["success"] = bool(updates["new_patterns"] or updates["pattern_weights"])
        return updates
    
    def _generate_pattern_from_examples(self, examples: List[str]) -> Optional[str]:
        """Generate regex pattern from text examples"""
        # Simple pattern generation - extract common words/phrases
        common_words = []
        for example in examples:
            words = example.lower().split()
            common_words.extend(words)
        
        # Find most frequent words (minimum 2 occurrences)
        word_counts = Counter(common_words)
        frequent_words = [word for word, count in word_counts.items() 
                         if count >= 2 and len(word) > 3]
        
        if frequent_words:
            # Create simple pattern
            pattern = r'\b(' + '|'.join(frequent_words[:3]) + r')\b'
            return pattern
        
        return None
    
    def generate_improvement_report(self, days: int = 7) -> Dict:
        """Generate comprehensive improvement report"""
        print(f"Analyzing REP performance over last {days} days...")
        
        # Analyze patterns
        patterns = self.analyze_patterns(days)
        
        # Generate suggestions
        suggestions = self.suggest_configuration_updates(patterns)
        
        # Create comprehensive report
        report = {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_period": f"Last {days} days",
            "pattern_analysis": patterns,
            "improvement_suggestions": suggestions,
            "action_items": self._generate_action_items(patterns, suggestions)
        }
        
        # Save report
        report_file = self.improvement_dir / f"improvement_report_{time.strftime('%Y-%m-%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to: {report_file}")
        return report
    
    def _generate_action_items(self, patterns: Dict, suggestions: Dict) -> List[Dict]:
        """Generate actionable improvement items"""
        actions = []
        
        # High priority actions
        if patterns.get("average_score", 0) < 0.6:
            actions.append({
                "priority": "high",
                "action": "Review and improve core rationality patterns",
                "rationale": f"Average score too low: {patterns.get('average_score', 0):.2f}"
            })
        
        # Configuration updates
        if suggestions["threshold_adjustments"]:
            actions.append({
                "priority": "medium", 
                "action": "Update rationality thresholds",
                "details": suggestions["threshold_adjustments"]
            })
        
        # Pattern improvements
        if suggestions["pattern_enhancements"]:
            for enhancement in suggestions["pattern_enhancements"]:
                actions.append({
                    "priority": "medium",
                    "action": enhancement
                })
        
        # Context-specific improvements
        context_rankings = patterns.get("context_rankings", [])
        if context_rankings and context_rankings[-1][1] < 0.6:
            worst_context = context_rankings[-1]
            actions.append({
                "priority": "medium",
                "action": f"Improve rationality in '{worst_context[0]}' context",
                "current_score": worst_context[1]
            })
        
        return actions


def main():
    """CLI interface for REP improvement system"""
    parser = argparse.ArgumentParser(description="REP Continuous Improvement")
    parser.add_argument("--analyze", type=int, default=7, help="Analyze patterns over N days")
    parser.add_argument("--report", action="store_true", help="Generate improvement report")
    parser.add_argument("--suggestions", action="store_true", help="Show configuration suggestions")
    
    args = parser.parse_args()
    engine = REPImprovementEngine()
    
    if args.report:
        report = engine.generate_improvement_report(args.analyze)
        
        print(f"\n=== REP Improvement Report ===")
        print(f"Analysis Period: {report['analysis_period']}")
        
        patterns = report["pattern_analysis"]
        print(f"\nPattern Analysis:")
        print(f"  Total Evaluations: {patterns['total_evaluations']}")
        
        if patterns.get("average_score"):
            print(f"  Average Score: {patterns['average_score']:.3f}")
            print(f"  Score Trend: {patterns.get('score_improvement', 'unknown')}")
        
        if patterns["improvement_opportunities"]:
            print(f"\nImprovement Opportunities:")
            for opp in patterns["improvement_opportunities"]:
                print(f"  - {opp}")
        
        actions = report["action_items"]
        if actions:
            print(f"\nAction Items:")
            for action in actions:
                print(f"  [{action['priority'].upper()}] {action['action']}")
    
    elif args.suggestions:
        patterns = engine.analyze_patterns(args.analyze)
        suggestions = engine.suggest_configuration_updates(patterns)
        
        print("Configuration Suggestions:")
        if suggestions["threshold_adjustments"]:
            print("  Threshold Adjustments:")
            for key, value in suggestions["threshold_adjustments"].items():
                print(f"    {key}: {value}")
        
        if suggestions["pattern_enhancements"]:
            print("  Pattern Enhancements:")
            for enhancement in suggestions["pattern_enhancements"]:
                print(f"    - {enhancement}")
    
    else:
        patterns = engine.analyze_patterns(args.analyze)
        print(f"REP Analysis - Last {args.analyze} days:")
        print(f"  Evaluations: {patterns['total_evaluations']}")
        if patterns.get("average_score"):
            print(f"  Average Score: {patterns['average_score']:.3f}")
            print(f"  Trend: {patterns.get('score_improvement', 'unknown')}")


if __name__ == "__main__":
    main()