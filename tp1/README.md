# Compilador Lexical e Sintático 📜💻

Este projeto implementa as fases de análise léxica e sintática de um compilador utilizando Python. Ele processa um arquivo de entrada e gera um arquivo tokens.json contendo os tokens identificados.

## 🎮 Funcionalidades

- **Análise Léxica:** Identifica e categoriza os tokens no código-fonte;
- **Análise Sintática:** Verifica a estrutura gramatical do código de entrada;
- Geração de um arquivo tokens.json com os tokens identificados.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** C
- **Lógica de compiladores:** Implementação dos analisadores léxico e sintático.

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Python instalado (versão mínima recomendada: 3.7)

2. Clone este repositório:
   ```bash
   git clone https://github.com/AdelsonJ/compiladores
   
3. Execute o compilador passando a versão do Python, o arquivo principal e o arquivo de entrada:
   ```bash
   python compilador.py arquivo_de_entrada.extensao

**Nota:** Substitua arquivo_de_entrada.extensao pelo nome do arquivo que deseja compilar.

## 📦 Estrutura do Projeto
- **compilador.py:** Arquivo principal que coordena a execução dos analisadores léxico e sintático;
- **lexico.py:** Realiza a análise léxica do código de entrada;
- **sintatico.py:** Executa a análise sintática com base nos tokens gerados;
- **tokens.json:** Arquivo gerado contendo os tokens identificados e suas respectivas categorias.

## 💡 Como Funciona
1. **Entrada:** Um arquivo contendo o código-fonte.
2. **Análise Léxica:**
    - Identificação dos tokens (palavras-chave, identificadores, operadores, etc.);
    - Geração do arquivo tokens.json.
3. **Análise Sintática:**
    - Verificação das regras gramaticais do código com base nos tokens gerados;
    - Durante o processo, o terminal exibe os tokens reconhecidos, detalhando suas categorias e valores.

## 🧑‍💻 Autor
Projeto desenvolvido por AdelsonJ.
