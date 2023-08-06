""" Enables users to command and control tag devices.  """

from enum import IntEnum
from conductor import conductor, airfinder


def compile_msg(self, fmt, data, msg):
    if len(fmt) < len(data):
        raise ValueError("Format must be longer than data!")

    for x in range(len(data)):
        i_fmt = fmt[0] + fmt[i+1]
        struct.pack_into(i_fmt, msg, len(msg), data[i])

    return msg


class Tag(conductor.Module):
    """docstring for Tag"""

    @property
    def enabled(self):
        return bool(self._data.get('enabled'))

    @property
    def metadata(self):
        return self._data.get('assetInfo').get('metadata').get('props')

    @property
    def name(self):
        return self._data.get('value')

    def __repr__(self):
        return '{} {} ({})'.format(self.__class__.__name__, self.subject_id, self.name)


