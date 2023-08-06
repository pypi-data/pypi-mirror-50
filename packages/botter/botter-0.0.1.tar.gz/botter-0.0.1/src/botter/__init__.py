from collections import namedtuple

__title__ = 'botter'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'BSD 2-clause'
__copyright__ = 'Copyright 2019 Peter Zaircev'
__version__ = '0.0.1'


VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha', serial=0)
