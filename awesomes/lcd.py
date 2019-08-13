s ='''\
 --      --  --      --  --  --  --  -- 
|  |   |   |   ||  ||   |      ||  ||  |
|  |   |   |   ||  ||   |      ||  ||  |
         --  --  --  --  --      --  -- 
|  |   ||      |   |   ||  |   ||  |   |
|  |   ||      |   |   ||  |   ||  |   |
 --      --  --      --  --      --  -- '''

def get_ch(ch):
	out = []
	for row in s.split('\n'):
		out.append(row[ch*(4):ch*(4)+4])
	return out
   
def print_array(arr):
	x = '-'
	print(f'x{x*len(arr[0])}x')
	for i in arr:
		print(f'|{i}|')
	print(f'x{x*len(arr[0])}x')

def ch2word(word):
    out = get_ch(int(word[0]))
    for ch in word[1:]:
        out = list(map(lambda a, b: a + ' ' + b, out, get_ch(int(ch))))
    return out
    
print_array(ch2word('2354'))
