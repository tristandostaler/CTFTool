#https://blog.markvincze.com/download-artifacts-from-a-latest-github-release-in-sh-and-powershell/
$latestRelease = Invoke-WebRequest https://github.com/0xd4d/dnSpy/releases/latest -Headers @{"Accept"="application/json"}
# The releases are returned in the format {"id":3622206,"tag_name":"hello-1.0.0.11",...}, we have to extract the tag_name.
$json = $latestRelease.Content | ConvertFrom-Json
$latestVersion = $json.tag_name
$url = "https://github.com/0xd4d/dnSpy/releases/download/$latestVersion/dnSpy.zip"

@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

Set-ExplorerOptions -EnableShowHiddenFilesFoldersDrives -EnableShowProtectedOSFiles -EnableShowFileExtensions -EnableShowFullPathInTitlebar
DISM /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux
chocolatey feature enable -n=allowGlobalConfirmation
choco install -y git
choco install -y GoogleChrome
choco install -y wireshark
choco install -y python3
choco install -y python
choco install -y vscode
choco install -y vscode-icons
choco install -y sysinternals
refreshenv
code --install-extension robertohuertasm.vscode-icons
code --install-extension ms-vscode.cpptools
code --install-extension ms-python.python
code --install-extension donjayamanne.githistory
code --install-extension PeterJausovec.vscode-docker
choco install -y ida-free
choco install -y dropbox
choco install -y 010editor
Install-ChocolateyPinnedTaskBarItem "${env:UserProfile}\Desktop\code.lnk"
Install-ChocolateyPinnedTaskBarItem "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
chocolatey feature disable -n=allowGlobalConfirmation
choco install -y BoxStarter