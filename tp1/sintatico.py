import json


def lerTokens(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            tokens = json.load(arquivo)  # Carrega os dados JSON
            return tokens
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_arquivo}")
        return []
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")
        return []
    

class Token:
    def __init__(self, tipo, lexema, numero_linha):
        self.tipo = tipo  
        self.lexema = lexema  
        self.numero_linha = numero_linha  

    def __str__(self):
        # Aqui, acessa a chave no dicionário tipo_token e retorna o nome dela.
        tipo_token = self.tipo if isinstance(self.tipo, str) else next(iter(self.tipo), 'UNKNOWN')
        return 'Token({tipo}, {lexema}, {numero_linha})'.format(
            tipo=tipo_token,
            lexema=self.lexema, 
            numero_linha=self.numero_linha
        )
    
    def __repr__(self):
        return self.__str__()

    
def atribui(tokens_json):
        vetor_tokens = []
        for token_json in tokens_json:
            tipo = list(token_json['tipo_token'].keys())[0]  
            lexema = token_json['tipo_token'][tipo] 
            numero_linha = token_json['numero_linha']
            
            # Cria a instância do Token e adiciona ao vetor
            vetor_tokens.append(Token(tipo, lexema, numero_linha))

        vetor_tokens.append(Token("EOF", "EOF", numero_linha))
        
        return vetor_tokens

def imprimeErro(especifico = None):
    global token, i
    print('\nErro sintático. ' + repr(token) + ' não esperado na entrada.')
    if especifico: 
        print('\n', especifico,'\n')

def match(tok):
    global token, i
    
    if token.tipo == tok or token.lexema == tok:
        print("Token",repr(token.lexema) + ' reconhecido na entrada.')
        i = i + 1
        if i < len(vetor_tokens):
            token = vetor_tokens[i]
    else:
        imprimeErro("Token não corresponde ao esperado.\nTipo atual:", token.tipo, 
                    "\nTipo atual:", token.lexema, "\nToken esperado:", tok)

def tokensEsperados(lexema, follow_dict):
    for elementos in follow_dict.items():
        if elementos[0] == lexema:
            return elementos[1:] 
    return None  

#--------------------- GRAMATICA ---------------------#

# Programa → Funcao FuncaoSeq
def programa():
    global token, i

    funcao()
    funcaoSeq()

    if token.lexema == "EOF":
        match("EOF")
        print('Fim da análise sintática.')

# FuncaoSeq → Funcao FuncaoSeq | ε
def funcaoSeq():
    global token, i


    if token.lexema == "FUNCTION":
        funcao()
        funcaoSeq()

# Funcao → fn NomeFuncao ( ListaParams ) TipoRetornoFuncao Bloco
def funcao():
    global token, i

    if token.lexema == "FUNCTION":
        match("FUNCTION")
        nomeFuncao()

        if token.lexema == "LBRACKET":
            match("LBRACKET")
            listaParams()
            
            if token.lexema == "RBRACKET":
                match("RBRACKET")
            else:
                imprimeErro("')' esperado")

            tipoRetornoFuncao()
            bloco()
        else:
            imprimeErro("'(' esperado")

    else:
        imprimeErro("'fn' esperado")

# NomeFuncao → ID | MAIN
def nomeFuncao():
    global token, i

    if token.tipo == "IDENTIFICADOR":
        match("IDENTIFICADOR")
    elif token.lexema == "MAIN":
        match("MAIN")    
    else:
        imprimeErro("IDENTIFICADOR ou MAIN esperado")

# ListaParams → ID : Type ListaParams2 | ε
def listaParams():
    global token, i

    if token.tipo == "IDENTIFICADOR":
        match("IDENTIFICADOR")

        if token.lexema == "COLON":
            match("COLON")
            typeParams()
            listaParams2()
        else:
            imprimeErro("':' esperado")

# ListaParams2 → , ID : Type ListaParams2 | ε
def listaParams2():
    global token, i
    
    if token.lexema == "COMMA":
        match("COMMA")
        if token.tipo == "IDENTIFICADOR":
            match("IDENTIFICADOR")

            if token.lexema == "COLON":
                match("COLON")

                typeParams()
                listaParams2()
            else:
                imprimeErro("':' esperado")
        else:
            imprimeErro("IDENTIFICADOR esperado")


# TipoRetornoFuncao → -> Type | ε
def tipoRetornoFuncao():
    global token, i
    if  token.lexema == "ARROW":
        match("ARROW")

        typeParams()

# Bloco → { Sequencia }
def bloco():
    global token, i

    if token.lexema == "LBRACE":
        match("LBRACE")
        sequencia()
        if token.lexema == "RBRACE":
            match("RBRACE")
        else:
            imprimeErro("'}' esperado")
    else:
        imprimeErro("'{' esperado")

