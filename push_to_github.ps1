[CmdletBinding()]
param(
    [string]$RepoPath = ".",
    [string]$Branch = "main",
    [string]$RemoteName = "origin",
    [string]$RemoteUrl = "https://github.com/Poniek-Labs/OpenDOC-system.git",
    [string]$CommitMessage = "",
    [string]$VersionFile = "VERSION",
    [ValidateSet("major", "minor", "none")]
    [string]$ReleaseType = "",
    [string]$GitUserName = "codebunny100",
    [string]$GitUserEmail = "es.wendland@gmail.com",
    [switch]$InitRepo,
    [switch]$NoTag
)

$ErrorActionPreference = "Stop"

function Run-Git {
    param([string[]]$Command)
    $output = & git @Command 2>&1
    if ($LASTEXITCODE -ne 0) {
        $msg = ($output | Out-String).Trim()
        throw "git $($Command -join ' ') failed`n$msg"
    }
    return $output
}

function Get-ReleaseTypeChoice {
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
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        return "1.0"
    }
    $raw = (Get-Content -LiteralPath $Path -Raw).Trim()
    if ($raw -notmatch '^\d+\.\d+$') {
        throw "Invalid VERSION format in '$Path'. Expected major.minor (e.g. 1.0)."
    }
    return $raw
}

function Get-NextVersion {
    param([string]$CurrentVersion, [string]$Type)
    $parts = $CurrentVersion.Split(".")
    $major = [int]$parts[0]
    $minor = [int]$parts[1]
    switch ($Type) {
        "major" { return "$($major + 1).0" }
        "minor" { return "$major.$($minor + 1)" }
        "none"  { return $CurrentVersion }
        default { throw "Unknown release type: $Type" }
    }
}

$resolvedRepoPath = (Resolve-Path -LiteralPath $RepoPath).Path
Set-Location -LiteralPath $resolvedRepoPath

$isRepo = $false
& git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -eq 0) { $isRepo = $true }

if (-not $isRepo) {
    if (-not $InitRepo) {
        throw "No git repo at '$resolvedRepoPath'. Re-run with -InitRepo."
    }
    Run-Git @("init") | Out-Null
}

# Clean stale merge state if present.
if (Test-Path -LiteralPath ".git/MERGE_HEAD") {
    Run-Git @("merge", "--abort") | Out-Null
}

# Identity (best effort)
if ($GitUserName -ne "") { Run-Git @("config", "user.name", $GitUserName) | Out-Null }
if ($GitUserEmail -ne "") { Run-Git @("config", "user.email", $GitUserEmail) | Out-Null }

# Branch checkout/create
$branchExists = ((& git branch --list $Branch | Out-String).Trim() -ne "")
if ($branchExists) {
    Run-Git @("checkout", $Branch) | Out-Null
} else {
    Run-Git @("checkout", "-b", $Branch) | Out-Null
}

# Ensure remote points where you want
$remoteExists = $false
& git remote get-url $RemoteName *> $null
if ($LASTEXITCODE -eq 0) { $remoteExists = $true }
if ($remoteExists) {
    Run-Git @("remote", "set-url", $RemoteName, $RemoteUrl) | Out-Null
} else {
    Run-Git @("remote", "add", $RemoteName, $RemoteUrl) | Out-Null
}

# Version bump
$effectiveType = Get-ReleaseTypeChoice -RequestedType $ReleaseType
$currentVersion = Get-CurrentVersion -Path $VersionFile
$nextVersion = Get-NextVersion -CurrentVersion $currentVersion -Type $effectiveType
if ($nextVersion -ne $currentVersion) {
    Set-Content -LiteralPath $VersionFile -Value $nextVersion -NoNewline
    Write-Host "Version bumped: $currentVersion -> $nextVersion"
} else {
    Write-Host "Version unchanged: $currentVersion"
}

# Commit
Run-Git @("add", "-A") | Out-Null
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $msg = $CommitMessage
    if ([string]::IsNullOrWhiteSpace($msg)) {
        $msg = "release: v$nextVersion ($effectiveType)"
    }
    Run-Git @("commit", "-m", $msg) | Out-Null
} else {
    Write-Host "No changes to commit."
}

# Tag (best effort)
if (-not $NoTag -and $effectiveType -ne "none") {
    & git tag -d "v$nextVersion" *> $null
    Run-Git @("tag", "-a", "v$nextVersion", "-m", "OpenDOC release v$nextVersion") | Out-Null
}

# Push local truth to remote main (no merge step)
Run-Git @("push", "-u", $RemoteName, "$Branch`:$Branch", "--force-with-lease") | Out-Null
if (-not $NoTag -and $effectiveType -ne "none") {
    Run-Git @("push", $RemoteName, "--tags", "--force-with-lease") | Out-Null
}

Write-Host "Done: pushed to $RemoteUrl on branch $Branch"

