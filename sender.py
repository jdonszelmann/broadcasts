

import broadcasts


b1 = broadcasts.Sender(37020)

for i in range(1000):
	b1.send("hello world")

b1.stop()