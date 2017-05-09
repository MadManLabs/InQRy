import platform
import re
from inqry.system_specs import diskutility
from inqry.system_specs import system_profiler


class SystemSpecs(object):
    """Represents the machine's system specifications. A SystemSpec instance
     has several machine components that are accessible via simple property
     methods.

    A SystemSpecs object should also be able to be used the same way,
    regardless of which operating system the specs were generated from.

    A SystemSpecs instance is platform agnostic, but does contain the os_type
    attribute"""

    def __init__(self, hardware_overview=None, internal_storage=None, os_type=None):
        self.os_type = os_type or platform.system()
        self.hardware_overview = hardware_overview or system_profiler.get_hardware_overview()
        self.internal_storage = internal_storage or diskutility.get_internal_storage()

    @property
    def form_factor(self):
        return self._identify_mac_form_factor() if self.os_type == 'Darwin' else self._identify_pc_form_factor()

    def _identify_mac_form_factor(self):
        mac_portable_pattern = re.compile(r'MacBook(Pro|Air|)([0-9]|[1-9][0-9]),[1-9]')
        return 'Portable' if re.match(mac_portable_pattern, self.model_identifier) else 'Desktop'

    def _identify_pc_form_factor(self):
        pc_portable_pattern = re.compile(r'')  # TODO: Write regexp for PC form factor
        return 'Portable' if not re.match(pc_portable_pattern, self.model_identifier) else 'Desktop'

    @property
    def model_name(self):
        try:
            return self.hardware_overview.get('Model Name')
        except AssertionError:
            raise AssertionError('Model Name key contains no value')

    @property
    def model_identifier(self):
        try:
            return self.hardware_overview.get('Model Identifier')
        except AssertionError:
            raise AssertionError('Model Identifier key contains no value')

    @property
    def serial_number(self):
        try:
            return self.hardware_overview.get('Serial Number (system)')
        except AssertionError:
            raise AssertionError('Serial Number key contains no value')

    @property
    def cpu_name(self):
        return self.hardware_overview.get('Processor Name')

    @property
    def cpu_processors(self):
        return self.hardware_overview.get('Number of Processors')

    @property
    def cpu_cores(self):
        return self.hardware_overview.get('Total Number of Cores')

    @property
    def cpu_speed(self):
        return self.hardware_overview.get('Processor Speed')

    @property
    def memory(self):
        return self.hardware_overview.get('Memory')

    @property
    def drive_count(self):
        return len(self.storage)

    @property
    def storage(self):
        return {'Drive {}'.format(disk_count): '{} {} ({})'.format(disk.size, disk.type, disk.device_name) for
                disk_count, disk in enumerate(self.internal_storage, 1)}

    @property
    def drive1(self):
        try:
            return self.storage['Drive 1']
        except KeyError:
            return str("")

    @property
    def drive2(self):
        try:
            return self.storage['Drive 2']
        except KeyError:
            return str("")

    @property
    def drive3(self):
        try:
            return self.storage['Drive 3']
        except KeyError:
            return str("")

    @property
    def drive4(self):
        try:
            return self.storage['Drive 4']
        except KeyError:
            return str("")
