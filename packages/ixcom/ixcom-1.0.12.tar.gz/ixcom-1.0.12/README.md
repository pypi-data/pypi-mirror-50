This library can be used to communicate with iMAR devices speaking the iXCOM protocol.

Example usage:

    import ixcom

    client = ixcom.client('192.168.1.30')
    client.open_last_free_channel()
    client.realign()