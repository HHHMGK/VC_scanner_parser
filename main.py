from utils import tokenizer

if __name__ == '__main__':
    path = './examples/example_gcd.vc'
    # path = './examples/example_fib.vc'
    data = ""
    
    with open(path, 'r') as file:
        data = file.read()
    
    tokens = tokenizer.tokenizer(data)
    
    with open('./examples/example_gcd.vctok', 'w+') as file:
    # with open('./examples/example_fib.vctok', 'w+') as file:
        file.write('\n'.join(tokens))