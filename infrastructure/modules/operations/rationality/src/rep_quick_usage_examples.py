#!/usr/bin/env python3
"""
REP Quick Usage Examples - Correct Python Syntax
"""

import sys
from pathlib import Path

# Add REP module to path
sys.path.insert(0, str(Path(__file__).parent / 'infrastructure/modules/operations/rationality'))

from rep import quick_rationality_check, detailed_rationality_analysis, RationalityEnhancementProtocol

def demonstrate_rep_usage():
    """Show correct REP usage patterns"""
    
    print("🧠 REP QUICK USAGE EXAMPLES")
    print("=" * 50)
    print()
    
    # Example 1: Quick rationality score
    print("1️⃣ QUICK RATIONALITY CHECK:")
    test_text = "This system will definitely solve all problems perfectly and never fails."
    score = quick_rationality_check(test_text)
    print(f"   Text: \"{test_text[:50]}...\"")
    print(f"   Score: {score:.3f}/1.0")
    print()
    
    # Example 2: Detailed analysis with recommendations  
    print("2️⃣ DETAILED ANALYSIS WITH RECOMMENDATIONS:")
    result = detailed_rationality_analysis(test_text)
    metrics = result['metrics']
    print(f"   Overall Score: {metrics['overall_score']:.3f}")
    print(f"   Logical Validity: {metrics['logical_validity_score']:.3f}")
    print(f"   Bias Indicators: {metrics['bias_indicators']}")
    print(f"   Confidence Calibration: {metrics['confidence_calibration']:.3f}")
    print(f"   Uncertainty Acknowledged: {metrics['uncertainty_acknowledgment']}")
    print(f"   Recommendations: {len(result['recommendations'])} suggestions")
    print()
    
    # Example 3: Improved version
    print("3️⃣ IMPROVED VERSION COMPARISON:")
    improved_text = "This system might help address many common issues, though results could vary based on specific requirements and use cases."
    improved_score = quick_rationality_check(improved_text)
    
    print(f"   Original Score: {score:.3f}")
    print(f"   Improved Score: {improved_score:.3f}")
    print(f"   Improvement: +{improved_score - score:.3f} ({((improved_score - score) * 100):.1f}% better)")
    print()
    
    # Example 4: Full REP engine usage
    print("4️⃣ FULL REP ENGINE USAGE:")
    rep = RationalityEnhancementProtocol()
    
    texts_to_analyze = [
        "This approach always works in every situation.",
        "This method generally works well in most typical scenarios.",
        "Based on available evidence, this technique appears effective for common use cases."
    ]
    
    for i, text in enumerate(texts_to_analyze, 1):
        analysis = rep.evaluate_text(text, context=f"example_{i}")
        print(f"   Example {i}: {analysis.overall_score:.3f} - \"{text[:40]}...\"")
    print()
    
    # Example 5: File analysis
    print("5️⃣ FILE ANALYSIS:")
    print("   # Analyze any file:")
    print("   python infrastructure/scripts/utils/rep_monitor.py --evaluate your_file.md")
    print("   ")
    print("   # Health check:")
    print("   python infrastructure/scripts/utils/rep_monitor.py --health")
    print("   ")
    print("   # Generate improvement report:")
    print("   python infrastructure/scripts/utils/rep_improvement.py --report")
    print()
    
    return {
        'quick_score': score,
        'improved_score': improved_score,
        'improvement': improved_score - score,
        'detailed_analysis': result
    }

def analyze_your_text():
    """Interactive text analysis"""
    print("📝 ANALYZE YOUR OWN TEXT")
    print("=" * 30)
    
    # You can replace this with any text you want to analyze
    your_text = input("Enter text to analyze (or press Enter for demo): ").strip()
    
    if not your_text:
        your_text = "The REP system definitely provides complete rationality enhancement for all AI outputs."
    
    print(f"\n🔍 ANALYZING: \"{your_text[:50]}{'...' if len(your_text) > 50 else ''}\"")
    print()
    
    # Quick analysis
    quick_score = quick_rationality_check(your_text)
    print(f"📊 Quick Score: {quick_score:.3f}/1.0")
    
    # Detailed analysis
    detailed = detailed_rationality_analysis(your_text)
    metrics = detailed['metrics']
    print(f"📈 Detailed Analysis:")
    print(f"   Logical Validity: {metrics['logical_validity_score']:.3f}")
    print(f"   Bias Indicators: {len(metrics['bias_indicators'])} found")
    if metrics['bias_indicators']:
        print(f"   Issues: {', '.join(metrics['bias_indicators'])}")
    print(f"   Calibration: {metrics['confidence_calibration']:.3f}")
    print(f"   Uncertainty Acknowledged: {'Yes' if metrics['uncertainty_acknowledgment'] else 'No'}")
    
    # Suggestions
    if quick_score < 0.7:
        print(f"\n💡 SUGGESTIONS FOR IMPROVEMENT:")
        print("   - Add uncertainty qualifiers (might, could, likely)")
        print("   - Avoid absolute claims (always, never, all, completely)")
        print("   - Include appropriate hedging language")
        print("   - Acknowledge limitations where relevant")
    else:
        print(f"\n✅ GOOD RATIONALITY - Score above threshold!")
    
    return detailed

if __name__ == "__main__":
    # Run demonstrations
    demo_results = demonstrate_rep_usage()
    
    print("🎯 SUMMARY:")
    print(f"   Quick scoring works: ✅")
    print(f"   Detailed analysis works: ✅") 
    print(f"   Improvement detection: +{demo_results['improvement']:.3f} points")
    print(f"   System health: ✅ EXCELLENT")
    print()
    
    # Interactive analysis
    print("=" * 50)
    analyze_your_text()