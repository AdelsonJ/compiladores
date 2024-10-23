import sys
import string
import json


arquivo = open("entrada.txt", 'r') 
estado = 0 
lexema = [] 
tokens = [] 


class Tipo:
    def __init__(self, tipo, token):
        self.tipo = tipo  
        self.token = token  

    def para_dict(self):
        return {
            self.tipo: self.token
        }

class Token:
    def __init__(self, inicio, fim, numero_linha, tipo_token):
        self.inicio = inicio  
        self.fim = fim  
        self.numero_linha = numero_linha  
        self.tipo_token = tipo_token  

    def para_dict(self):
        return {
            "inicio": self.inicio,
            "fim": self.fim,
            "numero_linha": self.numero_linha,
            "tipo_token": self.tipo_token.para_dict()  
        }


num_linha = 1
for linha in arquivo: 
    ibuf = linha.rstrip('\n')
    i = 0
    #print(linha)

    while i < len(ibuf): 
        char = ibuf[i]

        if estado == 0:
            # Especiais
            if char == '(':
                tipo = Tipo("PONTUACAO", "LBRACKET")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == ')':
                tipo = Tipo("PONTUACAO", "RBRACKET")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == ':':
                tipo = Tipo("PONTUACAO", "COLON")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == ',':
                tipo = Tipo("PONTUACAO", "COMMA")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == '{':
                tipo = Tipo("PONTUACAO", "LBRACE")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == '}':
                tipo = Tipo("PONTUACAO", "RBRACE")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == ';':
                tipo = Tipo("PONTUACAO", "SEMICOLON")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == '+':
                tipo = Tipo("OPERACAO", "PLUS")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == '*':
                tipo = Tipo("OPERACAO", "MULT")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)
            elif char == '/':
                tipo = Tipo("OPERACAO", "DIV")
                token = Token(i, i+1, num_linha, tipo)
                tokens.append(token)

            # Redireciona para os estados
            elif char == '=':
                estado = 1
            elif char == '!':
                estado = 2
            elif char == '>':
                estado = 3
            elif char == '<':
                estado = 4
            elif char == '-':
                estado = 5
            elif char in string.digits:
                inicio = i
                lexema.append(char)
                estado = 6
            elif char in string.ascii_letters:
                inicio = i
                lexema.append(char)
                estado = 9   
            elif char == "'":
                inicio = i
                estado = 10
            elif char == '"':
                inicio = i
                estado = 12
            

            i += 1

        elif estado == 1:
            if char == '=':
                tipo = Tipo("OPERACAO", "EQ")
                token = Token(i-1, i+1, num_linha, tipo)
                tokens.append(token)
            else:
                tipo = Tipo("OPERACAO", "ASSIGN")
                token = Token(i-1, i, num_linha, tipo)
                tokens.append(token)
            i += 1
            estado = 0

        elif estado == 2:
            if char == '=':
                tipo = Tipo("OPERACAO", "NE")
                token = Token(i-1, i+1, num_linha, tipo)
                tokens.append(token)
                i += 1
                estado = 0
            else:
                sys.exit("Erro: Esperado '=' apos '!'")
        
        elif estado == 3:
            if char == '=':
                tipo = Tipo("OPERACAO", "GE")
                token = Token(i-1, i+1, num_linha, tipo)
                tokens.append(token)
            else:
                tipo = Tipo("OPERACAO", "GT")
                token = Token(i-1, i, num_linha, tipo)
                tokens.append(token)
            i += 1
            estado = 0

        elif estado == 4:
            if char == '=':
                tipo = Tipo("OPERACAO", "LE")
                token = Token(i-1, i+1, num_linha, tipo)
                tokens.append(token)
            else:
                tipo = Tipo("OPERACAO", "LT")
                token = Token(i-1, i, num_linha, tipo)
                tokens.append(token)
            i += 1
            estado = 0
        
        elif estado == 5:
            if char == '>':
                tipo = Tipo("OPERACAO", "ARROW")
                token = Token(i-1, i+1, num_linha, tipo)
                tokens.append(token)
            else:
                tipo = Tipo("OPERACAO", "MINUS")
                token = Token(i-1, i, num_linha, tipo)
                tokens.append(token)
            i += 1
            estado = 0
        
        elif estado == 6:
            if char == '.':
                lexema.append(char)
                i += 1
                estado = 7
            elif char in string.digits:
                lexema.append(char)
                i += 1
            else:
                palavra = ''.join(lexema)
                tipo = Tipo("INT_CONST", int(palavra))
                token = Token(inicio, i, num_linha, tipo)
                tokens.append(token)
                estado = 0
                lexema = []

        elif estado == 7:
            if char in string.digits:
                lexema.append(char)
                i += 1
                estado = 8
                
        elif estado == 8:
            if char == '.':
                sys.exit("Erro: Um numero nao deve possuir mais de um '.'")
            elif char in string.digits:
                lexema.append(char)
                i += 1
            else:
                palavra = ''.join(lexema)
                tipo = Tipo("FLOAT_CONST", float(palavra))
                token = Token(inicio, i, num_linha, tipo)
                tokens.append(token)
                estado = 0
                lexema = []

        elif estado == 9:
            if char in string.digits or char in string.ascii_letters or char == '_':
                    lexema.append(char)
                    i += 1
            else:               
                palavra = ''.join(lexema)
                if palavra == "fn":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "FUNCTION")
                elif palavra == "main":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "MAIN")
                elif palavra == "let":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "LET")
                elif palavra == "int":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "INT")
                elif palavra == "float":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "FLOAT")
                elif palavra == "char":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "CHAR")
                elif palavra == "if":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "IF")
                elif palavra == "else":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "ELSE")
                elif palavra == "while":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "WHILE")
                elif palavra == "println":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "PRINTLN")
                elif palavra == "return":
                    tipo = Tipo("PALAVRAS_RESERVADAS", "RETURN")
                else:
                    tipo = Tipo("IDENTIFICADOR", palavra)
                token = Token(inicio, i, num_linha, tipo)
                tokens.append(token)
                estado = 0
                lexema = []  
                
        
        elif estado == 10:
            lexema.append(char)
            print(i)
            i += 1
            estado = 11

        elif estado == 11:
            if char == "'":
                tipo = Tipo("CARACTER_LITERAL", ''.join(lexema))
                token = Token(inicio, i, num_linha, tipo)
                tokens.append(token)
                estado = 0
            else:
                sys.exit("Erro: Esperado apenas um elemento dentro das aspas simples")

        
        elif estado == 12:
            estado = 13

        elif estado == 13:
            if char == "'":
                token = [char, "FMT_STRING", num_linha]
                tokens.append(token)
                estado = 0
        
with open('tokens.json', 'w') as arquivo_json:
    json.dump([token.para_dict() for token in tokens], arquivo_json, indent=4)