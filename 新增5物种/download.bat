@echo off

for /f "delims=" %%i in (poultry.txt) do (
    
    datasets download virus genome accession "%%i" --include genome,cds,protein --filename "%%i.zip"
    move /y "%%i.zip" "poultry\" >nul
)