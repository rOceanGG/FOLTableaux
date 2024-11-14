MAX_CONSTANTS = 10



# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    return 0

# Break the formula into LHS, Binary Connective, and RHS
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
    return breakToParts(fmla)[0]

# Return the connective symbol of a binary connective formula
def con(fmla):
    return breakToParts[1]

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    breakToParts[2]


# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    return None

#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    return 0

#------------------------------------------------------------------------------------------------------------------------------:
#                   DO NOT MODIFY THE CODE BELOW. MODIFICATION OF THE CODE BELOW WILL RESULT IN A MARK OF 0!                   :
#------------------------------------------------------------------------------------------------------------------------------:

f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
