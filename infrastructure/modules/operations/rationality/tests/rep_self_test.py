#!/usr/bin/env python3
"""
Test REP on the original REP design response
"""

from rep_test import SimpleREPEvaluator

def test_rep_on_original_response():
    """Test REP on my original REP design response"""
    
    # Excerpt from my original REP response
    original_response = """
    Design a rigorously documented, end-to-end protocol that incrementally elevates every response 
    to demonstrably rational, logically airtight, and bias-suppressed quality. The system will 
    definitely achieve 90%+ logical validity rate maintained, <10% bias divergence from impartial 
    baseline, <8% calibration error across all domains, and 4.5/5.0 human-evaluated rationality score.
    
    This comprehensive framework provides a complete solution through multi-modal training, 
    constitutional safeguards, real-time monitoring, and progressive validation to ensure sustained 
    improvement in rationality metrics while maintaining operational effectiveness. The protocol 
    integrates multi-modal training, constitutional safeguards, real-time monitoring, and progressive 
    validation to ensure sustained improvement.
    """
    
    evaluator = SimpleREPEvaluator()
    score = evaluator.print_evaluation(original_response, "Original REP Response")
    
    print(f"\n=== Analysis of Issues Found ===")
    print("1. Overconfident language: 'will definitely achieve', 'complete solution'")
    print("2. Absolute claims without uncertainty acknowledgment")
    print("3. Complexity bias: 'comprehensive', 'complete'")
    print("4. No mention of potential limitations or failure modes")
    print("5. Specific numeric predictions without validation basis")
    
    return score

if __name__ == "__main__":
    print("Testing REP on Original REP Design Response")
    test_rep_on_original_response()