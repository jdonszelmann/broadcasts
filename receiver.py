import broadcasts
import time

def func(message,address):
	print("received message: {} from {}".format(message,address))

r = broadcasts.Receiver("",37020,func)

time.sleep(20)
r.stop()

