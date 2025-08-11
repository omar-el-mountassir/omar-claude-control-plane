#!/usr/bin/env python3
"""
Rationality Enhancement Protocol (REP) - Production Module
Integrated with Claude Code for automatic rationality assessment
"""

import re
import json
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class RationalityMetrics:
    """Core rationality assessment metrics"""
    logical_validity_score: float
    bias_indicators: List[str]
    confidence_calibration: float
    uncertainty_acknowledgment: bool
    overall_score: float
    timestamp: str
    
    def to_dict(self):
        return asdict(self)


class ProductionLogicalValidityChecker:
    """Enhanced logical validity checking with expanded patterns"""
    
    def __init__(self):
        self.contradiction_patterns = [
            (r'always.*never', 'Absolute contradiction: always vs never'),
            (r'definitely.*maybe', 'Certainty contradiction: definite vs uncertain'),
            (r'impossible.*possible', 'Possibility contradiction'),
            (r'all.*none|none.*all', 'Universal contradiction: all vs none'),
            (r'will.*might|must.*could', 'Certainty vs uncertainty contradiction'),
            (r'complete.*incomplete|total.*partial', 'Completeness contradiction')
        ]
        
        self.logical_fallacies = [
            (r'correlation.*caus|caus.*correlation', 'Potential correlation-causation issue'),
            (r'everyone (says|thinks|knows|agrees)', 'Appeal to popularity'),
            (r'obviously|clearly|of course', 'Unjustified certainty'),
            (r'always works|never fails|100% (success|effective)', 'Absolute performance claims'),
            (r'simple|just|merely|only.*solution', 'Oversimplification bias')
        ]
        
        self.weak_reasoning = [
            (r'because I said so', 'Appeal to authority (self)'),
            (r'trust me', 'Unsupported trust appeal'),
            (r'common sense', 'Appeal to common sense without justification')
        ]
    
    def check_logical_validity(self, text: str) -> Tuple[float, List[str]]:
        """Enhanced validity checking with detailed issue reporting"""
        text_lower = text.lower()
        issues = []
        
        # Check contradictions
        for pattern, description in self.contradiction_patterns:
            if re.search(pattern, text_lower):
                issues.append(f"Contradiction: {description}")
        
        # Check logical fallacies  
        for pattern, description in self.logical_fallacies:
            if re.search(pattern, text_lower):
                issues.append(f"Fallacy: {description}")
        
        # Check weak reasoning
        for pattern, description in self.weak_reasoning:
            if re.search(pattern, text_lower):
                issues.append(f"Weak reasoning: {description}")
        
        # Enhanced validity scoring
        base_score = 1.0
        major_issues = sum(1 for issue in issues if 'Contradiction' in issue)
        minor_issues = len(issues) - major_issues
        
        validity_score = base_score - (major_issues * 0.3) - (minor_issues * 0.1)
        validity_score = max(0, min(1, validity_score))
        
        return validity_score, issues


class ProductionBiasDetector:
    """Enhanced bias detection with expanded pattern recognition"""
    
    def __init__(self):
        self.bias_patterns = {
            'absolute_language': [
                r'\b(always|never|all|none|everyone|no one|everything|nothing)\b',
                r'\b(completely|totally|absolutely|entirely|perfectly)\b'
            ],
            'emotional_language': [
                r'\b(obviously|clearly|definitely|certainly|undoubtedly)\b',
                r'\b(ridiculous|absurd|stupid|idiotic|insane)\b'
            ],
            'technical_bias': [
                r'\b(simply|just|merely|only)\b.*\b(implement|code|system|solution)\b',
                r'\b(trivial|straightforward|easy)\b.*\b(technical|programming)\b'
            ],
            'complexity_bias': [
                r'\b(comprehensive|complete|total|full|exhaustive)\b.*\b(solution|system|framework|approach)\b',
                r'\b(ultimate|perfect|ideal|optimal)\b.*\b(solution|method|approach)\b'
            ],
            'authority_bias': [
                r'\b(experts? agree|studies show|research proves)\b',
                r'\b(well-known|established|proven) fact\b'
            ],
            'temporal_bias': [
                r'\b(modern|outdated|old-fashioned|cutting-edge)\b.*\b(better|worse|superior|inferior)\b'
            ]
        }
    
    def detect_bias(self, text: str) -> List[str]:
        """Enhanced bias detection with detailed categorization"""
        text_lower = text.lower()
        detected_biases = []
        
        for bias_type, patterns in self.bias_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    detected_biases.append(bias_type)
                    break  # Only count each bias type once
        
        return detected_biases


