

class table:
    
    def __init__(self):
        self.table = {}

    def __str__(self):
        return str(self.table)

    def insert(self,symbol,value):
    	if self.contains(symbol) == False:
    		self.table[symbol] = value
    	# TODO: lanzar exeception si existe? 

    def delete(self,symbol):
    	if self.contains(symbol) == True:
    		del self.table[symbol]

    def update(self,symbol,value):
    	if self.contains(symbol) == True:
    		self.table[symbol] = value
	# TODO: lanzar exeception sino existe? 

    def contains(self,symbol):
    	return self.table.has_key(symbol)

    def lookup(self,symbol):
    	if self.contains(symbol) == True:
    		return self.table[symbol]


if __name__ == "__main__":
    a = table()
    print(a)
    a.insert('a',43)
    a.insert('b',23)
    a.lookup('a')
    print(a.lookup('a'))
    print(a)
