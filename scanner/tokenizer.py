import json

keyword = []
operator = []
seperator = []
escape = []
comment = []
multi_comment = []
DATAJSON = './scanner/data.json'
with open(DATAJSON, 'r') as file:
    data = json.load(file)
    keyword = data['keyword']
    operator = data['operator']
    seperator = data['seperator']
    escape = data['escape']
    comment = data['comment']
    multi_comment = data['multi_comment']

def removeTabs(text : str) -> str:
    return text.replace('\t','    ')

def tokenizer(text : str):
    lines = text.split('\n')
    tokens = []
    in_comment = False

    for line in lines:
        if line == '' or in_comment:
            continue
        if comment in line:
            i = line.find(comment)
            if i != 0:
                tokens.extend(line[:i].split())
            continue

        if multi_comment[0] in line:
            i = line.find(multi_comment[0])
            if i != 0:
                tokens.extend(line[:i].split())
            in_comment = True

        if multi_comment[1] in line:
            i = line.find(multi_comment[1])+1
            if i < len(line)-1:
                tokens.extend(line[i+1:].split())
            in_comment = False
            continue
        
        if not in_comment:
            tokens.extend(line.split())
    refined_tokens = []

    for tok in tokens:
        temp_toks = [tok]
        for sep in seperator + operator:
            i = 0
            while i < len(temp_toks):
                t = temp_toks[i]    
                split = t.find(sep)
                if split != -1 and t != sep:
                    t1 = t[:split]
                    t2 = t[split+1:]
                    temp_toks1 = temp_toks[:i]
                    temp_toks1.append(t1)
                    temp_toks1.append(sep)
                    temp_toks1.append(t2)
                    temp_toks1.extend(temp_toks[i+1:])
                    temp_toks = temp_toks1
                else:
                    i += 1
        refined_tokens.extend(temp_toks)

    for tok in refined_tokens:
        if tok == '':
            refined_tokens.remove(tok)

    # Fix for strings
    i = 0
    while i < len(refined_tokens): 
        tok = refined_tokens[i]
        if tok == "\"":
            for j in range(i+1, len(refined_tokens)):
                refined_tokens[i] += " " + refined_tokens[j]
                if refined_tokens[j] == "\"":
                    i = j
                    refined_tokens[j] = ''
                    break
                refined_tokens[j] = ''
        i+=1

    # Fix for double operators like '==', '!=', '<=', '>=', '&&', '||'
    for i in range(len(refined_tokens)-1):
        if refined_tokens[i]!='' and refined_tokens[i+1]!='' and refined_tokens[i]+refined_tokens[i+1] in operator:
            refined_tokens[i] = refined_tokens[i]+refined_tokens[i+1]
            refined_tokens[i+1] = ''

    refined_tokens = [tok for tok in refined_tokens if tok != '']

    refined_tokens.append('$')
    
    return refined_tokens

def tokenizer2(text: str) -> list:
    # Returns the list of (token,positional: start line,pos) pairs 
    
    lines = removeTabs(text).split('\n')
    tokens = []
    cnt_line = 0
    in_multi_comment = False
    for line in lines:
        line+= ' '
        in_comment = in_multi_comment
        in_string = False
        token = ''
        i = 0
        while i < len(line):
            if in_comment:
                # Stop multi comment
                if i+1 < len(line) and line[i]+line[i+1] == multi_comment[1]:
                    in_comment = False
                    in_multi_comment = False
                    i += 2
                    continue        
                i += 1
                continue
            
            # String
            if not in_string and line[i] == '\"' and (i == 0 or line[i-1] != '\\'):
                if token != '':
                    tokens.append((token,(cnt_line,i-len(token))))
                    token = ''
                in_string = True
                token += line[i]
                i += 1
                continue
            if in_string:
                token += line[i]
                if line[i] == '\"' and (i == 0 or line[i-1] != '\\'):
                    in_string = False
                i += 1
                continue
            
            # Start multi comment
            if i+1 < len(line) and line[i]+line[i+1] == multi_comment[0]:
                in_comment = True
                in_multi_comment = True
                i+=2
                continue

            # Skip when line comment
            if i+1 < len(line) and line[i]+line[i+1] == comment:
                break
            

            c = line[i]
            c2 = ''
            if i+1 < len(line):
                c2 = line[i+1]
            
            if c2 != '' and c+c2 in operator:
                if token != '':
                    tokens.append((token,(cnt_line,i-len(token))))
                    token = ''
                tokens.append((c+c2,(cnt_line,i)))
                i += 2
                continue

            if c in seperator + operator or c==' ':
                if token != '':
                    tokens.append((token,(cnt_line,i-len(token))))
                    token = ''
                if c != ' ':
                    tokens.append((c,(cnt_line,i)))
                i += 1
                continue

            
            token += c
            i+=1

        cnt_line += 1

    tokens.append(('$', (cnt_line,0)))
    return tokens   

