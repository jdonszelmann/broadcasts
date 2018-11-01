
# broadcasts

a simple library providing udp broadcasting of any python object. receiver.py and sender.py are examples of how to make a sender and receiver.

# usage:

just copy the broadcasts folder into your project and import it :)
this module is *not* on pip. im just too lazy


# explanation:

a sender broadcasts an object onto a specific port. all receivers connected to the ip of the sender and looking at this port will receive this message. it's like a radio beacon but then with udp :)