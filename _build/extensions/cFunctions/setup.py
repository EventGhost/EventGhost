from distutils.core import setup
from distutils.extension import Extension

setup(
    name='cFunctions',
    version='1.0',
    ext_modules=[
        Extension(
            'cFunctions',
            [
                'registry_funcs.c',
                'hooks.c',
                'keyhook.c',
                'mousehook.c',
                'utils.c',
                'win_funcs.c',
                'main.c'
            ],
            libraries=['user32', 'ole32', 'Advapi32'],
        )
    ],
)
