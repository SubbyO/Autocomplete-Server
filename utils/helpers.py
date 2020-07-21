'''
  Wrap item in string
'''
def strBase(item=None):
	if item is None:
		return str()
	else:
		return str(item)

'''
  Wrap item in tuple
'''
def tupleBase(item=None):
	if item is None:
		return tuple()
	else:
		return tuple([item])

'''
  Convert strings to a standard syntax: all lowercase and without punctuation
'''
def normalizeString(string):
	punctuation ='.?!,'
	return str(''.join([c.lower() for c in string if c not in punctuation]))