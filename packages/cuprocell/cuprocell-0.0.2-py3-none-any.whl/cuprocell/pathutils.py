import os

def getAppExe():

    exe = None

    if os.name == 'nt': # Windows
        exe = r'build\bin\Release\procell.exe'
    
    if os.name == 'posix': # Linux
        exe = r'bin\procell'

    return os.path.join(getAppRoot(), 'cuprocell', exe)

def getAppRoot():

    root = None
    
    if os.name == 'nt': # Windows
        root = os.path.expandvars(r'%LOCALAPPDATA%\.cuprocell')
    
    if os.name == 'posix': # Linux
        root = os.path.expandvars(r'$HOME/.cuprocell')

    return root
