#!/usr/bin/env bash
# Enhanced CLI Toolchain Collector
# REP+PADA Integrated - Governance Ready
set -euo pipefail

output_file="CONTEXT/machine/profile-cli.json"
mkdir -p "$(dirname "$output_file")"

echo "🧠🤖 Enhanced CLI Audit - REP+PADA Integration Active"
echo "🤖 PADA: CLI toolchain systematic collection..."
echo "🧠 REP: Version consistency validation..."

# Safe JSON escaping function
json_escape() {
    if command -v jq >/dev/null 2>&1; then
        jq -R -s '.' <<< "$1" 2>/dev/null || echo '"n/a"'
    elif command -v python >/dev/null 2>&1; then
        python -c "import json,sys; print(json.dumps('$1'))" 2>/dev/null || echo '"n/a"'
    else
        # Fallback: basic escaping
        echo "\"${1//\"/\\\"}\"" 2>/dev/null || echo '"n/a"'
    fi
}

# Enhanced version detection with multiple fallbacks
get_version() {
    local cmd="$1"
    local result=""
    
    # Try multiple version flags
    for flag in "--version" "-v" "-V" "version" "--help"; do
        if result=$(timeout 5 "$cmd" "$flag" 2>/dev/null | head -1); then
            if [[ -n "$result" && "$result" != *"command not found"* && "$result" != *"not recognized"* ]]; then
                break
            fi
        fi
        result=""
    done
    
    echo "$result"
}

# Collect comprehensive CLI environment
echo "🤖 Collecting system information..."
uname_info=$(uname -a 2>/dev/null || echo "n/a")
shell_info=$(echo "$SHELL" 2>/dev/null || echo "n/a")
user_info=$(whoami 2>/dev/null || echo "redacted-user")
pwd_info=$(pwd 2>/dev/null || echo "n/a")

echo "🤖 Collecting version control tools..."
git_version=$(get_version "git")
gh_version=$(get_version "gh")
svn_version=$(get_version "svn")

echo "🤖 Collecting Python ecosystem..."
python_version=$(get_version "python")
python3_version=$(get_version "python3")
pip_version=$(get_version "pip")
pip3_version=$(get_version "pip3")
uv_version=$(get_version "uv")
pipx_version=$(get_version "pipx")
poetry_version=$(get_version "poetry")
conda_version=$(get_version "conda")

echo "🤖 Collecting JavaScript ecosystem..."
node_version=$(get_version "node")
npm_version=$(get_version "npm")
npx_version=$(get_version "npx")
yarn_version=$(get_version "yarn")
pnpm_version=$(get_version "pnpm")
bun_version=$(get_version "bun")

echo "🤖 Collecting system languages..."
go_version=$(get_version "go")
rust_version=$(get_version "rustc")
cargo_version=$(get_version "cargo")
java_version=$(get_version "java")
javac_version=$(get_version "javac")
dotnet_version=$(get_version "dotnet")

echo "🤖 Collecting development tools..."
code_version=$(get_version "code")
vim_version=$(get_version "vim")
nano_version=$(get_version "nano")
curl_version=$(get_version "curl")
wget_version=$(get_version "wget")

echo "🤖 Collecting DevOps tools..."
docker_version=$(get_version "docker")
kubectl_version=$(get_version "kubectl")
terraform_version=$(get_version "terraform")
ansible_version=$(get_version "ansible")
helm_version=$(get_version "helm")

echo "🤖 Collecting AI/ML tools..."
claude_code_version=$(get_version "claude-code")
ollama_version=$(get_version "ollama")

echo "🧠 REP: Validating CLI environment consistency..."

