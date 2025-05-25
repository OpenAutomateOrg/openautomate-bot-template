# Sync metadata from bot.json to config.ini
param(
    [string]$BotJsonPath = "bot.json",
    [string]$ConfigPath = "config/config.ini"
)

if (-not (Test-Path $BotJsonPath)) {
    Write-Error "bot.json not found at: $BotJsonPath"
    exit 1
}

if (-not (Test-Path $ConfigPath)) {
    Write-Error "config.ini not found at: $ConfigPath"
    exit 1
}

# Read bot.json
$botData = Get-Content $BotJsonPath | ConvertFrom-Json

# Read config.ini
$configContent = Get-Content $ConfigPath

# Update config.ini with bot.json values
$updatedContent = @()
$inBotSection = $false

foreach ($line in $configContent) {
    if ($line -match '^\[bot\]') {
        $inBotSection = $true
        $updatedContent += $line
    }
    elseif ($line -match '^\[.*\]' -and $inBotSection) {
        $inBotSection = $false
        $updatedContent += $line
    }
    elseif ($inBotSection) {
        if ($line -match '^name\s*=') {
            $updatedContent += "name = $($botData.name)"
        }
        elseif ($line -match '^description\s*=') {
            $updatedContent += "description = $($botData.description)"
        }
        elseif ($line -match '^version\s*=') {
            $updatedContent += "version = $($botData.version)"
        }
        else {
            $updatedContent += $line
        }
    }
    else {
        $updatedContent += $line
    }
}

# Write updated config.ini
$updatedContent | Set-Content $ConfigPath

Write-Host "Metadata synced from bot.json to config.ini" -ForegroundColor Green 