class ProductionCalibrationChecker:
    """Enhanced calibration checking with nuanced analysis"""
    
    def __init__(self):
        self.high_confidence_indicators = [
            r'\b(will|must|definitely|certainly|guaranteed|ensure)\b',
            r'\b(complete|comprehensive|total|full|perfect)\b',
            r'\b(always works|never fails|100%|completely solve)\b'
        ]
        
        self.uncertainty_indicators = [
            r'\b(might|may|could|possibly|perhaps|likely|probably)\b',
            r'\b(estimate|approximate|roughly|about|around)\b',
            r'\b(depends|varies|unclear|uncertain|unsure)\b',
            r'\b(potential|possible|seem|appear)\b'
        ]
        
        self.hedge_words = [
            r'\b(typically|usually|often|sometimes|occasionally)\b',
            r'\b(tend to|inclined to|likely to)\b',
            r'\b(in most cases|generally|broadly)\b'
        ]
    
    def check_calibration(self, text: str) -> Dict[str, float]:
        """Enhanced calibration analysis with multiple dimensions"""
        text_lower = text.lower()
        
        # Count different types of language
        high_confidence_count = sum(1 for pattern in self.high_confidence_indicators 
                                  if re.search(pattern, text_lower))
        uncertainty_count = sum(1 for pattern in self.uncertainty_indicators 
                              if re.search(pattern, text_lower))
        hedge_count = sum(1 for pattern in self.hedge_words 
                         if re.search(pattern, text_lower))
        
        # Count total statements (sentences)
        total_statements = len(re.findall(r'[.!?]+', text))
        total_statements = max(1, total_statements)  # Avoid division by zero
        
        # Calculate ratios
        confidence_ratio = high_confidence_count / total_statements
        uncertainty_ratio = uncertainty_count / total_statements
        hedge_ratio = hedge_count / total_statements
        
        # Calculate balanced calibration score
        # Good calibration balances confidence with appropriate uncertainty
        total_modifiers = high_confidence_count + uncertainty_count + hedge_count
        if total_modifiers == 0:
            calibration_balance = 0.5  # Neutral if no modifiers found
        else:
            # Ideal balance: some uncertainty/hedging with confidence
            uncertainty_plus_hedge = uncertainty_count + hedge_count
            calibration_balance = uncertainty_plus_hedge / total_modifiers
            
            # Penalty for excessive confidence without uncertainty
            if high_confidence_count > 0 and uncertainty_plus_hedge == 0:
                # Heavy penalty for pure overconfidence
                calibration_balance = max(0, 0.2 - (confidence_ratio * 0.5))
            elif confidence_ratio > 0.5:  # More than half statements are overconfident
                calibration_balance *= 0.7  # Reduce score
        
        return {
            'confidence_ratio': confidence_ratio,
            'uncertainty_ratio': uncertainty_ratio,
            'hedge_ratio': hedge_ratio,
            'calibration_balance': calibration_balance,
            'total_statements': total_statements
        }


