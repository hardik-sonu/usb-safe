$ErrorActionPreference = "Stop"
Write-Host "Building USB Safe..."
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --onefile --windowed --name "USB Safe" --icon NONE src/main.py
Write-Host "Build complete! Executable is in dist/USB Safe.exe"
