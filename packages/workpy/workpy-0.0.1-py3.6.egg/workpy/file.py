from .base import *

def home(a='', *b):
	return os.path.join(os.path.expanduser("~"), a, *b).rstrip('\\')

def desktop(a='', *b):
	return home('Desktop', a, *b)

def mkdir(path):
	if os.path.exists(path):
		print(f'{path} exists! continue.')
		return
	os.makedirs(path.strip().rstrip("\\"))
	print(f'{path} created.')

def rmdir(path):
	if os.path.exists(path):
		os.removedirs(path)
		print(f'{path} deleted.')

if __name__ == '__main__':
	print(home())