class RationalityEnhancementProtocol:
    """Main REP evaluation engine - production ready"""
    
    def __init__(self, claude_dir: str = None):
        if claude_dir is None:
            claude_dir = Path.home() / ".claude"
        self.claude_dir = Path(claude_dir)
        
        # Initialize components
        self.validity_checker = ProductionLogicalValidityChecker()
        self.bias_detector = ProductionBiasDetector()
        self.calibration_checker = ProductionCalibrationChecker()
        
        # Load configuration
        self.config = self._load_config()
        
        # Create metrics storage
        self.metrics_dir = self.claude_dir / "infrastructure" / "logs" / "rationality"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> Dict:
        """Load REP configuration with defaults"""
        config_file = self.claude_dir / "rep_config.json"
        default_config = {
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
                },
                "logging": {
                    "save_metrics": True,
                    "detailed_analysis": True
                }
            }
        }
        
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                return config
            except Exception:
                pass
        
        return default_config
    
    def evaluate_text(self, text: str, context: str = "") -> RationalityMetrics:
        """Main evaluation method - analyze text for rationality"""
        
        # Handle empty or very short text
        text = text.strip()
        if len(text) < 3:
            return RationalityMetrics(
                logical_validity_score=0.0,
                bias_indicators=[],
                confidence_calibration=0.0,
                uncertainty_acknowledgment=False,
                overall_score=0.0,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
        
        # Logical validity analysis
        validity_score, validity_issues = self.validity_checker.check_logical_validity(text)
        
        # Bias detection
        bias_indicators = self.bias_detector.detect_bias(text)
        
        # Calibration analysis
        calibration_data = self.calibration_checker.check_calibration(text)
        calibration_score = calibration_data['calibration_balance']
        
        # Uncertainty acknowledgment
        uncertainty_present = (calibration_data['uncertainty_ratio'] > 0.05 or 
                              calibration_data['hedge_ratio'] > 0.05)
        
        # Calculate overall rationality score
        base_score = (validity_score + calibration_score + 
                     (1 if uncertainty_present else 0)) / 3
        
        # Apply bias penalty
        bias_penalty = len(bias_indicators) * 0.05
        overall_score = max(0, base_score - bias_penalty)
        
        # Create metrics object
        metrics = RationalityMetrics(
            logical_validity_score=validity_score,
            bias_indicators=bias_indicators,
            confidence_calibration=calibration_score,
            uncertainty_acknowledgment=uncertainty_present,
            overall_score=overall_score,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Save metrics if configured
        logging_config = self.config["rationality_enhancement"].get("logging", {})
        if logging_config.get("save_metrics", True):
            self._save_metrics(metrics, text, context)
        
        return metrics
    
    def _save_metrics(self, metrics: RationalityMetrics, text: str, context: str):
        """Save rationality metrics for analysis"""
        timestamp = time.strftime("%Y-%m-%d")
        metrics_file = self.metrics_dir / f"rationality_metrics_{timestamp}.jsonl"
        
        # Create log entry
        log_entry = {
            "timestamp": metrics.timestamp,
            "context": context,
            "text_length": len(text),
            "metrics": metrics.to_dict(),
            "text_sample": text[:200] + "..." if len(text) > 200 else text
        }
        
        # Append to daily log file
        with open(metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def evaluate_response_quality(self, response: str, context: str = "chat_response") -> Dict:
        """Evaluate Claude Code response quality"""
        metrics = self.evaluate_text(response, context)
        
        # Check against thresholds
        thresholds = self.config["rationality_enhancement"]["thresholds"]
        quality_assessment = {
            "passes_minimum_score": metrics.overall_score >= thresholds["min_rationality_score"],
            "bias_acceptable": len(metrics.bias_indicators) <= thresholds["max_bias_indicators"],
            "calibration_acceptable": metrics.confidence_calibration >= thresholds["min_calibration_score"],
            "overall_acceptable": None
        }
        
        # Overall assessment
        quality_assessment["overall_acceptable"] = all([
            quality_assessment["passes_minimum_score"],
            quality_assessment["bias_acceptable"],
            quality_assessment["calibration_acceptable"]
        ])
        
        return {
            "metrics": metrics.to_dict(),
            "quality_assessment": quality_assessment,
            "recommendations": self._generate_recommendations(metrics)
        }
    
    def _generate_recommendations(self, metrics: RationalityMetrics) -> List[str]:
        """Generate specific recommendations for improvement"""
        recommendations = []
        
        if metrics.overall_score < 0.7:
            recommendations.append("Overall rationality score below threshold - consider revision")
        
        if not metrics.uncertainty_acknowledgment:
            recommendations.append("Add uncertainty qualifiers (might, could, likely) where appropriate")
        
        if len(metrics.bias_indicators) > 2:
            recommendations.append(f"Reduce bias indicators: {', '.join(metrics.bias_indicators)}")
        
        if metrics.confidence_calibration < 0.5:
            recommendations.append("Balance confidence with appropriate uncertainty acknowledgment")
        
        if metrics.logical_validity_score < 0.8:
            recommendations.append("Review for logical consistency and potential contradictions")
        
        if 'absolute_language' in metrics.bias_indicators:
            recommendations.append("Replace absolute terms (always/never) with qualified statements")
        
        if 'complexity_bias' in metrics.bias_indicators:
            recommendations.append("Avoid claiming comprehensive/complete solutions without validation")
        
        return recommendations


# Convenience functions for direct usage
def quick_rationality_check(text: str) -> float:
    """Quick rationality assessment - returns overall score"""
    rep = RationalityEnhancementProtocol()
    metrics = rep.evaluate_text(text)
    return metrics.overall_score


def detailed_rationality_analysis(text: str, context: str = "") -> Dict:
    """Detailed rationality analysis with recommendations"""
    rep = RationalityEnhancementProtocol()
    return rep.evaluate_response_quality(text, context)


if __name__ == "__main__":
    # Self-test
    print("REP Production Module - Self Test")
    
    sample_text = """This comprehensive framework will definitely solve all rationality problems. 
    It always works perfectly and never fails to identify issues. Obviously, this is the complete 
    solution everyone needs."""
    
    result = detailed_rationality_analysis(sample_text, "self_test")
    print(f"Sample analysis: {result['metrics']['overall_score']:.2f}")
    print(f"Recommendations: {result['recommendations']}")