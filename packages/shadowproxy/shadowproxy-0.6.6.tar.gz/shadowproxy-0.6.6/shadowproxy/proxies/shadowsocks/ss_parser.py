import socket
import iofree


@iofree.parser
def ss_reader(cipher) -> None:
    parser = yield from iofree.get_parser()
    iv = yield from iofree.read(cipher.IV_SIZE)
    decrypt = cipher.make_decrypter(iv)
    while True:
        data = yield from iofree.read_more()
        parser.write(decrypt(data))


@iofree.parser
def ss_server_reader(cipher) -> None:
    "result queue: [target_addr]"
    parser = yield from iofree.get_parser()
    iv = yield from iofree.read(cipher.IV_SIZE)
    decrypt = cipher.make_decrypter(iv)
    buf = bytearray()
    target_addr = None
    while True:
        data = yield from iofree.read_more()
        data = decrypt(data)
        if target_addr:
            parser.write(data)
        else:
            buf.extend(data)
            target_addr, _ = yield from addr_reader(buf)
            parser.append_result(target_addr)
            if buf:
                parser.write(buf)
                del buf[:]


def addr_reader(buf=None):
    atyp = yield from iofree.read(1, from_=buf)
    if atyp == b"\x01":  # IPV4
        data = yield from iofree.read(4, from_=buf)
        host = socket.inet_ntoa(data)
    elif atyp == b"\x04":  # IPV6
        data = yield from iofree.read(16, from_=buf)
        host = socket.inet_ntop(socket.AF_INET6, data)
    elif atyp == b"\x03":  # hostname
        data = yield from iofree.read(1, from_=buf)
        data += yield from iofree.read(data[0], from_=buf)
        host = data[1:].decode("ascii")
    else:
        raise Exception(f"unknown atyp: {atyp}")
    data_port = yield from iofree.read(2, from_=buf)
    port = int.from_bytes(data_port, "big")
    return (host, port), atyp + data + data_port