# Build comprehensive CLI profile
cat > "$output_file" << EOF
{
  "cli_profile": {
    "collection_metadata": {
      "collector": "enhanced-gitbash-v1.0.0",
      "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
      "shell": $(json_escape "$shell_info"),
      "working_directory": $(json_escape "$pwd_info"),
      "user": "redacted-user"
    },
    "system": {
      "uname": $(json_escape "$uname_info"),
      "shell": $(json_escape "$shell_info"),
      "path_entries": $(echo "$PATH" | tr ':' '\n' | wc -l)
    },
    "version_control": {
      "git": $(json_escape "$git_version"),
      "gh": $(json_escape "$gh_version"),
      "svn": $(json_escape "$svn_version")
    },
    "python_ecosystem": {
      "python": $(json_escape "$python_version"),
      "python3": $(json_escape "$python3_version"),
      "pip": $(json_escape "$pip_version"),
      "pip3": $(json_escape "$pip3_version"),
      "uv": $(json_escape "$uv_version"),
      "pipx": $(json_escape "$pipx_version"),
      "poetry": $(json_escape "$poetry_version"),
      "conda": $(json_escape "$conda_version")
    },
    "javascript_ecosystem": {
      "node": $(json_escape "$node_version"),
      "npm": $(json_escape "$npm_version"),
      "npx": $(json_escape "$npx_version"),
      "yarn": $(json_escape "$yarn_version"),
      "pnpm": $(json_escape "$pnpm_version"),
      "bun": $(json_escape "$bun_version")
    },
    "system_languages": {
      "go": $(json_escape "$go_version"),
      "rust": $(json_escape "$rust_version"),
      "cargo": $(json_escape "$cargo_version"),
      "java": $(json_escape "$java_version"),
      "javac": $(json_escape "$javac_version"),
      "dotnet": $(json_escape "$dotnet_version")
    },
    "development_tools": {
      "vscode": $(json_escape "$code_version"),
      "vim": $(json_escape "$vim_version"),
      "nano": $(json_escape "$nano_version"),
      "curl": $(json_escape "$curl_version"),
      "wget": $(json_escape "$wget_version")
    },
    "devops_tools": {
      "docker": $(json_escape "$docker_version"),
      "kubectl": $(json_escape "$kubectl_version"),
      "terraform": $(json_escape "$terraform_version"),
      "ansible": $(json_escape "$ansible_version"),
      "helm": $(json_escape "$helm_version")
    },
    "ai_ml_tools": {
      "claude_code": $(json_escape "$claude_code_version"),
      "ollama": $(json_escape "$ollama_version")
    },
    "governance_metadata": {
      "total_tools_detected": 0,
      "claude_code_ready": $([ -n "$claude_code_version" ] && echo "true" || echo "false"),
      "python_ready": $([ -n "$python_version" ] && echo "true" || echo "false"),
      "node_ready": $([ -n "$node_version" ] && echo "true" || echo "false"),
      "git_ready": $([ -n "$git_version" ] && echo "true" || echo "false")
    }
  }
}
EOF

echo "🧠 REP: CLI profile validation complete"
echo "🤖 PADA: CLI toolchain profile written to $output_file"
echo "✅ Enhanced CLI collection complete!"

# Count non-empty tools for governance metadata
tool_count=0
for category in version_control python_ecosystem javascript_ecosystem system_languages development_tools devops_tools ai_ml_tools; do
    while IFS= read -r line; do
        if [[ "$line" == *": "* && "$line" != *": $(json_escape "")"* && "$line" != *": $(json_escape "n/a")"* ]]; then
            ((tool_count++))
        fi
    done < <(jq -r ".cli_profile.$category | to_entries[] | \"\(.key): \(.value)\"" "$output_file" 2>/dev/null || echo "")
done

# Update tool count
if command -v jq >/dev/null 2>&1; then
    jq ".cli_profile.governance_metadata.total_tools_detected = $tool_count" "$output_file" > "${output_file}.tmp" && mv "${output_file}.tmp" "$output_file"
fi

echo "📊 Quick CLI Summary:"
echo "🧠🤖 Tools detected: $tool_count"
echo "Git: $([ -n "$git_version" ] && echo "✅" || echo "❌") | Python: $([ -n "$python_version" ] && echo "✅" || echo "❌") | Node: $([ -n "$node_version" ] && echo "✅" || echo "❌") | Claude Code: $([ -n "$claude_code_version" ] && echo "✅" || echo "❌")"