
# Omar's Prompt for Claude Code: Repomix Workflow

Explore Repomix and evaluate its effectiveness for preparing codebases for AI analysis. Use Repomix to pack the repository into an AI-friendly format (XML, Markdown, or Plain Text). Consider the following workflow:

1. Run Repomix with compression to optimize token usage:

```bash
repomix --compress --style xml
```

2. Optionally, add a custom instruction file for tailored AI guidance:

```bash
repomix --instruction-file-path repomix-instruction.md
```

3. Review the output file (e.g., `repomix-output.xml`) and use it as input for LLMs (Claude, ChatGPT, etc.).
4. Example prompt for AI:

```text
This file contains my entire codebase, packed for AI analysis. Please review the overall structure and suggest improvements, focusing on maintainability and scalability. If possible, generate documentation and test cases based on the code.
```

Tips:

- Use `--token-count-tree` to visualize token usage and optimize for LLM context limits.
- Exclude sensitive or unnecessary files using `.gitignore`, `.repomixignore`, or CLI options.
- For large repos, use `--compress` and targeted include/exclude patterns.
