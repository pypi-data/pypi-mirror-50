import pkg_resources

from vips_abi.abi import (  # NOQA
    decode_abi,
    decode_single,
    encode_abi,
    encode_single,
    is_encodable,
    is_encodable_type,
)

try:
    __version__ = pkg_resources.get_distribution('vips-abi').version
except BaseException:
    __version__ = '2.0.0'
