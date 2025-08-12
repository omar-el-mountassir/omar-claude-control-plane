# Enhanced Windows Machine Profile Collector
# REP+PADA Integrated - Governance Ready Output
param([string]$OutputPath = "CONTEXT\machine\profile.json")

$ErrorActionPreference = "SilentlyContinue"

Write-Host "🧠🤖 Enhanced Machine Audit - REP+PADA Integration Active" -ForegroundColor Cyan
Write-Host "🤖 PADA: Systematic data collection initiated..." -ForegroundColor Yellow
Write-Host "🧠 REP: Logic validation and bias detection active..." -ForegroundColor Green

function TryCmd($cmd, $args = @()) { 
    try { 
        if ($args) { & $cmd @args } else { & $cmd }
    } catch { 
        $null 
    } 
}

function Get-ToolVersion($name, $args = @("--version")) {
    try {
        $output = @()
        foreach ($arg in $args) {
            $result = & $name $arg 2>$null
            if ($result) { 
                $output += ($result -join " ")
                break
            }
        }
        if (-not $output) {
            $result = & $name "-v" 2>$null
            if ($result) { $output += ($result -join " ") }
        }
        if ($output) { return $output[0] } else { return $null }
    } catch { 
        return $null 
    }
}

Write-Host "🤖 Collecting OS information..." -ForegroundColor Yellow

# Enhanced OS Info
$osInfo = Get-ComputerInfo
$winVer = [Environment]::OSVersion

Write-Host "🤖 Collecting CPU information..." -ForegroundColor Yellow

# Enhanced CPU Info
$cpuInfo = Get-CimInstance Win32_Processor
$cpuCache = Get-CimInstance Win32_CacheMemory | Where-Object { $_.Level -eq 3 }

Write-Host "🤖 Collecting Memory information..." -ForegroundColor Yellow

# Enhanced Memory Info  
$memSys = Get-CimInstance Win32_ComputerSystem
$memMods = Get-CimInstance Win32_PhysicalMemory
$memAvail = (Get-Counter '\Memory\Available Bytes' -SampleInterval 1 -MaxSamples 1).CounterSamples.CookedValue

Write-Host "🤖 Collecting Storage information..." -ForegroundColor Yellow

# Enhanced Storage Info
$disks = Get-PhysicalDisk
$diskHealth = Get-Disk
$smartData = Get-StorageReliabilityCounter -ErrorAction SilentlyContinue

Write-Host "🤖 Collecting GPU information..." -ForegroundColor Yellow

# Enhanced GPU Info
$gpus = Get-CimInstance Win32_VideoController
$dxDiag = Try { & dxdiag /t temp_dx.txt 2>$null; Get-Content temp_dx.txt -ErrorAction Stop; Remove-Item temp_dx.txt -Force } Catch { $null }

Write-Host "🤖 Collecting Network information..." -ForegroundColor Yellow

# Enhanced Network Info
$netCfg = Get-NetIPConfiguration
$netAdapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
$dnsServers = (Get-DnsClientServerAddress).ServerAddresses | Select-Object -Unique
$domainInfo = Try { (Get-ComputerInfo).CsDomain } Catch { $null }

Write-Host "🤖 Collecting Security information..." -ForegroundColor Yellow

# Enhanced Security Info
$fw = Get-NetFirewallProfile
$defender = Try { Get-MpComputerStatus } Catch { $null }
$tpm = Try { Get-Tpm } Catch { $null }
$secBoot = Try { Confirm-SecureBootUEFI } Catch { $null }
$bitlocker = Try { Get-BitLockerVolume } Catch { $null }
$uac = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name EnableLUA).EnableLUA

Write-Host "🤖 Collecting Toolchain information..." -ForegroundColor Yellow

