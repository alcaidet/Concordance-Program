# hash_map.py
# ===================================================
# Tiffanie Alcaide
# CS 261
#
# Implement a hash map with chaining
# ===================================================

class SLNode:
	def __init__(self, key, value):
		self.next = None
		self.key = key
		self.value = value

	def __str__(self):
		return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
	def __init__(self):
		self.head = None
		self.size = 0

	def add_front(self, key, value):
		"""Create a new node and inserts it at the front of the linked list
		Args:
			key: the key for the new node
			value: the value for the new node"""
		new_node = SLNode(key, value)
		new_node.next = self.head
		self.head = new_node
		self.size = self.size + 1

	def remove(self, key):
		"""Removes node from linked list
		Args:
			key: key of the node to remove """
		if self.head is None:
			return False
		if self.head.key == key:
			self.head = self.head.next
			self.size = self.size - 1
			return True
		cur = self.head.next
		prev = self.head
		while cur is not None:
			if cur.key == key:
				prev.next = cur.next
				self.size = self.size - 1
				return True
			prev = cur
			cur = cur.next
		return False

	def contains(self, key):
		"""Searches linked list for a node with a given key
		Args:
			key: key of node
		Return:
			node with matching key, otherwise None"""
		if self.head is not None:
			cur = self.head
			while cur is not None:
				if cur.key == key:
					return cur
				cur = cur.next
		return None

	def __str__(self):
		out = '['
		if self.head != None:
			cur = self.head
			out = out + str(self.head)
			cur = cur.next
			while cur != None:
				out = out + ' -> ' + str(cur)
				cur = cur.next
		out = out + ']'
		return out


def hash_function_1(key):
	hash = 0
	for i in key:
		hash = hash + ord(i)
	return hash


def hash_function_2(key):
	hash = 0
	index = 0
	for i in key:
		hash = hash + (index + 1) * ord(i)
		index = index + 1
	return hash


class HashMap:
	"""
	Creates a new hash map with the specified number of buckets.
	Args:
		capacity: the total number of buckets to be created in the hash table
		function: the hash function to use for hashing values
	"""

	def __init__(self, capacity, function):
		self._buckets = []
		for i in range(capacity):
			self._buckets.append(LinkedList())
		self.capacity = capacity
		self._hash_function = function
		self.size = 0

	def clear(self):
		"""
		Empties out the hash table deleting all links in the hash table.
		"""
		# re-initialize self._buckets
		self._buckets = []
		self.size = 0
		for i in range(self.capacity):
			self._buckets.append(LinkedList())



	def get(self, key):
		"""
		Returns the value with the given key.
		Args:
			key: the value of the key to look for
		Return:
			The value associated to the key. None if the link isn't found.
		"""
		# return None if the key doesn't exist
		if not self.contains_key(key):
			return None
		else:
			index = self.get_index(key) # get the index of the key

			# begin traversal of the linked list until we reach the key
			cur_node = self._buckets[index].head
			while cur_node.key != key:
				cur_node = cur_node.next

			return cur_node.value

	def resize_table(self, capacity):
		"""
		Resizes the hash table to have a number of buckets equal to the given
		capacity. All links need to be rehashed in this function after resizing
		Args:
			capacity: the new number of buckets.
		"""
		# make a new HashMap with the desired capacity
		new_map = HashMap(capacity, self._hash_function)

		# for each linked list in the map, rehash and add to new_map
		for i in self._buckets:
			cur_node = i.head
			while cur_node is not None:
				index = self._hash_function(cur_node.key) % capacity # get the new index for the key
				new_map._buckets[index].add_front(cur_node.key, cur_node.value) # add the key-value pair to the new map
				cur_node = cur_node.next # move to the next node in the linked list
		self._buckets = new_map._buckets # reassign self._buckets to the new_map
		self.capacity = capacity


	def put(self, key, value):
		"""
		Updates the given key-value pair in the hash table. If a link with the given
		key already exists, this will just update the value and skip traversing. Otherwise,
		it will create a new link with the given key and value and add it to the table
		bucket's linked list.

		Args:
			key: they key to use to has the entry
			value: the value associated with the entry
		"""


		index = self.get_index(key) # get the index
		cur_list = self._buckets[index] # this is the linked list

		# remove the key and assign the returned boolean in removed
		removed = cur_list.remove(key)
		cur_list.add_front(key, value) # re-add the key with updated value

		# if removed is false, then a new key was added so increase size by 1
		if not removed:
			self.size += 1




	def remove(self, key):
		"""
		Removes and frees the link with the given key from the table. If no such link
		exists, this does nothing. Remember to search the entire linked list at the
		bucket.
		Args:
			key: they key to search for and remove along with its value
		"""

		# if the key doesn't exist, exit the function
		if not self.contains_key(key):
			return
		else:
			index = self.get_index(key) # get the index of the key
			linked_list = self._buckets[index] # now get the entire linked list
			linked_list.remove(key) # call the remove function from the linked list
			self.size -= 1 # subtract 1

	def contains_key(self, key):
		"""
		Searches to see if a key exists within the hash table

		Returns:
			True if the key is found False otherwise

		"""
		# call the linked list contains() method for each bucket
		for i in self._buckets:
			if i.contains(key):
				return True
		return False

	def empty_buckets(self):
		"""
		Returns:
			The number of empty buckets in the table
		"""
		count = 0
		for i in self._buckets:
			if i.size == 0: # here we access the size property of the linked list
				count += 1
		return count

	def table_load(self):
		"""
		Returns:
			the ratio of (number of links) / (number of buckets) in the table as a float.

		"""
		load = self.size / self.capacity
		return load

	def __str__(self):
		"""
		Prints all the links in each of the buckets in the table.
		"""

		out = ""
		index = 0
		for bucket in self._buckets:
			out = out + str(index) + ': ' + str(bucket) + '\n'
			index = index + 1
		return out

	def get_index(self, key):
		"""
			Helper function to get the index of the key
			Returns: index
		"""
		index = self._hash_function(key) % self.capacity
		return index
