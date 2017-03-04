import sys
import pip

OS = sys.platform


def install(package):
    pip.main(['install', package])


if OS == 'win32':
    install("pypiwin32")
    install("wmi")
    from inqry.system_specs import windows_system_profiler as system_profiler
elif OS == 'darwin':
    from inqry.system_specs import mac_system_profiler as system_profiler
    from inqry.system_specs import macdisk
else:
    raise OSError('Operating system unknown')