# Sequencia → Declaracao Sequencia | Comando Sequencia | ε
def sequencia():
    global token, i

    if token.lexema == "LET":
        declaracao()
        sequencia()        
    elif token.tipo == "IDENTIFICADOR" or token.lexema == "IF" or token.lexema == "WHILE" or token.lexema == "PRINTLN" or token.lexema == "RETURN":
        comando()
        sequencia()   

# Declaracao → let VarList : Type ;
def declaracao():
    global token, i

    if token.lexema == "LET":
        match("LET")
        varList()

        if token.lexema == "COLON":
            match("COLON")
            typeParams()   

            if token.lexema == "SEMICOLON":
                match("SEMICOLON")
            else:
                imprimeErro("';' esperado")
        else:
            imprimeErro("':' esperado")

    else:
        imprimeErro("'LET' esperado")

# VarList → ID VarList2
def varList():
    global token, i

    if token.tipo == "IDENTIFICADOR":
        match("IDENTIFICADOR")
        varList2()
    else:
        imprimeErro("'IDENTIFICADOR' esperado")

# VarList2 → , ID VarList2 | ε
def varList2():
    global token, i

    if token.lexema == "COMMA":
        match("COMMA")
        if token.tipo == "IDENTIFICADOR":
            match("IDENTIFICADOR")
            varList2()
        else:
            imprimeErro("',' esperado")
            
# Type → int | float | char
def typeParams():
    global token, i

    if token.lexema == "INT":
        match("INT")
    elif token.lexema == "FLOAT":
        match("FLOAT")
    elif token.lexema == "CHAR":
        match("CHAR")
    else:
        imprimeErro("'INT', 'FLOAT' ou 'CHAR' esperado")
   
# Comando → ID AtribuicaoOuChamada |
#           ComandoSe |
#           while Expr Bloco |
#           println( FMT_STRING, ListaArgs ) ; |
#           return Expr ;

def comando():
    global token, i

    if token.tipo == "IDENTIFICADOR":
        match("IDENTIFICADOR")
        atribuicaoOuChamada()
    elif token.lexema == "IF":
        comandoSe()
    elif token.lexema == "WHILE":
        match("WHILE")
        expr()
        bloco()
    elif token.lexema == "PRINTLN":
        match("PRINTLN")

        if token.lexema == "LBRACKET":
            match("LBRACKET")

            if token.tipo == "FMT_STRING":
                match("FMT_STRING")

                if token.lexema == "COMMA":
                    match("COMMA")
                    listaArgs()
                    if token.lexema == "RBRACKET":
                        match("RBRACKET") 
                        if token.lexema == "SEMICOLON":
                            match("SEMICOLON")
                        else:
                            imprimeErro("')' esperado")
                    else:
                        imprimeErro("';' esperado")
                else:
                    imprimeErro("',' esperado")
            else:
                imprimeErro("'FMT_STRING' esperado")
        else:
            imprimeErro("'(' esperado")

    elif token.lexema == "RETURN":
        match("RETURN")
        expr()

        if token.lexema == "SEMICOLON":
            match("SEMICOLON")
        else:
            imprimeErro("';' esperado")
    else:
        imprimeErro("'IDENTIFICADOR', 'IF', 'WHILE', 'PRINTLN' ou 'RETURN' esperado")

# AtribuicaoOuChamada → = Expr ; | ( ListaArgs ) ;
def atribuicaoOuChamada():
    global token, i

    if token.lexema == "ASSIGN":
        match("ASSIGN")
        expr()

        if token.lexema == "SEMICOLON":
            match("SEMICOLON")
        else:
            imprimeErro("';' esperado")
    elif token.lexema == "LBRACKET":
        match("LBRACKET")
        listaArgs()
        if token.lexema == "RBRACKET":
            match("RBRACKET")

            if token.lexema == "SEMICOLON":
                match("SEMICOLON")
            else:
                imprimeErro("';' esperado")
        else:
            imprimeErro("')' esperado")
    else:
        imprimeErro("'=' ou '(' esperado")

# ComandoSe → if Expr Bloco ComandoSenao | Bloco
def comandoSe():
    global token, i

    if token.lexema == "IF":
        match("IF")
        expr()
        bloco()
        comandoSenao()
    elif token.lexema == "LBRACE":
        bloco()
    else:
        imprimeErro("'{' esperado")

# ComandoSenao → else ComandoSe | ε
def comandoSenao():
    global token, i

    if token.lexema == "ELSE":
        match("ELSE")
        comandoSe()

# Expr → Rel ExprOpc
def expr():
    global token, i

    rel()
    exprOpc()

# ExprOpc → OpIgual Rel ExprOpc | ε
def exprOpc():
    global token, i

    if token.lexema == "EQ" or token.lexema == "NE":
        opIgual()
        rel()
        exprOpc()