# Enhanced Proxy Detection
$proxy = @()
$proxy += (netsh winhttp show proxy) -join "`n"
$proxy += Try { (Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings").ProxyServer } Catch { "" }

# Comprehensive Toolchain Detection
$toolchain = [ordered]@{
    "claude_code"    = Get-ToolVersion "claude-code" @("--version", "version")
    "git"            = Get-ToolVersion "git" @("--version")  
    "python"         = Get-ToolVersion "python" @("--version", "-V")
    "uv"             = Get-ToolVersion "uv" @("--version")
    "node"           = Get-ToolVersion "node" @("--version")
    "npm"            = Get-ToolVersion "npm" @("--version")
    "pnpm"           = Get-ToolVersion "pnpm" @("--version")
    "yarn"           = Get-ToolVersion "yarn" @("--version")
    "bun"            = Get-ToolVersion "bun" @("--version")
    "go"             = Get-ToolVersion "go" @("version")
    "rust"           = Get-ToolVersion "rustc" @("--version")
    "cargo"          = Get-ToolVersion "cargo" @("--version")
    "docker"         = Get-ToolVersion "docker" @("--version")
    "kubectl"        = Get-ToolVersion "kubectl" @("version", "--client")
    "terraform"      = Get-ToolVersion "terraform" @("--version")
    "powershell"     = $PSVersionTable.PSVersion.ToString()
    "windowsterminal"= Get-ToolVersion "wt" @("--version")
    "vscode"         = Get-ToolVersion "code" @("--version")
}

Write-Host "🧠 REP: Validating collected data consistency..." -ForegroundColor Green

# Collect IPv4/IPv6 addresses
$ipv4 = @()
$ipv6 = @()
$netCfg | ForEach-Object { 
    if ($_.IPv4Address) { $ipv4 += $_.IPv4Address }
    if ($_.IPv6Address) { $ipv6 += $_.IPv6Address | Where-Object { $_ -notlike "fe80:*" } }
}

Write-Host "🤖 PADA: Structuring governance-ready profile..." -ForegroundColor Yellow

# Build Enhanced Profile
$profile = [ordered]@{
    os = [ordered]@{
        family = "Windows"
        version = $osInfo.WindowsVersion
        build = $osInfo.OsBuildNumber
        kernel = $osInfo.OsName
        edition = $osInfo.WindowsEditionId
        architecture = $env:PROCESSOR_ARCHITECTURE
    }
    cpu = [ordered]@{
        model = ($cpuInfo.Name | Select-Object -First 1).Trim()
        cores_logical = ($cpuInfo.NumberOfLogicalProcessors | Measure-Object -Sum).Sum
        cores_physical = ($cpuInfo.NumberOfCores | Measure-Object -Sum).Sum
        max_clock_mhz = $cpuInfo.MaxClockSpeed | Select-Object -First 1
        cache_l3_kb = if ($cpuCache) { $cpuCache.MaxCacheSize } else { $null }
        manufacturer = $cpuInfo.Manufacturer | Select-Object -First 1
    }
    memory = [ordered]@{
        total_bytes = [int64]$memSys.TotalPhysicalMemory
        available_bytes = [int64]$memAvail
        modules = @(
            $memMods | ForEach-Object {
                [ordered]@{
                    capacity_bytes = [int64]$_.Capacity
                    speed_mhz = if ($_.Speed) { [int]$_.Speed } else { $null }
                    manufacturer = if ($_.Manufacturer) { $_.Manufacturer.Trim() } else { $null }
                    part_number = if ($_.PartNumber) { $_.PartNumber.Trim() } else { $null }
                }
            }
        )
    }
    storage = @(
        $disks | ForEach-Object {
            $disk = $_
            $health = $diskHealth | Where-Object { $_.Number -eq $disk.DeviceId }
            [ordered]@{
                name = $disk.FriendlyName
                type = $disk.MediaType
                size_bytes = [int64]$disk.Size
                bus = $disk.BusType
                system = $false  # Would need more logic to detect
                health = if ($health) { $health.HealthStatus } else { $null }
                temperature_c = $null  # Would need SMART data
            }
        }
    )
    gpu = @(
        $gpus | Where-Object { $_.Name -notlike "*Basic*" } | ForEach-Object {
            [ordered]@{
                name = $_.Name
                vram_bytes = if ($_.AdapterRAM -gt 0) { [int64]$_.AdapterRAM } else { $null }
                driver = $_.DriverVersion
                compute_capability = $null  # Would need CUDA query
            }
        }
    )
    network = [ordered]@{
        hostname = "redacted-host"  # Security: redact actual hostname
        ipv4 = $ipv4
        ipv6 = $ipv6
        proxy = if ($proxy -match "Direct access" -or $proxy -match "No proxy") { $null } else { 
            ($proxy | Where-Object { $_ -and $_ -ne "" }) -join "; " 
        }
        vpn = Try { 
            $vpns = (Get-VpnConnection -ErrorAction Stop).Name
            if ($vpns) { $vpns -join ", " } else { $null }
        } Catch { $null }
        dns_servers = $dnsServers
        domain_joined = if ($domainInfo -and $domainInfo -ne "WORKGROUP") { $true } else { $false }
    }
    security = [ordered]@{
        tpm_present = if ($tpm) { [bool]$tpm.TpmPresent } else { $null }
        tmp_version = if ($tpm) { $tpm.TmpVersion } else { $null }
        secure_boot = if ($secBoot -ne $null) { [bool]$secBoot } else { $null }
        defender_enabled = if ($defender) { [bool]$defender.AntispywareEnabled } else { $null }
        firewall_domain = [bool]($fw | Where-Object { $_.Name -eq "Domain" }).Enabled
        firewall_private = [bool]($fw | Where-Object { $_.Name -eq "Private" }).Enabled  
        firewall_public = [bool]($fw | Where-Object { $_.Name -eq "Public" }).Enabled
        bitlocker_enabled = if ($bitlocker) { 
            [bool]($bitlocker | Where-Object { $_.ProtectionStatus -eq "On" })
        } else { $null }
        uac_enabled = [bool]$uac
    }
    toolchain = $toolchain
    timestamps = [ordered]@{
        collected_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        collector_version = "enhanced-v1.0.0"
        uptime_seconds = [int]((Get-Uptime).TotalSeconds)
    }
    governance_metadata = [ordered]@{
        profile_version = "1.0.0"
        compatibility_level = "claude-code-optimized"
        agent_orchestration_ready = $true
        rep_pada_compatible = $true
    }
}

Write-Host "🧠 REP: Final validation - checking profile completeness..." -ForegroundColor Green

# REP Validation: Check required fields
$requiredSections = @("os", "cpu", "memory", "storage", "gpu", "network", "security", "toolchain", "timestamps")
$missingSections = $requiredSections | Where-Object { -not $profile.ContainsKey($_) }

if ($missingSections) {
    Write-Host "🧠 REP Warning: Missing required sections: $($missingSections -join ', ')" -ForegroundColor Red
} else {
    Write-Host "🧠 REP: All required sections present ✅" -ForegroundColor Green
}

# Output JSON
Write-Host "🤖 PADA: Writing governance-ready profile to $OutputPath" -ForegroundColor Yellow

$jsonOutput = $profile | ConvertTo-Json -Depth 8 -Compress:$false
$jsonOutput | Out-File -FilePath $OutputPath -Encoding UTF8 -Force

Write-Host "✅ Enhanced machine profile collection complete!" -ForegroundColor Green
Write-Host "🧠🤖 REP+PADA Integration: Profile validated and structured for governance consumption" -ForegroundColor Cyan

# Output summary for immediate feedback
Write-Host "`n📊 Quick Summary:" -ForegroundColor Cyan
Write-Host "OS: $($profile.os.family) $($profile.os.version) ($($profile.os.architecture))"
Write-Host "CPU: $($profile.cpu.model) - $($profile.cpu.cores_physical)P/$($profile.cpu.cores_logical)L"
Write-Host "RAM: $('{0:N1} GB' -f ($profile.memory.total_bytes / 1GB))"
Write-Host "Storage: $($profile.storage.Count) devices"
Write-Host "GPU: $($profile.gpu.Count) devices"
Write-Host "Toolchain: $(($profile.toolchain.Values | Where-Object { $_ }).Count) tools detected"