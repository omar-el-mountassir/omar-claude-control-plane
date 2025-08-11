#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Completeness Checker - Validates promises vs deliverables

Purpose: Prevent the systematic "assume everything is done properly" problem
by providing external validation of claimed completeness.

Critical Use Cases:
- Master index promises 13 files but only 2 exist
- Documentation references files that don't exist  
- System claims completion but missing key components

Usage:
  python completeness-checker.py --target claude-code-knowledge
  python completeness-checker.py --target global-system
  python completeness-checker.py --file path/to/specific/file.md
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Add path for shared utilities
sys.path.append(str(Path(__file__).parent.parent / "utils"))
from claude_utils import get_claude_dir

class CompletenessChecker:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.issues = []
        self.validated_files = 0
        self.total_references = 0
        
    def check_claude_code_knowledge(self) -> Dict:
        """Validate Claude Code knowledge base completeness"""
        knowledge_base = self.base_path / "global" / "knowledge" / "claude-code"
        
        if not knowledge_base.exists():
            return {"status": "error", "message": "Claude Code knowledge base not found"}
            
        print("🔍 Validating Claude Code Knowledge Base...")
        
        # Check master index completeness
        master_index = knowledge_base / "MASTER-INDEX.md"
        if master_index.exists():
            self._validate_master_index(master_index, knowledge_base)
        else:
            self.issues.append({
                "type": "missing_critical_file",
                "file": "MASTER-INDEX.md",
                "severity": "critical",
                "message": "Master index file missing"
            })
            
        # Check all markdown files for broken links
        self._validate_directory_links(knowledge_base)
        
        return self._generate_report("Claude Code Knowledge Base")
    
    def _validate_master_index(self, master_index_path: Path, base_dir: Path):
        """Validate master index promises vs reality"""
        content = master_index_path.read_text(encoding='utf-8')
        
        # Find all file references in format [text](path/to/file.md)
        link_pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
        references = re.findall(link_pattern, content)
        
        print(f"📊 Found {len(references)} file references in master index")
        self.total_references += len(references)
        
        missing_files = []
        existing_files = []
        
        for link_text, file_path in references:
            # Resolve relative path from master index location
            full_path = base_dir / file_path
            self.validated_files += 1
            
            if not full_path.exists():
                missing_files.append({
                    "link_text": link_text,
                    "promised_path": file_path,
                    "full_path": str(full_path),
                    "type": "missing_referenced_file"
                })
            else:
                existing_files.append(file_path)
                
        # Report results
        if missing_files:
            self.issues.append({
                "type": "broken_promises",
                "file": "MASTER-INDEX.md", 
                "severity": "critical",
                "message": f"Master index promises {len(references)} files but {len(missing_files)} are missing",
                "missing_files": missing_files,
                "existing_files": existing_files
            })
            
        print(f"✅ Existing files: {len(existing_files)}")
        print(f"❌ Missing files: {len(missing_files)}")
        
        # Specific gap analysis
        if len(missing_files) > 0:
            print(f"\n🚨 CRITICAL GAPS DETECTED:")
            for missing in missing_files:
                print(f"   • {missing['link_text']} → {missing['promised_path']}")
    
    def _validate_directory_links(self, directory: Path):
        """Validate all internal links in markdown files"""
        for md_file in directory.rglob("*.md"):
            if md_file.name != "MASTER-INDEX.md":  # Already checked
                self._validate_file_links(md_file, directory)
    
    def _validate_file_links(self, file_path: Path, base_dir: Path):
        """Validate links within a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            # Find relative markdown links
            link_pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
            references = re.findall(link_pattern, content)
            
            for link_text, relative_path in references:
                # Resolve from file's directory
                full_path = file_path.parent / relative_path
                self.validated_files += 1
                self.total_references += 1
                
                if not full_path.exists():
                    self.issues.append({
                        "type": "broken_link",
                        "file": str(file_path.relative_to(base_dir)),
                        "severity": "medium",
                        "link_text": link_text,
                        "broken_path": relative_path,
                        "message": f"Broken link: {link_text} → {relative_path}"
                    })
                    
        except Exception as e:
            self.issues.append({
                "type": "validation_error",
                "file": str(file_path.relative_to(base_dir)),
                "severity": "low", 
                "message": f"Could not validate file: {str(e)}"
            })
    
    def _generate_report(self, target_name: str) -> Dict:
        """Generate comprehensive validation report"""
        critical_issues = [i for i in self.issues if i["severity"] == "critical"]
        medium_issues = [i for i in self.issues if i["severity"] == "medium"]
        low_issues = [i for i in self.issues if i["severity"] == "low"]
        
        report = {
            "target": target_name,
            "status": "fail" if critical_issues else ("warning" if medium_issues else "pass"),
            "summary": {
                "total_files_validated": self.validated_files,
                "total_references_checked": self.total_references,
                "critical_issues": len(critical_issues),
                "medium_issues": len(medium_issues),
                "low_issues": len(low_issues)
            },
            "issues": self.issues
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print human-readable validation report"""
        print(f"\n{'='*50}")
        print(f"🔍 COMPLETENESS VALIDATION REPORT")
        print(f"{'='*50}")
        print(f"Target: {report['target']}")
        print(f"Status: {'🚨 FAIL' if report['status'] == 'fail' else '⚠️ WARNING' if report['status'] == 'warning' else '✅ PASS'}")
        
        summary = report['summary']
        print(f"\n📊 SUMMARY:")
        print(f"   Files Validated: {summary['total_files_validated']}")
        print(f"   References Checked: {summary['total_references_checked']}")
        print(f"   Critical Issues: {summary['critical_issues']}")
        print(f"   Medium Issues: {summary['medium_issues']}")
        print(f"   Low Issues: {summary['low_issues']}")
        
        # Print critical issues first
        critical_issues = [i for i in report['issues'] if i['severity'] == 'critical']
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES (MUST FIX):")
            for issue in critical_issues:
                print(f"   • {issue['message']}")
                if 'missing_files' in issue:
                    print(f"     Missing files:")
                    for missing in issue['missing_files'][:5]:  # Limit output
                        print(f"       - {missing['link_text']} → {missing['promised_path']}")
                    if len(issue['missing_files']) > 5:
                        print(f"       ... and {len(issue['missing_files']) - 5} more")
        
        # Print medium issues
        medium_issues = [i for i in report['issues'] if i['severity'] == 'medium']
        if medium_issues:
            print(f"\n⚠️ MEDIUM ISSUES (SHOULD FIX):")
            for issue in medium_issues[:10]:  # Limit output
                print(f"   • {issue['file']}: {issue['message']}")
            if len(medium_issues) > 10:
                print(f"   ... and {len(medium_issues) - 10} more medium issues")
                
        print(f"\n{'='*50}")
        
        # Exit with appropriate code
        if report['status'] == 'fail':
            return 1
        elif report['status'] == 'warning':
            return 2
        else:
            return 0

