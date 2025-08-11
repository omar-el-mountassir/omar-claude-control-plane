#!/usr/bin/env python3
"""
REP Optimization - Enhance patterns and accuracy
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'infrastructure/modules/operations/rationality'))
from rep import RationalityEnhancementProtocol

def optimize_bias_detection():
    """Optimize bias detection patterns"""
    print("=== BIAS DETECTION OPTIMIZATION ===")
    
    # Test current patterns against known cases
    test_cases = [
        # Should NOT trigger bias (false positives to fix)
        ("Scientific Statement", "Research indicates that approximately 70% of participants showed improvement.", False),
        ("Qualified Claim", "This method typically works well under normal conditions.", False),
        ("Hedged Technical", "The algorithm generally performs efficiently for most datasets.", False),
        
        # SHOULD trigger bias (true positives to maintain)
        ("Absolute Claim", "This always works perfectly in every situation.", True),
        ("Emotional Certainty", "Obviously everyone knows this is clearly the best solution.", True),
        ("Overconfident Tech", "This simple implementation will solve all your problems completely.", True),
    ]
    
    rep = RationalityEnhancementProtocol()
    false_positives = []
    false_negatives = []
    
    for name, text, should_have_bias in test_cases:
        result = rep.evaluate_text(text)
        has_bias = len(result.bias_indicators) > 0
        
        print(f"{name}: Bias={len(result.bias_indicators)}, Score={result.overall_score:.3f}")
        
        if should_have_bias and not has_bias:
            false_negatives.append(name)
        elif not should_have_bias and has_bias:
            false_positives.append((name, result.bias_indicators))
    
    print(f"\nFalse Positives: {false_positives}")
    print(f"False Negatives: {false_negatives}")
    
    return false_positives, false_negatives

def test_calibration_accuracy():
    """Test calibration detection accuracy"""
    print("\n=== CALIBRATION ACCURACY TESTING ===")
    
    test_cases = [
        ("Well Calibrated", "This approach might work in many cases, though results could vary.", 0.7),
        ("Over-Confident", "This will definitely work perfectly in all cases guaranteed.", 0.2),
        ("Under-Confident", "Maybe this could possibly work perhaps sometimes potentially.", 0.8),
        ("Balanced Mix", "While this often works well, some cases may require different approaches.", 0.8),
    ]
    
    rep = RationalityEnhancementProtocol()
    calibration_issues = []
    
    for name, text, expected_min_score in test_cases:
        result = rep.evaluate_text(text)
        calibration = result.confidence_calibration
        
        print(f"{name}: Calibration={calibration:.3f}, Expected>={expected_min_score}")
        
        if calibration < expected_min_score:
            calibration_issues.append((name, calibration, expected_min_score))
    
    return calibration_issues

def create_enhanced_patterns():
    """Create enhanced detection patterns"""
    print("\n=== CREATING ENHANCED PATTERNS ===")
    
    # Enhanced bias patterns with better precision
    enhanced_patterns = {
        'absolute_language': [
            # More nuanced - avoid scientific/technical contexts
            r'\b(always|never)\b(?!.*\b(research|study|data|evidence|cases|conditions)\b)',
            r'\b(all|none)\b\s+(?!of\s+the\s+(research|data|cases))',
            r'\beveryone\s+(knows|agrees|says)\b',
            r'\bno\s+one\s+(can|will|should)\b'
        ],
        'overconfidence': [
            r'\b(definitely|certainly|guaranteed|undoubtedly)\b.*\b(will|works?|solves?)\b',
            r'\b(perfect|complete|total)\b.*\b(solution|fix|answer)\b',
            r'\b100%\s+(effective|accurate|successful)\b'
        ],
        'complexity_bias': [
            r'\b(comprehensive|complete|ultimate|perfect)\b.*\b(solution|system|approach)\b',
            r'\bthis\s+(simple|easy)\b.*\b(solves?|fixes?)\b.*\b(everything|all)\b'
        ]
    }
    
    # Enhanced uncertainty detection
    enhanced_uncertainty = [
        r'\b(might|may|could|possibly|perhaps|potentially|likely|probably)\b',
        r'\b(appears?|seems?|suggests?|indicates?)\b.*\bthat\b',
        r'\bin\s+most\s+cases\b|\btypically\b|\busually\b|\bgenerally\b',
        r'\b(preliminary|initial|tentative)\b.*\b(results?|findings?)\b',
        r'\bdepending\s+on\b|\bunder\s+certain\s+conditions\b'
    ]
    
    print(f"Enhanced absolute patterns: {len(enhanced_patterns['absolute_language'])}")
    print(f"Enhanced overconfidence patterns: {len(enhanced_patterns['overconfidence'])}")
    print(f"Enhanced uncertainty patterns: {len(enhanced_uncertainty)}")
    
    return enhanced_patterns, enhanced_uncertainty

def test_performance_optimization():
    """Test performance optimization opportunities"""
    print("\n=== PERFORMANCE OPTIMIZATION ===")
    
    import time
    rep = RationalityEnhancementProtocol()
    
    # Test different text lengths
    texts = [
        "Short text for testing.",
        "Medium length text that contains several sentences with various patterns. " * 5,
        "Long text with many sentences and complex patterns to test performance. " * 20,
        "Very long text with extensive content for performance benchmarking. " * 100
    ]
    
    times = []
    for i, text in enumerate(texts):
        start_time = time.time()
        result = rep.evaluate_text(text)
        end_time = time.time()
        
        duration = end_time - start_time
        times.append(duration)
        print(f"Text {i+1} ({len(text)} chars): {duration:.4f}s")
    
    # Check for performance issues
    if times[-1] > 0.1:  # Very long text taking >100ms
        print("⚠️ Performance issue: Long text processing too slow")
        return True
    
    return False

def main():
    """Run REP optimization analysis"""
    print("REP OPTIMIZATION ANALYSIS")
    print("=" * 50)
    
    # Test bias detection
    false_pos, false_neg = optimize_bias_detection()
    
    # Test calibration accuracy
    calibration_issues = test_calibration_accuracy()
    
    # Create enhanced patterns
    enhanced_patterns, enhanced_uncertainty = create_enhanced_patterns()
    
    # Test performance
    perf_issues = test_performance_optimization()
    
    print(f"\n=== OPTIMIZATION SUMMARY ===")
    print(f"False Positives in Bias Detection: {len(false_pos)}")
    print(f"False Negatives in Bias Detection: {len(false_neg)}")
    print(f"Calibration Issues: {len(calibration_issues)}")
    print(f"Performance Issues: {'Yes' if perf_issues else 'No'}")
    
    if false_pos or false_neg or calibration_issues:
        print("\n📝 Recommendations:")
        if false_pos:
            print("  - Refine bias patterns to reduce false positives")
        if false_neg:
            print("  - Add patterns to catch missed bias cases")
        if calibration_issues:
            print("  - Improve calibration scoring algorithm")
        if perf_issues:
            print("  - Optimize regex patterns for better performance")
    else:
        print("\n✅ REP performance and accuracy are well optimized")

if __name__ == "__main__":
    main()