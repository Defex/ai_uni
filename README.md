Powershell:
Look up enviroment keys - Get-ChildItem Env:
set enviroment key  - $env:LOL_API_KEY = "XXXX-XX-XXX-XXX"
set globaly - run as admin [Environment]::SetEnvironmentVariable("LOL_API_KEY", "XXXXX", "Machine")