def main():
    """Main validation entry point with input validation"""
    
    # Input validation
    if len(sys.argv) < 2:
        print("Usage: python completeness-checker.py --target TARGET")
        print("       python completeness-checker.py --file FILE_PATH")
        print()
        print("Targets:")
        print("  claude-code-knowledge  - Validate Claude Code knowledge base")
        print("  global-system         - Validate global system (not implemented)")
        print()
        print("Examples:")
        print("  python completeness-checker.py --target claude-code-knowledge")
        print("  python completeness-checker.py --file path/to/file.md")
        sys.exit(1)
    
    # Validate argument count
    if len(sys.argv) > 3:
        print("❌ Error: Too many arguments")
        print("Usage: python completeness-checker.py --target TARGET")
        sys.exit(1)
    
    # Get Claude Code base directory
    base_path = get_claude_dir()
    if not base_path.exists():
        print(f"❌ Claude Code directory not found at {base_path}")
        sys.exit(1)
        
    checker = CompletenessChecker(str(base_path))
    
    # Parse and validate arguments
    command = sys.argv[1].strip()
    
    if command == "--target":
        if len(sys.argv) != 3:
            print("❌ Error: --target requires exactly one argument")
            print("Usage: python completeness-checker.py --target TARGET")
            sys.exit(1)
            
        target_type = sys.argv[2].strip()
        
        # Validate target type
        valid_targets = ["claude-code-knowledge", "global-system"]
        if target_type not in valid_targets:
            print(f"❌ Error: Unknown target '{target_type}'")
            print(f"Valid targets: {', '.join(valid_targets)}")
            sys.exit(1)
        
        if target_type == "claude-code-knowledge":
            report = checker.check_claude_code_knowledge()
        elif target_type == "global-system":
            print("❌ Global system validation not yet implemented")
            sys.exit(1)
            
    elif command == "--file":
        if len(sys.argv) != 3:
            print("❌ Error: --file requires exactly one argument")
            print("Usage: python completeness-checker.py --file FILE_PATH")
            sys.exit(1)
            
        file_path = sys.argv[2].strip()
        
        # Validate file path
        if not file_path:
            print("❌ Error: File path cannot be empty")
            sys.exit(1)
        
        target_file = Path(file_path)
        if not target_file.exists():
            print(f"❌ Error: File does not exist: {file_path}")
            sys.exit(1)
            
        if not target_file.is_file():
            print(f"❌ Error: Path is not a file: {file_path}")
            sys.exit(1)
        
        print("❌ Single file validation not yet implemented")
        sys.exit(1)
        
    else:
        print(f"❌ Error: Unknown command '{command}'")
        print("Valid commands: --target, --file")
        sys.exit(1)
    
    # Execute validation and print report
    try:
        exit_code = checker.print_report(report)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()