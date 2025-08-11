# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
shopt -s expand_aliases
# Check for rg availability
if ! command -v rg >/dev/null 2>&1; then
  alias rg=''\''C:\Users\omarm\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\vendor\ripgrep\x64-win32\rg.exe'\'''
fi
export PATH='/mingw64/bin:/usr/bin:/c/Users/omarm/bin:/c/Users/omarm/bin:/mingw64/bin:/usr/local/bin:/usr/bin:/usr/bin:/mingw64/bin:/usr/bin:/c/Users/omarm/bin:/c/Program Files/Common Files/Oracle/Java/javapath:/c/Python313/Scripts:/c/Python313:/c/WINDOWS/system32:/c/WINDOWS:/c/WINDOWS/System32/Wbem:/c/WINDOWS/System32/WindowsPowerShell/v1.0:/c/WINDOWS/System32/OpenSSH:/c/Program Files/NVIDIA Corporation/NVIDIA app/NvDLISR:/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/cmd:/c/ProgramData/chocolatey/bin:/c/Program Files (x86)/cloudflared:/c/Program Files/Graphviz/bin:/c/Program Files/GitHub CLI:/c/Program Files/dotnet:/c/Program Files/PowerShell/7:/c/Program Files/Java/jdk-24/bin:/c/Users/omarm/Tools/StructurizrCLI:/c/Users/omarm/Tools/PlantUML:/c/Users/omarm/.local/bin:/c/Users/omarm/AppData/Roaming/npm:/c/Users/omarm/AppData/Roaming/Python/Python313/Scripts:/c/Users/omarm/AppData/Roaming/Python/Python313:/c/Users/omarm/AppData/Roaming/Programs/Zero Install:/c/Users/omarm/AppData/Local/Microsoft/WindowsApps:/c/Users/omarm/AppData/Local/Programs/Microsoft VS Code/bin:/c/Users/omarm/AppData/Local/GitHubDesktop/bin:/c/Program Files/nodejs:/c/Users/omarm/AppData/Roaming/Code/User/globalStorage/github.copilot-chat/debugCommand:/usr/bin/vendor_perl:/usr/bin/core_perl'
