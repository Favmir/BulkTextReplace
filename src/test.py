import re
expression = 'ahgeMATCHES(ahg)ahk'
text = 'ahgegahahgahahgehzxhk'

def preprocess(expression, text):
    MatchMATCHES = re.search(r'MATCHES\(', expression)
    while(MatchMATCHES != None):
        innerStart = MatchMATCHES.end()
        innerEnd = innerStart
        depth = 1
        for char in expression[innerStart:]:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            if depth == 0:
                break
            innerEnd += 1
        
        count = len(re.findall(expression[innerStart:innerEnd], text))
        expression = expression[:MatchMATCHES.start()] + str(count) + expression[innerEnd+1:]
        MatchMATCHES = re.search(r'MATCHES\(', expression)
    if(re.search(r'MATCHES\((.*)\)',expression) != None):
        Exception("expression containing MATCHES() is not nested properly.")
    return expression

print(preprocess(expression, text))


print(eval('not 1 > 2 and 3 < 4'))