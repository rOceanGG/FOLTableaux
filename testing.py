#Testing for con()
def con(fmla):
    if fmla[0] == '(':
        depth = 0
        for x in range(len(fmla)-1):
            if fmla[x] == '(':
                depth += 1
            elif fmla[x] == ')':
                depth -= 1
            elif depth == 1 and fmla[x:x+2] in ['/\\', '\\/', '=>']:
                return fmla[x:x+2]
    else:
        return ''

formula1 = "(p=>q)"
formula2 = "(p\\/q)"
formula3 = "(p/\\q)"
formula4 = "((p=>q)\\/x)"

print("Test 1: Formula: " + formula1 + ", Expected: =>, Actual: " + str(con(formula1)))
print("Test 2: Formula: " + formula2 + ", Expected: \\/, Actual: " + str(con(formula2)))
print("Test 3: Formula: " + formula3 + ", Expected: /\\, Actual: " + str(con(formula3)))
print("Test 4: Formula: " + formula4 + ", Expected: \\/, Actual: " + str(con(formula4)))