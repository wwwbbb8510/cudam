def recvall(stream):
    """
    receive all the data in the cudam_socket
    :param stream: cudam_socket or request, both of which have recv method
    :return: the whole string received by the cudam_socket
    :rtype: bytearray
    """
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = stream.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data