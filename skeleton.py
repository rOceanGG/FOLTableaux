MAX_CONSTANTS = 10
NOT = '~'
AND = '/\\'
OR = '\\/'
IMPLIES = '=>'
CONNECTIVES = [AND, OR, IMPLIES]


# Break the formula into LHS, Binary Connective, and RHS
def breakToParts(fmla):
    try:
        if fmla[0] == '(':
            depth = 0
            for x in range(len(fmla)-1):
                if fmla[x] == '(':
                    depth += 1
                elif fmla[x] == ')':
                    depth -= 1
                elif depth == 1 and fmla[x:x+2] in CONNECTIVES:
                    return [fmla[1:x], fmla[x:x+2], fmla[x+2:len(fmla) -1]]
        else:
            return ['','','']
    except:
        return ['', '', '']
    return ['', '', '']

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


# Parse a formula, consult parseOutputs for return values.
def parse(fmla):

    # The following three functions are used to detect Propositional Formulae
    def isProposition(formula):
        return formula in ['p', 'q', 'r', 's']

    def isSymbol(formula):
        return formula in CONNECTIVES
    
    def isPropositionalFormula(formula):
        if isProposition(formula):
            return 6 # a proposition
        elif len(formula) > 1 and formula[0] == NOT and isPropositionalFormula(formula[1:]) != 0:
            return 7 # a negation of a propositional formula
        else:
            parts = breakToParts(formula)
            if parts == ['','','']:
                return 0 # not a formula
            else:
                if isPropositionalFormula(parts[0]) != 0 and isSymbol(parts[1]) and isPropositionalFormula(parts[2]) != 0:
                    return 8 # a binary connective propositional formula
                else: 
                    return 0 # not a formula

    def isVariable(formula):
        return formula in ['x','y','z','w']
    
    def isPredicate(formula):
        return formula in ['P','Q','R','S']
    
    def isQuantifier(formula):
        return formula in ['A', 'E']
    
    #Note that isSymbol() function is the same because there are no new binary connectives

    def isFOLFormula(formula):
        if (len(formula) == 6 and isPredicate(formula[0]) and 
        formula[1] == '(' and isVariable(formula[2]) and formula[3] == ','
        and isVariable(formula[4]) and formula[5] == ')'):
            return 1 # an atom
        elif len(formula) > 2 and formula[0] == NOT and isFOLFormula(formula[1:]) != 0:
            return 2 # a negation of a first order logic formula
        elif len(formula) > 3 and isQuantifier(formula[0]) and isVariable(formula[1]) and isFOLFormula(formula[2:]) != 0:
            return 3 if formula[0] == 'A' else 4
        # a universally quantified first order logic formula, an existentially quantified first order logic formula
        else:
            parts = breakToParts(formula)
            if parts == ['','','']:
                return 0
            else:
                if isFOLFormula(parts[0]) != 0 and isSymbol(parts[1]) and isFOLFormula(parts[2]) != 0:
                    return 5
                else:
                    return 0

    # If either quantifier is present, then start checking for FOL
    if 'A' in fmla or 'E' in fmla or 'P' in fmla or 'Q' in fmla or 'R' in fmla or 'S' in fmla:
        return isFOLFormula(fmla)
        
    # Otherwise check for Propositional Logic
    else:
        return isPropositionalFormula(fmla)
        



# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    queue = [fmla]

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
