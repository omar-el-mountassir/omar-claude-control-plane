#!/usr/bin/env python3
"""
REP Diagnostic Testing - Find and Fix Issues
"""

import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'infrastructure/modules/operations/rationality'))
from rep import RationalityEnhancementProtocol, detailed_rationality_analysis

def test_performance():
    """Test REP performance and identify bottlenecks"""
    print("=== PERFORMANCE TESTING ===")
    rep = RationalityEnhancementProtocol()
    
    # Test various text lengths
    test_texts = [
        ("Short", "This works well."),
        ("Medium", "This approach seems to work well in many cases. " * 10),
        ("Long", "This comprehensive system definitely works perfectly. " * 50),
        ("Very Long", "Obviously this complete solution always delivers results. " * 200)
    ]
    
    for name, text in test_texts:
        start_time = time.time()
        result = rep.evaluate_text(text)
        end_time = time.time()
        
        print(f"{name} ({len(text)} chars): {end_time - start_time:.3f}s - Score: {result.overall_score:.3f}")

def test_accuracy_edge_cases():
    """Test REP accuracy on edge cases"""
    print("\n=== ACCURACY EDGE CASE TESTING ===")
    rep = RationalityEnhancementProtocol()
    
    edge_cases = [
        ("Empty", ""),
        ("Single Word", "Hello"),
        ("Questions Only", "What should we do? How can we proceed? Why is this happening?"),
        ("All Uncertainty", "Maybe this might possibly work perhaps under certain conditions potentially."),
        ("Technical Jargon", "The API endpoint utilizes RESTful architecture with OAuth2 authentication."),
        ("Mixed Languages", "This works bien and functions correctement in most cas."),
        ("Numbers Heavy", "Version 2.3.1 increased performance by 15% with 99.9% uptime."),
        ("Quoted Text", '"This always works," he said confidently, "and never fails completely."')
    ]
    
    issues = []
    for name, text in edge_cases:
        try:
            result = rep.evaluate_text(text)
            score = result.overall_score
            bias_count = len(result.bias_indicators)
            print(f"{name}: Score {score:.3f}, Bias: {bias_count}")
            
            # Check for obvious issues
            if name == "Empty" and score > 0:
                issues.append("Empty text should have low/zero score")
            if name == "All Uncertainty" and score < 0.8:
                issues.append("High uncertainty text should score well")
            if name == "Questions Only" and bias_count > 0:
                issues.append("Questions should not trigger bias detection")
                
        except Exception as e:
            issues.append(f"{name} caused error: {e}")
            print(f"{name}: ERROR - {e}")
    
    return issues

def test_false_positives():
    """Test for false positive bias detection"""
    print("\n=== FALSE POSITIVE TESTING ===")
    rep = RationalityEnhancementProtocol()
    
    good_texts = [
        ("Scientific", "The study suggests that this approach may be effective in approximately 70% of cases, though further research is needed."),
        ("Hedged", "This solution typically works well, though results may vary depending on specific circumstances and requirements."),
        ("Balanced", "While this method has shown promise, we should carefully consider potential limitations and alternative approaches."),
        ("Provisional", "Initial results indicate this could be helpful, pending additional validation and testing."),
        ("Qualified", "Under normal conditions, this approach generally provides satisfactory results for most use cases.")
    ]
    
    false_positives = []
    for name, text in good_texts:
        result = rep.evaluate_text(text)
        if result.overall_score < 0.7:  # These should score well
            false_positives.append(f"{name}: {result.overall_score:.3f} (should be high)")
        if len(result.bias_indicators) > 1:  # Should have minimal bias
            false_positives.append(f"{name}: {len(result.bias_indicators)} bias indicators (should be low)")
        
        print(f"{name}: Score {result.overall_score:.3f}, Bias: {len(result.bias_indicators)}")
    
    return false_positives

def test_consistency():
    """Test REP consistency across multiple runs"""
    print("\n=== CONSISTENCY TESTING ===")
    rep = RationalityEnhancementProtocol()
    
    test_text = "This system will definitely work perfectly and solve all problems completely."
    scores = []
    
    for i in range(5):
        result = rep.evaluate_text(test_text)
        scores.append(result.overall_score)
    
    consistency_score = max(scores) - min(scores)
    print(f"Score variation: {consistency_score:.6f} (should be 0.0)")
    print(f"Scores: {scores}")
    
    return consistency_score > 0.001  # Flag if inconsistent

def identify_improvements():
    """Identify specific areas for improvement"""
    print("\n=== IMPROVEMENT IDENTIFICATION ===")
    
    # Run all diagnostic tests
    performance_issues = []
    accuracy_issues = test_accuracy_edge_cases()
    false_positives = test_false_positives()
    consistency_issue = test_consistency()
    
    improvements = []
    
    if accuracy_issues:
        improvements.extend([f"Accuracy: {issue}" for issue in accuracy_issues])
    
    if false_positives:
        improvements.extend([f"False Positive: {issue}" for issue in false_positives])
    
    if consistency_issue:
        improvements.append("Consistency: Results vary between runs")
    
    return improvements

def main():
    """Run comprehensive diagnostic testing"""
    print("REP DIAGNOSTIC TESTING")
    print("=" * 50)
    
    # Performance testing
    test_performance()
    
    # Identify issues and improvements
    improvements = identify_improvements()
    
    print(f"\n=== DIAGNOSTIC SUMMARY ===")
    if improvements:
        print("Issues Found:")
        for issue in improvements:
            print(f"  - {issue}")
    else:
        print("✓ No significant issues found")
    
    print(f"\nTotal Issues: {len(improvements)}")
    
    return improvements

if __name__ == "__main__":
    issues = main()
    if issues:
        print(f"\n{len(issues)} issues found - proceeding with fixes...")
    else:
        print("\n✓ System health confirmed")