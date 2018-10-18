# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import os
from distutils.core import Command
import sys
from subprocess import Popen, PIPE

import logging

logger = logging.getLogger()

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
EXTENSIONS_PATH = os.path.join(BASE_PATH, '..', 'extensions')

RAW_INPUT_HOOK_SRC = os.path.join(EXTENSIONS_PATH, 'RawInputHook.dll')
RAW_INPUT_HOOK_DST = 'plugins\RawInput'

MCE_IR_SRC = os.path.join(EXTENSIONS_PATH, 'MceIr.dll')
MCE_IR_DST = 'plugins\MceRemote'

TASK_HOOK_SRC = os.path.join(EXTENSIONS_PATH, 'TaskHook.dll')
TASK_HOOK_DST = 'plugins\Task'

C_FUNCTIONS_SRC = os.path.join(EXTENSIONS_PATH, 'cFunctions')
C_FUNCTIONS_DST = 'pyd_imports'

DX_JOYSTICK_SRC = os.path.join(EXTENSIONS_PATH, '_dxJoystick')
DX_JOYSTICK_DST = 'pyd_imports'

VISTA_VOL_EVENTS_SRC = os.path.join(EXTENSIONS_PATH, 'VistaVolEvents')
VISTA_VOL_EVENTS_DST = 'pyd_imports'

WIN_USB_SRC = os.path.join(EXTENSIONS_PATH, 'WinUsbWrapper')
WIN_USB_DST = 'lib27\site-packages'


class Extension(object):
    def __init__(self, name, solution_path, destination_path):
        self.name = name
        self.solution_path = solution_path
        self.destination_path = destination_path


class BuildEXT(Command):
    user_options = [
        ("build-base=", None, "temp directory build location"),
        ("dist-dir=", 'distribution location'),
        ("threaded-build", None, "build extensions at the same time"),

    ]

    boolean_options = ["threaded-build"]

    def initialize_options(self):
        self.build_base = None
        self.dist_dir = None
        self.threaded_build = False

    def finalize_options(self):
        pass

    def run(self):
        dist_dir = self.dist_dir
        tmp_folder = self.build_base

        extensions_build_path = os.path.join(tmp_folder,  'extensions')

        if not os.path.exists(extensions_build_path):
            os.mkdir(extensions_build_path)

        extensions = self.distribution.ext_modules

        import msvc
        environment = msvc.Environment()

        import threading
        folder_lock = threading.Lock()

        should_exit = False

        def do(build_ext, evt):
            global should_exit

            name = build_ext.name
            solution_path = build_ext.solution_path

            if 'pyd_imports' in build_ext.destination_path:
                destination_path = os.path.join(
                    tmp_folder,
                    build_ext.destination_path
                )
                with folder_lock:
                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)
                    if destination_path not in sys.path:
                        sys.path.insert(0, destination_path)
            else:
                destination_path = os.path.join(
                    dist_dir,
                    build_ext.destination_path
                )

            build_path = os.path.join(extensions_build_path, name)

            logger.log(22, '--- updating solution {0}'.format(name))

            solution, output_paths = environment.update_solution(
                os.path.abspath(solution_path),
                os.path.abspath(build_path)
            )
            evt.wait(0.5)

            build_command = environment.get_build_command(solution)
            logger.log(22, '--- building {0}'.format(name))

            evt.wait(0.5)

            proc = Popen(build_command, stdout=PIPE, stderr=PIPE)

            if sys.version_info[0] >= 3:
                empty_return = b''
            else:
                empty_return = ''

            log_data = []

            while proc.poll() is None:
                for line in iter(proc.stdout.readline, empty_return):
                    if line:
                        log_data += [line.rstrip()]

            for project_name, output_file in output_paths.items():
                if output_file is None:
                    out_data = [
                        'BUILD FAILURE',
                        'Solution: {0}'.format(name),
                        'Project: {0}'.format(project_name),
                        'No File path returned.'
                    ]

                    logger.log(22, '\n'.join(out_data))

                    should_exit = True
                    break

                if not os.path.exists(output_file):
                    test_output_file = os.path.join(build_path, output_file)
                    if not os.path.exists(test_output_file):
                        out_data = [
                            'BUILD FAILURE',
                            'Solution: {0}'.format(name),
                            'Project: {0}'.format(project_name),
                            'Output File: {0}'.format(output_file),
                            'Compilation Failed.'
                        ]

                        logger.log(22, '\n'.join(out_data))
                        should_exit = True
                        break
                    else:
                        output_file = test_output_file

                output_file_path = os.path.join(
                    destination_path,
                    name
                )

                if os.path.exists(output_file_path):
                    os.remove(output_file_path)

                print 'copying.. ' + output_file + ' --> ' + destination_path

                build_ext.destination_path = destination_path
                self.copy_file(output_file, destination_path)

            with folder_lock:
                print '\n'.join(log_data)

            evt.set()

        events = []
        for ext in extensions:
            event = threading.Event()
            events += [event]

            if self.threaded_build:
                t = threading.Thread(target=do, args=(ext, event))
                t.daemon = True
                t.start()
            else:
                do(ext, event)

        for event in events:
            event.wait()
            if should_exit:
                sys.exit(1)

        del sys.modules['cFunctions']


RawInputHook = Extension(
    'RawInputHook.dll',
    RAW_INPUT_HOOK_SRC,
    RAW_INPUT_HOOK_DST
)

MceIr = Extension(
    'MceIr.dll',
    MCE_IR_SRC,
    MCE_IR_DST
)

TaskHook = Extension(
    'TaskHook.dll',
    TASK_HOOK_SRC,
    TASK_HOOK_DST
)

cFunctions = Extension(
    'cFunctions.pyd',
    C_FUNCTIONS_SRC,
    C_FUNCTIONS_DST
)

dxJoystick = Extension(
    '_dxJoystick.pyd',
    DX_JOYSTICK_SRC,
    DX_JOYSTICK_DST
)

VistaVolEvents = Extension(
    'VistaVolEvents.pyd',
    VISTA_VOL_EVENTS_SRC,
    VISTA_VOL_EVENTS_DST
)

WinUsbWrapper = Extension(
    'WinUsbWrapper.dll',
    WIN_USB_SRC,
    WIN_USB_DST
)