# OpIgual → == | !=
def opIgual():
    global token, i

    if token.lexema == "EQ":
        match("EQ")
    elif token.lexema == "NE":
        match("NE")

# Rel → Adicao RelOpc
def rel():
    global token, i

    adicao()
    relOpc()

# RelOpc → OpRel Adicao RelOpc | ε
def relOpc():
    global token, i

    if token.lexema == "GT" or token.lexema == "GE" or token.lexema == "LT" or token.lexema == "LE":
        opRel()
        adicao()
        relOpc()

# OpRel → < | <= | > | >=
def opRel():
    global token, i

    if token.lexema == "GT":
        match("GT")
    elif token.lexema == "GE":
        match("GE")
    elif token.lexema == "LT":
        match("LT")
    elif token.lexema == "LE":
        match("LE")

# Adicao → Termo AdicaoOpc
def adicao():
    global token, i

    termo()
    adicaoOpc()

# AdicaoOpc → OpAdicao Termo AdicaoOpc | ε
def adicaoOpc():
    global token, i

    if token.lexema == "PLUS" or token.lexema == "MINUS":
        opAdicao()
        termo()
        adicaoOpc()

# OpAdicao → + | -
def opAdicao():
    global token, i

    if token.lexema == "PLUS":
        match("PLUS")
    elif token.lexema == "MINUS":
        match("MINUS")

# Termo → Fator TermoOpc
def termo():
    global token, i

    fator()
    termoOpc()

# TermoOpc → OpMult Fator TermoOpc | ε
def termoOpc():
    global token, i

    if token.lexema == "MULT" or token.lexema == "DIV":
        opMult()
        fator()
        termoOpc()

# OpMult → * | /
def opMult():
    global token, i

    if token.lexema == "MULT":
        match("MULT")
    elif token.lexema == "DIV":
        match("DIV")

# Fator → ID ChamadaFuncao |
#         INT_CONST |
#         FLOAT_CONST |
#         CHAR_LITERAL |
#         ( Expr )
def fator():
    global token, i

    if token.tipo == "IDENTIFICADOR":
        match("IDENTIFICADOR")
        chamadaFuncao()
    elif token.tipo == "INT_CONST":
        match("INT_CONST")
    elif token.tipo == "FLOAT_CONST":
        match("FLOAT_CONST")
    elif token.tipo == "CHAR_LITERAL":
        match("CHAR_LITERAL")
    elif token.lexema == "LBRACKET":
        match("LBRACKET")
        expr()

        if token.tipo == "RBRACKET":
            match("RBRACKET")
        else:
            imprimeErro("')' esperado")
    else:
        imprimeErro("'IDENTIFICADOR', 'INT_CONST', 'FLOAT_CONST', 'CHAR_LITERAL' ou ')' esperado")

# ChamadaFuncao → ( ListaArgs ) | ε
def chamadaFuncao():
    global token, i
    
    if token.lexema == "LBRACKET":
        match("LBRACKET")
        listaArgs()
        if token.lexema == "RBRACKET":
            match("RBRACKET")
        else:
            imprimeErro("')' esperado")

# ListaArgs → Arg ListaArgs2 | ε
def listaArgs():
    global token, i

    if token.tipo == "IDENTIFICADOR" or token.tipo == "INT_CONST" or token.tipo == "FLOAT_CONST" or token.tipo == "CHAR_LITERAL":
        arg()
        listaArgs2()

# ListaArgs2 → , Arg ListaArgs2 | ε
def listaArgs2():
    global token, i

    if token.lexema == "COMMA":
        match("COMMA")
        arg()
        listaArgs2()


# Arg → ID ChamadaFuncao | INT_CONST | FLOAT_CONST | CHAR_LITERAL
def arg():
    global token, i

    if token.tipo == "IDENTIFICADOR":
        match("IDENTIFICADOR")
        chamadaFuncao()
    elif token.tipo == "INT_CONST":
        match("INT_CONST")
    elif token.tipo == "FLOAT_CONST":
        match("FLOAT_CONST")
    elif token.tipo == "CHAR_LITERAL":
        match("CHAR_LITERAL")
    else:
        imprimeErro("'IDENTIFICADOR', 'INT_CONST', 'FLOAT_CONST' ou 'CHAR_LITERAL' esperado")

#----------------------------------------------#


# Exemplo de uso
nome_arquivo = "tokens.json"
tokens_json = lerTokens(nome_arquivo)
vetor_tokens = atribui(tokens_json)

i = 0
token = vetor_tokens[i]

#print(repr(token))

programa()

"""# Exibe os tokens criados
for token in vetor_tokens:
    print(f"Tipo: {token.tipo}, Token: {token.lexema}, Linha: {token.numero_linha}") """
