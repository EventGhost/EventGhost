SET KEY=HKLM\SOFTWARE\Python\PythonCore\2.5\InstallPath
FOR /F "skip=4 tokens=3*" %%I IN ('REG QUERY "%KEY%" /VE') DO @SET PY25DIR=%%J
SET KEY=HKLM\SOFTWARE\Python\PythonCore\2.6\InstallPath
FOR /F "skip=4 tokens=3*" %%I IN ('REG QUERY "%KEY%" /VE') DO @SET PY26DIR=%%J

FOR /D %%d IN (*) DO CALL:compile %%d
goto:eof

:compile
echo %1
pushd %1
RMDIR build /S /Q
%PY25DIR%Python.exe setup.py build
COPY build\lib.win32-2.5\*.pyd ..\..\lib25\site-packages\
%PY26DIR%Python.exe setup.py build
COPY build\lib.win32-2.6\*.pyd ..\..\lib26\site-packages\
popd
goto:eof
