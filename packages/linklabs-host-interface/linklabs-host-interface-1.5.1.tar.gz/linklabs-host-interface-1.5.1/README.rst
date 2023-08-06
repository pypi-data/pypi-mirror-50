ll_ifc.py
============

This is a python implementation of the Link Labs host interface.

To get started, simply instantiate a ``ModuleDriver``::

    import ll_ifc
    mod = ll_ifc.ModuleDriver()

Then, set up the module with your gateway's network token and the desired application token::

    app_token = '12345678901234567890'
    net_token = '12345678'
    mod.set_up(app_token, net_token)

Once that's finished, you can send uplink messages::

    mod.send_message_checked(b'hello')

And receive downlink messages::

    mod.set_downlink_mode('always')
    mod.wait_for_received_message()
