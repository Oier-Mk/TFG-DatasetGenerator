
def train():
    k="None"
    def f(x):
        nonlocal k 
        k = str(x)
    f(4)
    print(k)

train()
