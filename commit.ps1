# ============================================================
# commit.ps1 — Sync from network drive and commit to GitHub
#
# Usage:
#   .\commit.ps1 -Message "Your commit message"
#
# Optional:
#   .\commit.ps1 -Message "Your commit message" -Branch "dev_cssEdits"
#
# Why this script exists:
#   The O: drive is a mapped network share that blocks Git's
#   fsync calls and prevents .git file creation. All commits
#   must be made from the local clone at C:\temp\Static-Documentation.
#   This script syncs your working files from O: to C:\ and
#   then commits and pushes for you.
# ============================================================

param (
    [Parameter(Mandatory = $true)]
    [string]$Message,

    [Parameter(Mandatory = $false)]
    [string]$Branch = "dev_cssEdits"
)

$src = "O:\Static-Documentation"
$dst = "C:\temp\Static-Documentation"

# ── Step 1: Check local clone exists ─────────────────────────
if (!(Test-Path "$dst\.git")) {
    Write-Host ""
    Write-Error "Local clone not found at $dst. Run the following first:"
    Write-Host "  git clone https://github.com/revtestaccount/Static-Documentation.git $dst"
    Write-Host "  cd $dst"
    Write-Host "  git checkout $Branch"
    exit 1
}

# ── Step 2: Sync O: → C:\temp using robocopy ─────────────────
Write-Host ""
Write-Host "Syncing files from $src to $dst ..." -ForegroundColor Cyan

robocopy $src $dst /MIR /XD ".git" "node_modules" /NFL /NDL /NJH /NJS /NC /NS

if ($LASTEXITCODE -ge 8) {
    Write-Error "Robocopy failed with exit code $LASTEXITCODE. Aborting."
    exit 1
}

Write-Host "Sync complete." -ForegroundColor Green

# ── Step 3: Stage all changes ────────────────────────────────
Write-Host ""
Write-Host "Staging changes..." -ForegroundColor Cyan
Set-Location $dst
git add .

# ── Step 4: Show what's staged ───────────────────────────────
Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Cyan
git status --short

# ── Step 5: Confirm before committing ────────────────────────
Write-Host ""
$confirm = Read-Host "Proceed with commit? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Aborted." -ForegroundColor Yellow
    exit 0
}

# ── Step 6: Commit ───────────────────────────────────────────
Write-Host ""
Write-Host "Committing..." -ForegroundColor Cyan
git commit -m $Message

if ($LASTEXITCODE -ne 0) {
    Write-Error "Commit failed."
    exit 1
}

# ── Step 7: Push ─────────────────────────────────────────────
Write-Host ""
Write-Host "Pushing to origin/$Branch..." -ForegroundColor Cyan
git push origin $Branch

if ($LASTEXITCODE -ne 0) {
    Write-Error "Push failed."
    exit 1
}

Write-Host ""
Write-Host "Done! Changes pushed to origin/$Branch." -ForegroundColor Green
