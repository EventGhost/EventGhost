import os
from distutils.core import setup
from distutils.extension import Extension

sdkPath = os.getenv('DXSDK_DIR')
assert sdkPath is not None, "Error: Microsoft DirectX SDK not found"

setup(
    name='_dxJoystick',
    version='1.0',
    ext_modules=[
        Extension(
            '_dxJoystick',
            [
                '_dxJoystick.cpp',
            ],
            include_dirs=[os.path.join(sdkPath, "Include")],
            library_dirs=[os.path.join(sdkPath, "lib", "x86")],
            libraries=[
                'dxguid',
                'dxerr9',
                'dinput8',
            ],
        )
    ],
)
