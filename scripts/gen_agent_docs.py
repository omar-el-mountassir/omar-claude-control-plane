#!/usr/bin/env python3
"""
Agent Documentation Generator - 150-word compliance enforcer
Reads agents/ directory, generates compliant docs/agents/*.md files
"""

import os
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

class AgentDocGenerator:
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        
        self.base_path = base_path
        self.agents_path = base_path / "agents"
        self.docs_agents_path = base_path / "docs" / "docs" / "agents"
        self.templates_path = base_path / "templates"
        
        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(str(self.templates_path)))
        self.template = self.env.get_template('agent_doc.md.j2')
    
    def count_words(self, text: str) -> int:
        """Count words in text, excluding markdown formatting"""
        # Remove markdown formatting
        clean_text = re.sub(r'[#*`\-]', '', text)
        # Split and count words
        words = clean_text.split()
        return len(words)
    
    def extract_agent_info(self, agent_file: Path) -> dict:
        """Extract agent information from markdown file"""
        if not agent_file.exists():
            return None
        
        content = agent_file.read_text(encoding='utf-8')
        
        # Extract title/name
        name_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        agent_name = name_match.group(1) if name_match else agent_file.stem
        
        # Extract sections
        purpose_match = re.search(r'(?:purpose|overview|description):\s*(.+?)(?:\n\n|\Z)', content, re.IGNORECASE | re.DOTALL)
        purpose_statement = purpose_match.group(1).strip() if purpose_match else "Purpose not defined"
        
        # Try to extract core functions
        functions_match = re.search(r'(?:functions|capabilities|features):\s*(.+?)(?:\n\n|\Z)', content, re.IGNORECASE | re.DOTALL)
        core_functions = functions_match.group(1).strip() if functions_match else "Functions not defined"
        
        # Try to extract constraints
        constraints_match = re.search(r'(?:constraints|limitations|requirements):\s*(.+?)(?:\n\n|\Z)', content, re.IGNORECASE | re.DOTALL)
        constraints = constraints_match.group(1).strip() if constraints_match else "No constraints specified"
        
        # Try to extract examples
        examples_match = re.search(r'(?:examples|usage):\s*(.+?)(?:\n\n|\Z)', content, re.IGNORECASE | re.DOTALL)
        usage_examples = examples_match.group(1).strip() if examples_match else None
        
        return {
            'agent_name': agent_name,
            'purpose_statement': purpose_statement,
            'core_functions': core_functions,
            'constraints': constraints,
            'usage_examples': usage_examples
        }
    
    def generate_doc(self, agent_info: dict) -> str:
        """Generate documentation using template"""
        # Calculate total word count
        total_text = f"{agent_info['purpose_statement']} {agent_info['core_functions']} {agent_info['constraints']}"
        if agent_info['usage_examples']:
            total_text += f" {agent_info['usage_examples']}"
        
        word_count = self.count_words(total_text)
        
        # Render template
        return self.template.render(
            **agent_info,
            word_count=word_count,
            last_updated=datetime.now().strftime('%Y-%m-%d')
        )
    
    def scan_agents(self):
        """Scan agents directory and generate documentation"""
        if not self.agents_path.exists():
            print(f"❌ Agents directory not found: {self.agents_path}")
            return
        
        # Create docs directory if needed
        self.docs_agents_path.mkdir(parents=True, exist_ok=True)
        
        agents_found = 0
        agents_generated = 0
        compliance_failures = 0
        
        # Scan all .md files in agents directory
        for agent_file in self.agents_path.glob("**/*.md"):
            agents_found += 1
            print(f"📋 Processing: {agent_file.stem}")
            
            # Extract agent info
            agent_info = self.extract_agent_info(agent_file)
            if not agent_info:
                print(f"⚠️  Could not extract info from {agent_file.stem}")
                continue
            
            # Generate documentation
            doc_content = self.generate_doc(agent_info)
            
            # Check compliance
            word_count = self.count_words(f"{agent_info['purpose_statement']} {agent_info['core_functions']} {agent_info['constraints']}")
            if agent_info['usage_examples']:
                word_count += self.count_words(agent_info['usage_examples'])
            
            if word_count > 150:
                compliance_failures += 1
                print(f"❌ COMPLIANCE FAIL: {agent_file.stem} ({word_count}/150 words)")
            else:
                print(f"✅ COMPLIANCE PASS: {agent_file.stem} ({word_count}/150 words)")
            
            # Write documentation
            output_file = self.docs_agents_path / f"{agent_file.stem}.md"
            output_file.write_text(doc_content, encoding='utf-8')
            agents_generated += 1
        
        print(f"\n📊 Generation Summary:")
        print(f"   Agents found: {agents_found}")
        print(f"   Docs generated: {agents_generated}")
        print(f"   Compliance failures: {compliance_failures}")
        
        if compliance_failures > 0:
            print(f"❌ {compliance_failures} agents exceed 150-word limit!")
            return False
        else:
            print("✅ All agents comply with 150-word standard!")
            return True

def main():
    generator = AgentDocGenerator()
    success = generator.scan_agents()
    exit(0 if success else 1)

if __name__ == "__main__":
    main()