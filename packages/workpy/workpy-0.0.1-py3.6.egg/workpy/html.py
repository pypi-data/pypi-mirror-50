from .base import *
from .file import *

def html(t, b=None):
	t = t.title()
	b = b or f'<h1>{t}</h1>'
	d = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>%s</title>\n\t<meta charset="utf-8">\n\t'
	d += '<link rel="stylesheet" href="/css/bootstrap.min.css">\n\t'
	d += '<script src="/js/jquery.min.js"></script>\n\t'
	d += '<script src="/js/bootstrap.min.js"></script>\n</head>\n<body>\n%s\n</body>\n</html>\n'
	return d % (t, b)

def h5demo(m, w=0, p=None):
	if not m or len(m.strip()) == 0:
		print('Param m is None, do nothing')
		return
	base = p or desktop()
	p = os.path.join(base, m.lower())
	mkdir(p)
	f = os.path.join(p, m.lower()+'.html')
	d = html(m)
	if not os.path.exists(f):
		with open(f, 'w', encoding='utf-8') as fd:
			fd.write(d)
		print(f'{f} created!')
	elif w == 1:
		with open(f, 'w', encoding='utf-8') as fd:
			fd.write(d)
		print(f'{f} rewrited!')

if __name__ == '__main__':
	h5demo('test')