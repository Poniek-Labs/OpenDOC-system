[CmdletBinding()]
param(
    [string]$RepoPath = ".",
    [string]$Branch = "main",
    [string]$CommitMessage = "",
    [string]$RemoteName = "origin",
    [string]$RemoteUrl = "https://github.com/Poniek-Labs/OpenDOC-system.git",
    [string]$GitUserName = "codebunny100",
    [string]$GitUserEmail = "es.wendland@gmail.com",
    [ValidateSet("major", "minor", "none")]
    [string]$ReleaseType = "",
    [string]$VersionFile = "VERSION",
    [switch]$CreateTag = $true,
    [switch]$InitRepo
)

$ErrorActionPreference = "Stop"

<#
.SYNOPSIS
Stages, commits, and pushes OpenDOC files to GitHub.

.DESCRIPTION
Can initialize a git repository, set/update remote, commit changes, and push.
Also supports interactive major/minor release version bumping.

.EXAMPLE
.\push_to_github.ps1 -InitRepo

.EXAMPLE
.\push_to_github.ps1 -ReleaseType minor
#>

function Run-Git {
    param([string[]]$Command)
    if (-not $Command -or $Command.Count -eq 0) {
        throw "Run-Git received an empty command list."
    }
    $output = & git @Command 2>&1
    if ($LASTEXITCODE -ne 0) {
        $joined = ($output | Out-String).Trim()
        if ([string]::IsNullOrWhiteSpace($joined)) {
            throw "Git command failed: git $($Command -join ' ')"
        }
        throw "Git command failed: git $($Command -join ' ')`n$joined"
    }
    return $output
}

function Get-ReleaseType {
    param([string]$RequestedType)
    if ($RequestedType -ne "") {
        return $RequestedType
    }

    Write-Host ""
    Write-Host "Select release type:"
    Write-Host "  1) Major release"
    Write-Host "  2) Minor release"
    $choice = Read-Host "Enter choice (1/2)"

    switch ($choice) {
        "1" { return "major" }
        "2" { return "minor" }
        default { throw "Invalid choice. Use 1 or 2." }
    }
}

function Get-CurrentVersion {
    param([string]$FilePath)
    if (-not (Test-Path -LiteralPath $FilePath)) {
        return "1.0"
    }
    $raw = (Get-Content -LiteralPath $FilePath -Raw).Trim()
    if ($raw -match '^\d+\.\d+$') {
        return $raw
    }
    throw "Invalid version format in '$FilePath'. Expected 'major.minor' (e.g. 1.0)."
}

function Bump-Version {
    param(
        [string]$CurrentVersion,
        [string]$Type
    )
    $parts = $CurrentVersion.Split(".")
    $major = [int]$parts[0]
    $minor = [int]$parts[1]

    switch ($Type) {
        "major" { return "$($major + 1).0" }
        "minor" { return "$major.$($minor + 1)" }
        "none"  { return $CurrentVersion }
        default { throw "Unknown release type '$Type'" }
    }
}

$resolvedRepoPath = (Resolve-Path -LiteralPath $RepoPath).Path
Set-Location -LiteralPath $resolvedRepoPath

$isRepo = $false
try {
    & git rev-parse --is-inside-work-tree *> $null
    $isRepo = ($LASTEXITCODE -eq 0)
} catch {
    $isRepo = $false
}

if (-not $isRepo) {
    if (-not $InitRepo) {
        throw "No git repository found at '$resolvedRepoPath'. Re-run with -InitRepo."
    }
    Run-Git -Command @("init")
}

# Optional identity setup for new environments
if (-not [string]::IsNullOrWhiteSpace($GitUserName)) {
    Run-Git -Command @("config", "user.name", $GitUserName) | Out-Null
}
if (-not [string]::IsNullOrWhiteSpace($GitUserEmail)) {
    Run-Git -Command @("config", "user.email", $GitUserEmail) | Out-Null
}

$effectiveUserName = ((& git config user.name) 2>$null | Out-String).Trim()
$effectiveUserEmail = ((& git config user.email) 2>$null | Out-String).Trim()
if ([string]::IsNullOrWhiteSpace($effectiveUserName) -or [string]::IsNullOrWhiteSpace($effectiveUserEmail)) {
    Write-Host "Warning: git user identity is not set. Commit may fail until configured."
}

# Ensure branch exists and is checked out
try {
    Run-Git -Command @("checkout", "-B", $Branch)
} catch {
    # Fallback for older git
    Run-Git -Command @("checkout", "-b", $Branch)
}

if ($RemoteUrl -ne "") {
    $remoteExists = $false
    try {
        & git remote get-url $RemoteName *> $null
        $remoteExists = ($LASTEXITCODE -eq 0)
    } catch {
        $remoteExists = $false
    }

    if ($remoteExists) {
        Run-Git -Command @("remote", "set-url", $RemoteName, $RemoteUrl)
    } else {
        Run-Git -Command @("remote", "add", $RemoteName, $RemoteUrl)
    }
}

# Release bump
$effectiveReleaseType = Get-ReleaseType -RequestedType $ReleaseType
$currentVersion = Get-CurrentVersion -FilePath $VersionFile
$newVersion = Bump-Version -CurrentVersion $currentVersion -Type $effectiveReleaseType

if ($newVersion -ne $currentVersion) {
    Set-Content -LiteralPath $VersionFile -Value $newVersion -NoNewline
    Write-Host "Version bumped: $currentVersion -> $newVersion"
} else {
    Write-Host "Version unchanged: $currentVersion"
}

# Stage everything in the selected repo path
Run-Git -Command @("add", "-A")

# Commit if there are staged changes
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $finalMessage = $CommitMessage
    if ([string]::IsNullOrWhiteSpace($finalMessage)) {
        if ($effectiveReleaseType -eq "none") {
            $finalMessage = "chore: update OpenDOC"
        } else {
            $finalMessage = "release: v$newVersion ($effectiveReleaseType)"
        }
    }
    Run-Git -Command @("commit", "-m", $finalMessage)

    if ($CreateTag -and $effectiveReleaseType -ne "none") {
        Run-Git -Command @("tag", "-a", "v$newVersion", "-m", "OpenDOC release v$newVersion")
    }
} else {
    Write-Host "No staged changes to commit."
}

# Push
Run-Git -Command @("push", "-u", $RemoteName, $Branch)
if ($CreateTag -and $effectiveReleaseType -ne "none") {
    Run-Git -Command @("push", $RemoteName, "--tags")
}

Write-Host "Push complete."
