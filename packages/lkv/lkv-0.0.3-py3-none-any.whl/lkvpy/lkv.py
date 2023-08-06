def output():
    print('this is a demo. if you are interested, contact 2427080101@qq.com')

def get_food():
	A = ["zijing", "taoli", "yushu", "qingfen", "zhilan", "tingtao", "guanchou", "heyuan"]
	randint = random.randint(0,1000)%8
	print(A[randint])
