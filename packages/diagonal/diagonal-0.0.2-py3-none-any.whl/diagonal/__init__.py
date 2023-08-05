def isSquare(arr,m,n):
    if(m != n):
        return 0

    flag = 0
    for i in arr:
        if(len(i) != n):
            flag = 1
            break

    if(flag):
        return 0
    return 1

def main(arr):
    m = len(arr)
    n = len(arr[0])
    if(not isSquare(arr,m,n)): return "- Not a square matrix"
    
    diagonal = []
    for i in range(m):
        diagonal.append(arr[i][i])

    return diagonal

def anti(arr):
    m = len(arr)
    n = len(arr[0])
    if(not isSquare(arr,m,n)): return "- Not a square matrix"
    
    diagonal = []
    m=m-1
    for i in range(m+1):
        diagonal.append(arr[i][m-i])

    return diagonal

def isFine(arr,n):
    for i in arr:
        if(len(i) != n):
            return 0
    return 1

def upFrom0(arr):
    m = len(arr)
    n = len(arr[0])
    if(not isFine(arr,n)): return "- All rows should have same number of items"
    
    diagonals = []
    for k in range(m):
        i = k
        j = 0
        d = []
        while(i>=0 and j<n):
            d.append(arr[i][j])
            #print(arr[i][j], end=" ")
            i-=1
            j+=1
        #print()
        diagonals.append(d)
    
    for k in range(1,n):
        i = m-1
        j = k
        d=[]
        while(i>=0 and j<n):
            d.append(arr[i][j])
            #print(arr[i][j], end=" ")
            i-=1
            j+=1
        #print()
        diagonals.append(d)
    return diagonals

def downFrom0(arr):
    diagonals = upFrom0(arr)
    for i in range(len(diagonals)):
        diagonals[i] = diagonals[i][::-1]
    return diagonals

def downFromM(arr):
    m = len(arr)
    n = len(arr[0])
    if(not isFine(arr,n)): return "- All rows should have same number of items"
    
    diagonals = []
    for k in range(m):
        i = m -1 -k
        j = 0
        d = []
        while(i<m and j<n):
            d.append(arr[i][j])
            i+=1
            j+=1
        diagonals.append(d)
    
    for k in range(1, n):
        i = 0
        j = k
        d = []
        while(i<m and j<n):
            d.append(arr[i][j])
            i+=1
            j+=1
        diagonals.append(d)

    return diagonals

def upFromM(arr):
    diagonals = downFromM(arr)
    for i in range(len(diagonals)):
        diagonals[i] = diagonals[i][::-1]
    return diagonals

def zigzagUp(arr):
    diagonals = upFrom0(arr)
    for i in range(len(diagonals)):
        if(i%2==1):
            diagonals[i] = diagonals[i][::-1]
    zigzag = []
    for i in diagonals:
        for j in i:
            zigzag.append(j)
    
    return zigzag

def zigzagDown(arr):
    diagonals = upFrom0(arr)
    for i in range(len(diagonals)):
        if(i%2==0):
            diagonals[i] = diagonals[i][::-1]
    zigzag = []
    for i in diagonals:
        for j in i:
            zigzag.append(j)
    
    return zigzag

def get(arr, start = "0", direction = "up", type="all"):
    if(type == "all"): #get all diagonals
        if(start == "0"):
            if(direction == "up"):
                return upFrom0(arr)
            elif(direction == "down"):
                return downFrom0(arr)
            else:
                return "- Keyword Error"
        elif( start == "m"):
            if(direction == "up"):
                return upFromM(arr)
            elif(direction == "down"):
                return downFromM(arr)
            else:
                return "- Keyword Error"
    else: #only main diagonals
        if(type == "main"):
            return main(arr)
        elif(type == "anti"):
            return anti(arr)
        elif(type == "zigzag"):
            if(direction == "up"):
                return zigzagUp(arr)
            elif(direction == "down"):
                return zigzagDown(arr)
            else:
                return "- Keyword error"
        else:
            return "- Keyword Error"