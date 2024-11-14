#Testing for con()
def breakToParts(fmla):
    if fmla[0] == '(':
        depth = 0
        for x in range(len(fmla)-1):
            if fmla[x] == '(':
                depth += 1
            elif fmla[x] == ')':
                depth -= 1
            elif depth == 1 and fmla[x:x+2] in ['/\\', '\/', '=>']:
                return [fmla[1:x], fmla[x:x+2], fmla[x+2:len(fmla) -1]]
    else:
        return ['','','']

# Return the LHS of a binary connective formula
def lhs(fmla):
    parts = breakToParts(fmla)
    return parts[0]

# Return the connective symbol of a binary connective formula
def con(fmla):
    parts = breakToParts(fmla)
    return parts[1]

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    parts = breakToParts(fmla)
    return parts[2]


#Formulas
fmla1 = '~(p=>(q=>p))'
fmla2 = '(~(p=>q)/\\q)'
fmla3 = '(~~~p\\/(q/\\~q))'
fmla4 = '(p=>p)'
fmla5 = '~(p=>p)'
fmla6 = '((p\\/q)/\\'
fmla7 = '(p~q)'
fmla8 = '((p\\/q)/\\(~p\\/~q))'
fmla9 = '(q/\\~(p\\/~p))'
fmla10 = 'p'
fmla11 = '((p\\/q)/\\((p=>~p)/\\(~p=>p)))'
fmla12 = '~~~~~~~~~~~q'
fmla13 = '(ExP(x,x)/\\Ax(~P(x,x)=>P(x,x)))'
fmla14 = '~Ax(P(x,x)/\\~P(x,x))'
fmla15 = '~Ax~Ey~P(x,y)'
fmla16 = 'ExAx(P(x,x)/\\~P(x,x))'
fmla17 = 'ExAy(Q(x,x)=>P(y,y))'
fmla18 = '(Q(x,x)~(P(y,y))'
fmla19 = 'ExEy((Q(x,x)/\\Q(y,y))\\/~P(y,y))'
fmla20 = 'ExEy((Q(x,x)/\\Q(y,y))\\/'
fmla21 = 'Ex~P(x,x)'
fmla22 = '(AxEyP(x,y)/\\EzQ(z,z))'
fmla23 = '(Ax(P(x,x)/\\~P(x,x))/\\ExQ(x,x))'
fmla24 = 'ExEy(P(x,y)/\\Ex~P(x,y))'

print("\nTesting for con()")
print("Test 1 -- Formula: " + fmla1 + ", Expected: " +  ", Actual: " + str(con(fmla1)))
print("Test 2 -- Formula: " + fmla2 + ", Expected: /\\" +  ", Actual: " + str(con(fmla2)))
print("Test 3 -- Formula: " + fmla3 + ", Expected: \\/" +  ", Actual: " + str(con(fmla3)))
print("Test 4 -- Formula: " + fmla4 + ", Expected: =>" +  ", Actual: " + str(con(fmla4)))
print("Test 5 -- Formula: " + fmla6 + ", Expected: /\\" +  ", Actual: " + str(con(fmla6)))

print("\nTesting for lhs()")
print("Test 1 -- Formula: " + fmla1 + ", Expected: " +  ", Actual: " + str(lhs(fmla1)))
print("Test 2 -- Formula: " + fmla2 + ", Expected: ~(p=>q)" +  ", Actual: " + str(lhs(fmla2)))
print("Test 3 -- Formula: " + fmla3 + ", Expected: ~~~p" +  ", Actual: " + str(lhs(fmla3)))
print("Test 4 -- Formula: " + fmla4 + ", Expected: p" +  ", Actual: " + str(lhs(fmla4)))
print("Test 5 -- Formula: " + fmla6 + ", Expected: (p\\/q)" +  ", Actual: " + str(lhs(fmla6)))

print("\nTesting for rhs()")
print("Test 1 -- Formula: " + fmla1 + ", Expected: " +  ", Actual: " + str(rhs(fmla1)))
print("Test 2 -- Formula: " + fmla2 + ", Expected: q" +  ", Actual: " + str(rhs(fmla2)))
print("Test 3 -- Formula: " + fmla3 + ", Expected: (q/\\~q)" +  ", Actual: " + str(rhs(fmla3)))
print("Test 4 -- Formula: " + fmla4 + ", Expected: p" +  ", Actual: " + str(rhs(fmla4)))
print("Test 5 -- Formula: " + fmla6 + ", Expected: " +  ", Actual: " + str(rhs(fmla6)))