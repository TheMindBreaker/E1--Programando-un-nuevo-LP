import re as regex
import sys
from tabulate import tabulate


#Define Patterns 
real_pat = r'[-]?[\.]?\d+[.]?\d*[(e|E)]?[-]?\d*'
var_pat = r'[A-Za-z][\w]*'
comment_pat= r'//.*'
operand_pat  = r'[=*+-/^@]'
parent_pat = '[()]'
compare_pat = "[@]"

def lexerAritmetico(file):
    #Open File to read
    try:
        with open(file, "r") as input_file:
            #Get Operation Lines
            for line in input_file.readlines():
                #Remove Empty Lines
                if line.strip():
                    result = patternSplit(line)
                    #print Tables
                    print(tabulate(result[0],["Token", "Tipo"], tablefmt="grid"))
                    #print Errors
                    for error in result[1]:
                        if(error != ""):
                            print(error)
    except IOError:
        print("Not able to find the file or to open it")
                
    
def patternSplit(line):
    result = [[],[]]
    

    #Parentesis and comparison Correction
    line = line.replace("(", " ( ")
    line = line.replace(")", " ) ")
    line = line.replace("==", "@")
    
    #Splitting Base on Pattern
    splitting = regex.findall(real_pat + "|" + var_pat + "|" + comment_pat + "|" + operand_pat + "|" + parent_pat + "|" + compare_pat,line)

    #Check valid pattern to apply rules
    for x in splitting:
        if regex.match(real_pat,x):
            if(regex.match('-?\d+(.?)[Ee]',x)):
                result[1].append("Error: Se espera un operador despues de un real o decimal")
            result[0].append([x, "Real"])
            
        elif regex.match(var_pat,x):
            result[0].append([x, "Variable"])
        elif regex.match(comment_pat,x):
            result[0].append([x,"Commentario"])
        elif regex.match(operand_pat,x):
            res = operandRuller(x, splitting)
            result[0].append(res[0])
            result[1].append(res[1])
        elif regex.match(parent_pat,x):
            res = parentesisHandler(x, splitting)
            result[0].append(res[0])
            result[1].append(res[1])
            
    return result
    

#Function to check parentesis completed
def parentesisHandler(value, line):
    result = []
    error  = ""
    if(value == '('):
        if ")" not in line:
            error = "Error: Falta Cierre de Parentesis"
        else: 
            if(line.index(value) < line.index(")")):
                error = "Error: El cierre de parentesis se encuentral es posicion incorrecta"

        result = [value, "Parentecis Abierto"]
    if(value == ')'):
        result = [value, "Parentecis Cerrado"]
    return [result, error]

def operandRuller(value, line): 
    result = []
    error = ""
    pos = line.index(value)

    #Detect Side Vars or Reals
    if(regex.match(comment_pat, line[pos + 1]) or regex.match(operand_pat, line[pos + 1])):
        #Exclude some failed to detec regex
        if(regex.match(real_pat,line[pos + 1])):
            error += ""
        else:
            error += "Error: Falta valor valido despues del operador "
    


    #Check Operation Type
    match value:
        case "=":
            result = [value,"Igualacion"]
        case "*":
            result = [value,"Multiplicacion"]
        case "+":
            result = [value,"Sumatoria"]
        case "-":
            result = [value,"Resta"]
        case "/":
            result = [value,"Division"]
        case "^":
            result = [value,"Potencia"]
        case "@":
            result = ["==","Comparacion"]
    return [result, error]

if(len(sys.argv) == 2):
    if regex.match(r'.*\.txt',sys.argv[1]):
        lexerAritmetico(sys.argv[1])
    else:
        print("Error: File format is not correct, it should be txt format :" + sys.argv[1])
else:
    print("Error: Missing File Name    python main.py  filename.txt :" + sys.argv[1])
