<#
.SYNOPSIS
    Performs static type checking with mypy
.DESCRIPTION
    Performs static type checking with mypy to detect any potential
    issues in the specified source code files and directories.
#>
using namespace System.Runtime.InteropServices

[CmdletBinding()]
param (
    [Parameter(
        Position=0,
        ValueFromPipeline,
        ValueFromPipelineByPropertyName,
        ValueFromRemainingArguments
    )]
    [Alias("p")]
    [string[]] $Path = $null
)

# Define global variables and validate prerequisites
begin {
    if (-not [RuntimeInformation]::IsOSPlatform([OSPlatform]::Windows)) {
        throw "This script only supports Windows operating Systems"
    }

    if ((Get-Location).Path.Replace("\", "/") -notlike "*/rfc-search/tools*") {
        throw "This script must be executed in directory /rfc-search/tools"
    }

    $MypyArgs = @()
    $ExePath = $(where.exe "mypy.exe" 2> $null)

    if (-not $ExePath) {
        throw "Failed to locate executable file 'mypy.exe'"
    }

    if (-not ($ExePath -is [string])) {
        $ExePath = $ExePath[0]
    }
}

# Process the pipeline input if available
process {
    if ($Path) {
        if ($Path -notlike "***" -and -not (Test-Path $Path)) {
            throw "Invalid file path: '${Path}'"
        }
        $MypyArgs += $Path
    }
}

# Run mypy subprocess to perform static type checking
end {
    # Use default mypy options if no config file exists
    if (-not (Test-Path "mypy.ini")) {
        if (-not $MypyArgs) {
            throw "Path must be specified if no configuration file exists"
        }

        $MypyArgs += @(
            "--no-implicit-optional",
            "--strict",
            "--warn-incomplete-stub",
            "--warn-no-return",
            "--warn-redundant-casts",
            "--warn-return-any",
            "--warn-unreachable",
            "--warn-unused-ignores"
        )
    }
    Start-Process $ExePath -ArgumentList $MypyArgs -NoNewWindow -Wait
}
