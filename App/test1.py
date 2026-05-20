from collections import defaultdict

chunks = ["a-b a--b ","a-","b"];queries = ["a-b","a","b"]
data = defaultdict(int)
currentValid = ''
for x in ''.join(chunks)+' ':
    if x==' ' and currentValid:
        if currentValid[:-1]=='-':currentValid = currentValid[:-1]
        data[currentValid] += 1
        currentValid = ''
    elif x=='-':
        if currentValid and currentValid[-1]=='-':currentValid = currentValid[:-1];continue
        else:currentValid += x
    else:currentValid += x
print(data)