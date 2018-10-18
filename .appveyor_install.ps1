
$Env:PYTHON = "C:\Stackless27_x$Env:BUILDARCH"
$Env:PYTHONPATH = "$Env:PYTHON;$Env:PYTHON\Scripts;$Env:PYTHON\DLLs;$Env:PYTHON\Lib;$Env:PYTHON\Lib\site-packages;"

$SysWOWDLL = "$Env:SYSTEMROOT\SysWOW64\python27.dll"
$SystemDLL = "$Env:SYSTEMROOT\System\python27.dll"

$Env:PATH = $Env:PATH -replace "Python27", "Stackless27_x$Env:BUILDARCH"

If (Test-Path $SystemDLL) {
    Remove-Item $SystemDLL
}
If (Test-Path $SysWOWDLL) {
    Remove-Item $SysWOWDLL
}

$ModuleOutputFolder = $Env:APPVEYOR_BUILD_FOLDER + "\_build\output\ModuleOutput_x$Env:BUILDARCH"

if (-Not(Test-Path $ModuleOutputFolder)) {
    New-Item $ModuleOutputFolder -type directory | Out-Null
}

if (-Not (Test-Path $Env:PYTHON)) {
    # if appveyor image is changed to VS2017 you will need to uncomment these lines
    # $VCInstaller = $InstallersFolder + "VCForPython27.msi"
    # $VCURL = "https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi"

    Import-Module -Name ".\.appveyor_runapp.psm1"

    $SitePackages = "$Env:PYTHON\Lib\site-packages"
    $Python = "$Env:PYTHON\python.exe"
    $Pip = "$Env:PYTHON\Scripts\pip.exe"
    $EasyInstall = "$Env:PYTHON\Scripts\easy_install.exe"

    $InstallersFolder = $Env:APPVEYOR_BUILD_FOLDER + "\_build\installers\"
    if (-Not(Test-Path $InstallersFolder)) {
        New-Item $InstallersFolder -type directory | Out-Null
    }

    if ($Env:BUILDARCH -eq "64") {
        $StacklessInstaller = "python-2.7.15150.amd64-stackless.msi"
        $Py2ExeInstaller = "py2exe-0.6.9.win64-py2.7.amd64.exe"
        $WxInstaller = "wxPython3.0-win64-3.0.2.0-py27.exe"
    } else {
        $StacklessInstaller = "python-2.7.15150-stackless.msi"
        $Py2ExeInstaller = "py2exe-0.6.9.win32-py2.7.exe"
        $WxInstaller = "wxPython3.0-win32-3.0.2.0-py27.exe"
    }

    $StacklessURL = "http://www.stackless.com/binaries/$StacklessInstaller"
    $StacklessInstaller =  $InstallersFolder + $StacklessInstaller

    $Py2ExeURL = "https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/$Py2ExeInstaller/download"
    $Py2ExeInstaller = $InstallersFolder + $Py2ExeInstaller


    $WxURL = "https://sourceforge.net/projects/wxpython/files/wxPython/3.0.2.0/$WxInstaller/download"
    $WxInstaller = $InstallersFolder + $WxInstaller

    $junk = Start-Job -ScriptBlock { Start-FileDownload $Args[0] -Timeout 60000 -FileName $Args[1] } -Name "Stackless" -ArgumentList $StacklessURL, $StacklessInstaller
    $junk = Start-Job -ScriptBlock { Start-FileDownload $Args[0] -Timeout 60000 -FileName $Args[1] } -Name "wxPython" -ArgumentList $WxURL, $WxInstaller
    $junk = Start-Job -ScriptBlock { Start-FileDownload $Args[0] -Timeout 60000 -FileName $Args[1] } -Name "py2exe" -ArgumentList $Py2ExeURL, $Py2ExeInstaller


    Write-Host "=============== Installing Requirements =============="

    Write-Host "  ---- Installing Stackless 2.7.15150"
    $junk = Wait-Job -Name "Stackless"
    Start-Process "MsiExec.exe" -ArgumentList "/I $StacklessInstaller /quiet /passive /qn /norestart TARGETDIR=$Env:PYTHON" -WindowStyle Hidden -Wait
    Write-Host "       Done."

    # Write-Host "  ---- Installing Visual C Compiler for Python 2.7"
    # Invoke-App "$VCInstaller"

    Write-Host "  ---- Upgrading pip 9.0.1"
    Invoke-App $Python "-m pip install --no-cache-dir -U pip==9.0.1" "$ModuleOutputFolder\pip 9.0.1.err.log" "$ModuleOutputFolder\pip 9.0.1.out.log"

    Write-Host "  ---- Upgrading setuptools 40.2.0"
    Invoke-App $Python "-m pip install --no-cache-dir -U setuptools==40.2.0" "$ModuleOutputFolder\setuptools 40.2.0.err.log" "$ModuleOutputFolder\setuptools 40.2.0.out.log"

    Write-Host "  ---- Installing py2exe 0.6.9"
    $junk = Wait-Job -Name "py2exe"
    Invoke-App $EasyInstall "--always-unzip $Py2ExeInstaller"

    Write-Host "  ---- Installing wxPython 3.0.2.0"
    $junk = Wait-Job -Name "wxPython"
    Start-Process $WxInstaller -ArgumentList "/VerySilent /NoRestart /NoCancel /SupressMessageBoxes /Silent /dir=$SitePackages" -WindowStyle Hidden -Wait
    Write-Host "       Done."

    Invoke-App $Pip "pycrypto 2.6.1" "pycrypto==2.6.1" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "wheel 0.29.0" "wheel==0.29.0" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "commonmark 0.7.5" "commonmark==0.7.5" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "jinja2 2.8.1" "jinja2==2.8.1" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "sphinx 1.5.6" "sphinx==1.5.6" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "pillow 3.4.2" "pillow==3.4.2" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "comtypes 1.1.7" "comtypes==1.1.7" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "paramiko 2.2.1" "paramiko==2.2.1" -LogDir $ModuleOutputFolder
    Invoke-App $Pip "pywin32 223" "pywin32==223" -LogDir $ModuleOutputFolder
    # *See Changes* PipInstall "pycrypto 2.6.1" "pycrypto==2.6.1"
    # *See Changes* PipInstall "ctypeslib 0.5.6" "svn+http://svn.python.org/projects/ctypes/trunk/ctypeslib/#ctypeslib=0.5.6"

} else {
    # we are already using a cached version so
    # there is no need to cache it agian.
    $env:APPVEYOR_CACHE_SKIP_SAVE = "true"
    Out-File "$ModuleOutputFolder\cached build" -InputObject ""

}
