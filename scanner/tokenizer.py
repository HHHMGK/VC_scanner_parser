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

def tab2space(text : str) -> str:
    return text.replace('\t','    ')

def tokenize(text: str) -> list:
    # Returns the list of tokens and their positions
    lines = tab2space(text).split('\n')
    tokens = []
    pos = []
    cnt_line = 0
    in_multi_comment = False
    for line in lines:
        line+= ' '
        in_comment = in_multi_comment
        in_string = False
        token = ''
        i = 0
        while i < len(line):
            # Skip when in comment
            if in_comment:
                # Stop multi comment when the end of comment is found
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
                    tokens.append(token)
                    pos.append((cnt_line,i-len(token)))
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
            
            # Check seperator, operator, double operator
            c = line[i]
            c2 = ''
            if i+1 < len(line):
                c2 = line[i+1]
            
            if c2 != '' and c+c2 in operator:
                if token != '':
                    tokens.append(token)
                    pos.append((cnt_line,i-len(token)))
                    token = ''
                tokens.append(c+c2)
                pos.append((cnt_line,i))
                i += 2
                continue

            if c in seperator + operator or c==' ':
                if token != '':
                    tokens.append(token)
                    pos.append((cnt_line,i-len(token)))
                    token = ''
                if c != ' ':
                    # tokens.append((c,(cnt_line,i)))
                    tokens.append(c)
                    pos.append((cnt_line,i))
                i += 1
                continue

            # Normal case
            token += c
            i+=1

        cnt_line += 1

    # tokens.append(('$', (cnt_line,0)))
    tokens.append('$')
    pos.append((cnt_line,0))
    return tokens, pos

