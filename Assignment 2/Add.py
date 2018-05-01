#!/usr/bin/python3

import xmlrpc.server


class Adder:
	@staticmethod
	def network_add(string1, string2):
		if len(string1) <= len(string2):
			string1 = string1.zfill(len(string2))
		else:
			string2 = string2.zfill(len(string1))
		
		zipped = zip(reversed(string1), reversed(string2))
		carry = 0
		final_sum = []
		
		for val1, val2 in zipped:
			curr_sum = int(val1) + int(val2) + carry
			final_sum.append(str(curr_sum % 10))
			carry = curr_sum // 10
		final_sum.append(str(carry))
		
		return ''.join(final_sum)[::-1].lstrip('0')
	

if __name__ == '__main__':
	server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 8000))
	server.register_instance(Adder())
	server.register_function(Adder.network_add)
	server.serve_forever()
