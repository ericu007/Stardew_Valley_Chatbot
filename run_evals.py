import sys
import os 

# 1. Manually add the "evals" folder to Python's path
sys.path.insert(0, os.path.abspath("evals"))

# 2. Now we can import them directly just like pytest does
from conftest import get_review, judge_with_golden, judge_with_rubric
from test_rules import RULE_CASES
from test_golden import GOLDEN_EXAMPLES
from test_rubric import CASES, RUBRIC

def run_evals():
    # Dictionary to track our passes and totals by category
    metrics = {
        "In-Domain Rules": {"pass": 0, "total": 0},
        "Out-of-Scope Rules": {"pass": 0, "total": 0},
        "Adversarial/Safety Rules": {"pass": 0, "total": 0},
        "Golden-Reference MaaJ": {"pass": 0, "total": 0},
        "Rubric MaaJ": {"pass": 0, "total": 0},
    }

    print("🚀 Starting Evaluation Harness...\n")

    # --- 1. Deterministic Rule Tests ---
    print("Running Deterministic Rule Tests...")
    for case in RULE_CASES:
        # Determine category based on the test name
        if case["name"].startswith("in_domain"):
            cat = "In-Domain Rules"
        elif case["name"].startswith("out_of_scope"):
            cat = "Out-of-Scope Rules"
        elif case["name"].startswith("adversarial"):
            cat = "Adversarial/Safety Rules"
        else:
            continue

        metrics[cat]["total"] += 1
        response = get_review(case["input"])
        
        # Deterministic check
        if case["expected"].lower() in response.lower():
            metrics[cat]["pass"] += 1
        else:
            print(f"  [FAIL] {case['name']} | Expected: '{case['expected']}' | Got: {response}")

    # --- 2. Golden-Reference MaaJ Tests ---
    print("Running Golden-Reference MaaJ Tests...")
    for case in GOLDEN_EXAMPLES:
        metrics["Golden-Reference MaaJ"]["total"] += 1
        response = get_review(case["q"])
        rating = judge_with_golden(case["q"], case["ref"], response)
        
        if rating >= 6:
            metrics["Golden-Reference MaaJ"]["pass"] += 1
        else:
            print(f"  [FAIL] Golden '{case['q']}' | Score: {rating}/10")

    # --- 3. Rubric MaaJ Tests ---
    print("Running Rubric MaaJ Tests...")
    for q in CASES:
        metrics["Rubric MaaJ"]["total"] += 1
        response = get_review(q)
        rating = judge_with_rubric(q, response, RUBRIC)
        
        if rating >= 7:
            metrics["Rubric MaaJ"]["pass"] += 1
        else:
            print(f"  [FAIL] Rubric '{q}' | Score: {rating}/10")

    # --- 4. Print Summary ---
    print("\n" + "="*45)
    print(" 📊 EVALUATION PASS RATES BY CATEGORY")
    print("="*45)
    
    total_passed = 0
    total_tests = 0
    
    for category, stats in metrics.items():
        if stats["total"] > 0:
            pass_rate = (stats["pass"] / stats["total"]) * 100
            print(f"{category.ljust(26)}: {stats['pass']}/{stats['total']} ({pass_rate:.1f}%)")
            
            total_passed += stats["pass"]
            total_tests += stats["total"]
            
    print("-" * 45)
    overall_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    print(f"OVERALL PASS RATE         : {total_passed}/{total_tests} ({overall_rate:.1f}%)")
    print("="*45)

if __name__ == "__main__":
    run_evals()