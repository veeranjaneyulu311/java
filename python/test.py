
class MyClass:
	"""please inform"""
	i=12345
	
	def f(self):
		return 'hello world'
		
print(MyClass.__name__)
	
if __name__=='__main__':
	print(MyClass.i)
	print(MyClass.f)
	print(MyClass.__doc__)
	