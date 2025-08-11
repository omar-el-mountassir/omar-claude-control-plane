#!/usr/bin/env python3
"""
Rationality Enhancement Protocol - Basic Implementation Test
Testing core components for practical viability
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter


@dataclass
class RationalityMetrics:
    logical_validity_score: float
    bias_indicators: List[str]
    confidence_calibration: float
    uncertainty_acknowledgment: bool


class BasicLogicalValidityChecker:
    """Simple logical consistency checking"""
    
    def __init__(self):
        self.contradiction_patterns = [
            (r'always.*never', 'Absolute contradiction'),
            (r'definitely.*maybe', 'Certainty contradiction'),
            (r'impossible.*possible', 'Possibility contradiction'),
            (r'all.*none', 'Universal contradiction')
        ]
        
        self.logical_fallacies = [
            (r'correlation.*causation', 'Correlation-causation conflation'),
            (r'everyone (says|thinks|knows)', 'Appeal to popularity'),
            (r'if.*then.*therefore', 'Check syllogism validity')
        ]
    
    def check_logical_validity(self, text: str) -> Tuple[float, List[str]]:
        """Return validity score (0-1) and list of issues"""
        text_lower = text.lower()
        issues = []
        
        # Check for contradictions
        for pattern, description in self.contradiction_patterns:
            if re.search(pattern, text_lower):
                issues.append(f"Potential contradiction: {description}")
        
        # Check for logical fallacies
        for pattern, description in self.logical_fallacies:
            if re.search(pattern, text_lower):
                issues.append(f"Potential fallacy: {description}")
        
        # Simple validity score
        validity_score = max(0, 1.0 - (len(issues) * 0.2))
        return validity_score, issues


class BasicBiasDetector:
    """Simple bias detection through pattern matching"""
    
    def __init__(self):
        self.bias_indicators = {
            'absolute_language': [r'\b(always|never|all|none|everyone|no one)\b'],
            'emotional_language': [r'\b(obviously|clearly|definitely|certainly)\b'],
            'technical_bias': [r'\b(simply|just|merely|only)\b.*\b(implement|code|system)\b'],
            'complexity_bias': [r'\b(comprehensive|complete|total|full)\b.*\b(solution|system|framework)\b']
        }
    
    def detect_bias(self, text: str) -> List[str]:
        """Return list of detected bias types"""
        text_lower = text.lower()
        detected_biases = []
        
        for bias_type, patterns in self.bias_indicators.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    detected_biases.append(bias_type)
                    break
        
        return detected_biases


class BasicCalibrationChecker:
    """Simple confidence vs uncertainty calibration"""
    
    def __init__(self):
        self.confidence_indicators = [
            r'\b(will|must|definitely|certainly|guaranteed)\b',
            r'\b(complete|comprehensive|total|full)\b',
            r'\b(always works|never fails|100%)\b'
        ]
        
        self.uncertainty_indicators = [
            r'\b(might|may|could|possibly|perhaps|likely)\b',
            r'\b(estimate|approximate|roughly|about)\b',
            r'\b(depends|varies|unclear|uncertain)\b'
        ]
    
    def check_calibration(self, text: str) -> Dict[str, float]:
        """Return calibration analysis"""
        text_lower = text.lower()
        
        confidence_count = sum(1 for pattern in self.confidence_indicators 
                             if re.search(pattern, text_lower))
        uncertainty_count = sum(1 for pattern in self.uncertainty_indicators 
                              if re.search(pattern, text_lower))
        
        total_statements = len(re.findall(r'[.!?]+', text))
        
        return {
            'confidence_ratio': confidence_count / max(1, total_statements),
            'uncertainty_ratio': uncertainty_count / max(1, total_statements),
            'calibration_balance': uncertainty_count / max(1, confidence_count + uncertainty_count)
        }


class SimpleREPEvaluator:
    """Main REP evaluation orchestrator"""
    
    def __init__(self):
        self.validity_checker = BasicLogicalValidityChecker()
        self.bias_detector = BasicBiasDetector()
        self.calibration_checker = BasicCalibrationChecker()
    
    def evaluate_text(self, text: str) -> RationalityMetrics:
        """Evaluate text using REP components"""
        
        # Logical validity check
        validity_score, validity_issues = self.validity_checker.check_logical_validity(text)
        
        # Bias detection
        bias_indicators = self.bias_detector.detect_bias(text)
        
        # Calibration check
        calibration_data = self.calibration_checker.check_calibration(text)
        calibration_score = calibration_data['calibration_balance']
        
        # Check for uncertainty acknowledgment
        uncertainty_present = calibration_data['uncertainty_ratio'] > 0.1
        
        return RationalityMetrics(
            logical_validity_score=validity_score,
            bias_indicators=bias_indicators,
            confidence_calibration=calibration_score,
            uncertainty_acknowledgment=uncertainty_present
        )
    
    def print_evaluation(self, text: str, title: str = "REP Evaluation"):
        """Print detailed evaluation results"""
        metrics = self.evaluate_text(text)
        
        print(f"\n=== {title} ===")
        print(f"Logical Validity Score: {metrics.logical_validity_score:.2f}/1.0")
        print(f"Bias Indicators: {', '.join(metrics.bias_indicators) if metrics.bias_indicators else 'None detected'}")
        print(f"Calibration Score: {metrics.confidence_calibration:.2f}/1.0")
        print(f"Uncertainty Acknowledgment: {'Yes' if metrics.uncertainty_acknowledgment else 'No'}")
        
        # Overall rationality score
        overall = (metrics.logical_validity_score + 
                  metrics.confidence_calibration + 
                  (1 if metrics.uncertainty_acknowledgment else 0) -
                  len(metrics.bias_indicators) * 0.1) / 3
        overall = max(0, min(1, overall))
        
        print(f"Overall Rationality Score: {overall:.2f}/1.0")
        return overall


def test_rep_on_sample_texts():
    """Test REP on various sample texts"""
    evaluator = SimpleREPEvaluator()
    
    # Test samples
    samples = {
        "Overconfident": "This system will definitely work perfectly and solve all problems. It always produces correct results.",
        "Balanced": "This approach might work well in many cases, though we should test it carefully and expect some limitations.",
        "Biased": "Obviously, everyone knows that this simple solution is the only way to implement such systems.",
        "Contradictory": "This method always works and never fails, but sometimes it might not be reliable."
    }
    
    results = {}
    for name, text in samples.items():
        score = evaluator.print_evaluation(text, f"Sample: {name}")
        results[name] = score
    
    print(f"\n=== REP Test Results Summary ===")
    for name, score in results.items():
        print(f"{name}: {score:.2f}")
    
    return results


if __name__ == "__main__":
    print("Testing Rationality Enhancement Protocol - Basic Implementation")
    test_rep_on_sample_texts()