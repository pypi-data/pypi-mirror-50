from vips_hash.backends.auto import (
    AutoBackend,
)
from vips_hash.main import (
    Keccak256,
)

keccak = Keccak256(AutoBackend())
