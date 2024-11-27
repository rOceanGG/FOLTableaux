MAX_CONSTANTS = 10
NOT = '~'
AND = '/\\'
OR = '\\/'
IMPLIES = '=>'
CONNECTIVES = [AND, OR, IMPLIES]
FOL_INDICES = [1,2,3,4,5]
PROPOSITIONAL_INDICES = [6,7,8]

class TreeNode():
    def __init__(self, stmt, children=None, values=None, gammas = None):
        self.stmt = stmt
        self.children = children if children else []
        self.values = values if values else []
        self.gammas = gammas if gammas else []

    def addValue(self, value):
        if value not in self.values:
            self.values.append(value)
        
        for c in self.children:
            c.addValue(value)

    
    def addGamma(self, newGamma):
        if newGamma not in self.gammas:
            self.gammas.append(newGamma)
        
        for c in self.children:
            c.addGamma(newGamma)
    


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
    
    def isIntroVar(formula):
        return formula in ['a','b','c','d','e','f','g','h','i','j']
    
    def isPredicate(formula):
        return formula in ['P','Q','R','S']
    
    def isQuantifier(formula):
        return formula in ['A', 'E']
    
    #Note that isSymbol() function is the same because there are no new binary connectives

    def isFOLFormula(formula):
        if (len(formula) == 6 and isPredicate(formula[0]) and 
        formula[1] == '(' and (isVariable(formula[2]) or isIntroVar(formula[2])) and formula[3] == ','
        and (isVariable(formula[4]) or isIntroVar(formula[4])) and formula[5] == ')'):
            return 1 # an atom
        elif len(formula) > 2 and formula[0] == NOT and isFOLFormula(formula[1:]) != 0:
            return 2 # a negation of a first order logic formula
        elif len(formula) > 3 and isQuantifier(formula[0]) and (isVariable(formula[1]) or isIntroVar(formula[1])) and isFOLFormula(formula[2:]) != 0:
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
    FOLPROP = parse(fmla)
    if FOLPROP == 0: return []
    tabRoot = TreeNode(fmla, [], [], [])
    leafProps = []
    queue = [tabRoot]
    newVars = []

    def removeFromQueue(node):
        if node.children:
            for c in node.children:
                removeFromQueue(c)
        
        queue.remove(node)

    def addChildrenToLeaf(node, newChildren):
        if len(node.children) == 0:
            node.children = [TreeNode(c.stmt, [], list(node.values), list(node.gammas)) for c in newChildren]
            for child in node.children:
                queue.append(child)
        else:
            for c in node.children:
                addChildrenToLeaf(c, newChildren)

    if FOLPROP > 5:
        while queue:
            curNode = queue.pop(0)
            fmlaType = parse(curNode.stmt)

            if fmlaType == 6 or (fmlaType == 7 and len(curNode.stmt) == 2):
                curNode.addValue(curNode.stmt)
                if not curNode.children:
                    leafProps.append(curNode.values)

            elif fmlaType == 8:
                left,sym,right = breakToParts(curNode.stmt)
                leftSideNode = TreeNode(left, [], list(curNode.values), list(curNode.gammas))
                rightSideNode = TreeNode(right, [], list(curNode.values), list(curNode.gammas))
                if sym == AND: 
                    addChildrenToLeaf(curNode,[leftSideNode])
                    addChildrenToLeaf(curNode,[rightSideNode])
                elif sym == OR:
                    addChildrenToLeaf(curNode,[leftSideNode, rightSideNode])
                elif sym == IMPLIES:
                    addChildrenToLeaf(curNode, [TreeNode(NOT + left, [], list(curNode.values), list(curNode.gammas)), rightSideNode])
                
            else:
                if curNode.stmt[:2] == NOT + NOT:
                    while curNode.stmt[:2] == NOT + NOT:
                        curNode.stmt = curNode.stmt[2:]
                    queue.insert(0, curNode)
                else:
                    negatedLeft, negatedSym, negatedRight = breakToParts(curNode.stmt[1:])
                    if negatedSym == OR:
                        leftSideNode = TreeNode(NOT + negatedLeft, [], list(curNode.values), list(curNode.gammas))
                        rightSideNode = TreeNode(NOT + negatedRight, [], list(curNode.values), list(curNode.gammas))
                        addChildrenToLeaf(curNode, [leftSideNode])
                        addChildrenToLeaf(curNode, [rightSideNode])
                    elif negatedSym == AND:
                        leftSideNode = TreeNode(NOT + negatedLeft, [], list(curNode.values), list(curNode.gammas))
                        rightSideNode = TreeNode(NOT + negatedRight, [], list(curNode.values), list(curNode.gammas))
                        addChildrenToLeaf(curNode, [leftSideNode, rightSideNode])
                    elif negatedSym == IMPLIES:
                        leftSideNode = TreeNode(negatedLeft, [], list(curNode.values), list(curNode.gammas))
                        rightSideNode = TreeNode(NOT+negatedRight, [], list(curNode.values), list(curNode.gammas))
                        addChildrenToLeaf(curNode, [leftSideNode])
                        addChildrenToLeaf(curNode, [rightSideNode])
                    
    else:
        while queue:
            curNode = queue.pop(0)
            fmlaType = parse(curNode.stmt)

            if fmlaType == 1 or (fmlaType == 2 and len(curNode.stmt) == 7):
                curNode.addValue(curNode.stmt)
                if not curNode.children:
                    leafProps.append(curNode.values)
                
            elif fmlaType == 5:
                left,sym,right = breakToParts(curNode.stmt)
                leftSideNode = TreeNode(left, [], list(curNode.values), list(curNode.gammas))
                rightSideNode = TreeNode(right, [], list(curNode.values), list(curNode.gammas))
                if sym == AND: 
                    addChildrenToLeaf(curNode,[leftSideNode])
                    addChildrenToLeaf(curNode,[rightSideNode])
                elif sym == OR:
                    addChildrenToLeaf(curNode,[leftSideNode, rightSideNode])
                elif sym == IMPLIES:
                    addChildrenToLeaf(curNode, [TreeNode(NOT + left, [], list(curNode.values), list(curNode.gammas)), rightSideNode])
            elif curNode.stmt[:2] == NOT + NOT:
                while curNode.stmt[:2] == NOT + NOT:
                    curNode.stmt = curNode.stmt[2:]
                queue.insert(0, curNode)
            elif fmlaType == 2 and parse(curNode.stmt[1:]) == 5:
                negatedLeft, negatedSym, negatedRight = breakToParts(curNode.stmt[1:])
                if negatedSym == OR:
                    leftSideNode = TreeNode(NOT + negatedLeft, [], list(curNode.values), list(curNode.gammas))
                    rightSideNode = TreeNode(NOT + negatedRight, [], list(curNode.values), list(curNode.gammas))
                    addChildrenToLeaf(curNode, [leftSideNode])
                    addChildrenToLeaf(curNode, [rightSideNode])
                elif negatedSym == AND:
                    leftSideNode = TreeNode(NOT + negatedLeft, [], list(curNode.values), list(curNode.gammas))
                    rightSideNode = TreeNode(NOT + negatedRight, [], list(curNode.values), list(curNode.gammas))
                    addChildrenToLeaf(curNode, [leftSideNode, rightSideNode])
                elif negatedSym == IMPLIES:
                    leftSideNode = TreeNode(negatedLeft, [], list(curNode.values), list(curNode.gammas))
                    rightSideNode = TreeNode(NOT + negatedRight, [], list(curNode.values), list(curNode.gammas))
                    addChildrenToLeaf(curNode, [leftSideNode])
                    addChildrenToLeaf(curNode, [rightSideNode])
            #Delta expansions
            elif fmlaType == 4 or (fmlaType == 2 and parse(curNode.stmt[1:]) == 3):
                if len(newVars) == 10:
                    for c in curNode.children:
                        removeFromQueue(c)
                    leafProps.append(['Return 2'])
                    break
                    
                # Select what the new variable is going to be
                if len(newVars) == 0:
                    newVar = 'a'
                else:
                    newVar = chr(ord(newVars[-1]) + 1)

                newVars.append(newVar)

                    #If existential quantifier, select all of statement aside from the quantifier and quantified variable
                if fmlaType == 4:
                    quantified = curNode.stmt[1]
                    newStmt = curNode.stmt.replace(quantified, newVar)[2:]
                    
                    #Otherwise take all of statement aside from the negation, quantifier and quantified variable
                else:
                    quantified = curNode.stmt[2]
                    newStmt = NOT + curNode.stmt.replace(quantified, newVar)[3:]
                    
                newNode = TreeNode(newStmt, list(curNode.children), list(curNode.values), list(curNode.gammas))
                queue.insert(0, newNode)
                #Put the new variable in all mentioned gamma statements
                for gamma in curNode.gammas:
                    if gamma[0] == NOT:
                        newStmt = gamma.replace(gamma[2], newVar)[3:]
                    else:
                        newStmt = gamma.replace(gamma[1], newVar)[2:]
                        
                    newNode = TreeNode(newStmt, [], list(curNode.values), list(curNode.gammas))
                    addChildrenToLeaf(curNode, [newNode])
            #Gamma expansions
            else:
                curNode.addGamma(curNode.stmt)
                if curNode.stmt[0] == NOT:
                    quantified = curNode.stmt[2]
                else:
                    quantified = curNode.stmt[1]
                
                if len(newVars) == 0:
                    newVars.append('a')
                
                for v in newVars:
                    if curNode.stmt[0] == NOT:
                        newStmt = NOT + curNode.stmt.replace(quantified, v)[3:]
                    else:
                        newStmt = curNode.stmt.replace(quantified, v)[2:]
                    
                    newNode = TreeNode(newStmt, [], list(curNode.values), list(curNode.gammas))
                    addChildrenToLeaf(curNode, [newNode])


                    

    return leafProps
        
    

#check for satisfiability
def sat(tableau):
    #output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    pathways = tableau[0]

    def allUnknown(arr):
        for a in arr:
            for prop in a:
                if prop != 'Return 2':
                    return False
        
        return True

    def containsContradiction(arr):
        for prop in arr:
            if NOT + prop in arr or (len(prop) == 2 and prop[1] in arr):
                return True
        
        return False
    
    if allUnknown(pathways):
        return 2
    for path in pathways:
        if not containsContradiction(path):
            return 1
    
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
