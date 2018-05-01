#!/usr/bin/python3

import xmlrpc.client
import xmlrpc.server


class Multiplier:
	adder_address = 'http://localhost:8000/'
	
	@staticmethod
	def set_adder_server(address):
		Multiplier.adder_address = address
	
	@staticmethod
	def network_multiply(string1, string2):
		adder_server = xmlrpc.client.ServerProxy(Multiplier.adder_address)
		
		if len(string1) <= len(string2):
			string1 = string1.zfill(len(string2))
		else:
			string2 = string2.zfill(len(string1))
		
		place = 0
		carry = 0
		products = []
		for val2 in reversed(string2):
			curr_product = ['0' for _ in range(place)]
			for val1 in reversed(string1):
				product = int(val1) * int(val2) + carry
				curr_product.append(str(product % 10))
				carry = product // 10
			curr_product.append(str(carry))
			products.append(''.join(curr_product)[::-1])
			place += 1
		
		final_product = '0'
		for product in products:
			final_product = adder_server.network_add(final_product, product)
		
		return final_product


if __name__ == '__main__':
	server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 8001), allow_none=True)
	server.register_instance(Multiplier())
	server.register_function(Multiplier.network_multiply)
	server.register_function(Multiplier.set_adder_server)
	server.serve_forever()
