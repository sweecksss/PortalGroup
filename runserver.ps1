$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $python)) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    $systemPython = if ($pythonCommand) {
        $pythonCommand.Source
    } else {
        Get-ChildItem -Path (Join-Path $env:LOCALAPPDATA 'Programs\Python') -Filter python.exe -File -Recurse -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending |
            Select-Object -First 1 -ExpandProperty FullName
    }

    if (-not $systemPython) {
        throw 'Python 3.10 or newer is required. Install it from https://www.python.org/downloads/ and run this command again.'
    }

    & $systemPython -m venv .venv
}

& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt
& $python manage.py migrate
& $python manage.py runserver
