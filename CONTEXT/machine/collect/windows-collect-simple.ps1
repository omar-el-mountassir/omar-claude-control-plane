# Simplified Windows Machine Profile Collector
# REP+PADA Integrated - Governance Ready Output
param([string]$OutputPath = "CONTEXT\machine\profile.json")

$ErrorActionPreference = "SilentlyContinue"

Write-Host "🧠🤖 Enhanced Machine Audit - REP+PADA Integration Active" -ForegroundColor Cyan

# Collect basic system info
$osInfo = Get-ComputerInfo
$cpuInfo = Get-CimInstance Win32_Processor | Select-Object -First 1
$memInfo = Get-CimInstance Win32_ComputerSystem
$disks = Get-PhysicalDisk
$gpus = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -notlike "*Basic*" }
$netConfig = Get-NetIPConfiguration -Detailed | Where-Object { $_.NetProfile.Name -ne "Unidentified network" } | Select-Object -First 1

# Basic toolchain detection
$tools = @{}
$toolList = @("git", "python", "uv", "node", "npm", "claude-code", "docker", "go")

foreach ($tool in $toolList) {
    try {
        $version = & $tool --version 2>$null | Select-Object -First 1
        if (-not $version) { $version = & $tool -v 2>$null | Select-Object -First 1 }
        $tools[$tool] = if ($version) { $version.ToString().Trim() } else { $null }
    } catch {
        $tools[$tool] = $null
    }
}

# Add PowerShell version
$tools["powershell"] = $PSVersionTable.PSVersion.ToString()

# Build profile
$profile = @{
    os = @{
        family = "Windows"
        version = $osInfo.WindowsVersion
        build = $osInfo.OSBuildNumber
        kernel = $osInfo.OSName
        architecture = $env:PROCESSOR_ARCHITECTURE
        edition = $osInfo.WindowsEditionId
    }
    cpu = @{
        model = $cpuInfo.Name.Trim()
        cores_logical = $cpuInfo.NumberOfLogicalProcessors
        cores_physical = $cpuInfo.NumberOfCores
        max_clock_mhz = $cpuInfo.MaxClockSpeed
        manufacturer = $cpuInfo.Manufacturer
    }
    memory = @{
        total_bytes = [int64]$memInfo.TotalPhysicalMemory
        modules = @()
    }
    storage = @(
        $disks | ForEach-Object {
            @{
                name = $_.FriendlyName
                type = $_.MediaType
                size_bytes = [int64]$_.Size
                bus = $_.BusType
                system = $false
            }
        }
    )
    gpu = @(
        $gpus | ForEach-Object {
            @{
                name = $_.Name
                vram_bytes = if ($_.AdapterRAM -gt 0) { [int64]$_.AdapterRAM } else { $null }
                driver = $_.DriverVersion
            }
        }
    )
    network = @{
        hostname = "redacted-host"
        ipv4 = @($netConfig.IPv4Address.IPAddress)
        ipv6 = @()
        proxy = $null
        vpn = $null
        dns_servers = @()
        domain_joined = $false
    }
    security = @{
        tmp_present = $null
        tpm_version = $null
        secure_boot = $null
        defender_enabled = $null
        firewall_domain = $null
        firewall_private = $null
        firewall_public = $null
        bitlocker_enabled = $null
        uac_enabled = $null
    }
    toolchain = $tools
    timestamps = @{
        collected_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        collector_version = "simple-v1.0.0"
        uptime_seconds = [int]((Get-Uptime).TotalSeconds)
    }
    governance_metadata = @{
        profile_version = "1.0.0"
        compatibility_level = "claude-code-optimized"
        agent_orchestration_ready = $true
        rep_pada_compatible = $true
    }
}

# Convert to JSON and save
$jsonOutput = $profile | ConvertTo-Json -Depth 6
$jsonOutput | Out-File -FilePath $OutputPath -Encoding UTF8 -Force

Write-Host "✅ Basic machine profile collected successfully!" -ForegroundColor Green
Write-Host "📊 Quick Summary:" -ForegroundColor Cyan
Write-Host "OS: $($profile.os.family) $($profile.os.version)"
Write-Host "CPU: $($profile.cpu.model) - $($profile.cpu.cores_physical)P/$($profile.cpu.cores_logical)L"
Write-Host "RAM: $('{0:N1} GB' -f ($profile.memory.total_bytes / 1GB))"
Write-Host "Storage: $($profile.storage.Count) devices"
Write-Host "GPU: $($profile.gpu.Count) devices"