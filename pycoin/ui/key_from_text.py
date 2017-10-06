from .. import encoding
from ..serialize import b2h
from .validate import netcode_and_type_for_text
from pycoin.key.electrum import ElectrumWallet
from pycoin.key.BIP32Node import BIP32Node
from pycoin.key.Key import Key


def key_from_text(text, generator=None, is_compressed=None, key_types=None):
    """
    This function will accept a BIP0032 wallet string, a WIF, or a bitcoin address.

    The "is_compressed" parameter is ignored unless a public address is passed in.
    """

    netcode, key_type, data = netcode_and_type_for_text(text)

    if key_types and key_type not in key_types:
        raise encoding.EncodingError("bad key type: %s" % key_type)

    if key_type in ("pub32", "prv32"):
        return BIP32Node.from_wallet_key(generator, text)

    if key_type == 'wif':
        is_compressed = (len(data) > 32)
        if is_compressed:
            data = data[:-1]
        return Key(
            secret_exponent=encoding.from_bytes_32(data),
            generator=generator,
            prefer_uncompressed=not is_compressed, netcode=netcode)

    if key_type == 'address':
        return Key(hash160=data, is_compressed=is_compressed, netcode=netcode)

    if key_type == 'elc_seed':
        return ElectrumWallet(initial_key=b2h(data), generator=generator)

    if key_type == 'elc_prv':
        return ElectrumWallet(master_private_key=encoding.from_bytes_32(data), generator=generator)

    if key_type == 'elc_pub':
        return ElectrumWallet(master_public_key=data, generator=generator)

    raise encoding.EncodingError("unknown text: %s" % text)
