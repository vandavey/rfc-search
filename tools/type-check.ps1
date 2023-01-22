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
        Mandatory,
        Position=0,
        ValueFromPipeline,
        ValueFromPipelineByPropertyName,
        ValueFromRemainingArguments
    )]
    [Alias("p")]
    [string[]] $Path
)

# Declare globals and validate prerequisites
begin {
    if (-not [RuntimeInformation]::IsOSPlatform([OSPlatform]::Windows)) {
        throw "This script only supports Windows operating Systems"
    }

    $PathList = @()
    $ExePath = $(where.exe "mypy.exe" 2> $null)

    if (-not $ExePath) {
        throw "Failed to locate executable file 'mypy.exe'"
    }

    if (-not ($ExePath -is [string])) {
        $ExePath = $ExePath[0]
    }
}

# Process all the pipeline input
process {
    if ($Path) {
        if (-not (Test-Path $Path)) {
            throw "Invalid file path: '${Path}'"
        }
        $PathList += $Path    
    }
}

# Run mypy subprocess to perform static type checking
end {
    $MypyArgs = @{
        ArgumentList = $PathList + @(
            "--strict"
            "--warn-incomplete-stub",
            "--warn-redundant-casts",
            "--warn-return-any",
            "--warn-unreachable",
            "--warn-unused-ignores"
        )
        FilePath = $ExePath
        NoNewWindow = $true
        Wait = $true
    }

    # Perform static type checking with mypy
    Start-Process @MypyArgs
}
