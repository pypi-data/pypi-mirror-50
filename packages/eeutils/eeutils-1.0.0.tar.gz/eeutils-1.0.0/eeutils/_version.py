__version__ = "1.0.0"
__version_info__ = tuple(map(int, __version__.split(".")))

if len(__version_info__) >= 2:
    __major_version__ = (".").join(
        map(str, __version_info__[:2]))
else:
    __major_version__ = __version__

__release__ = __version__
