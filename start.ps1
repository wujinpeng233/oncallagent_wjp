Set-Location -LiteralPath $PSScriptRoot
& 'C:\Users\30521\.conda\envs\fastapi\python.exe' -m uvicorn main:app --reload
