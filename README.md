# Projeto 2 - Teoria e Aplicação de Grafos
## Emparelhamento Estável Máximo: Alocação de Alunos a Projetos

[cite_start]**Instituição:** Universidade de Brasília (UnB) [cite: 1]
[cite_start]**Curso:** Ciência da Computação [cite: 2]
[cite_start]**Disciplina:** Teoria e Aplicação de Grafos, Turma A, 2025/1 [cite: 4]
[cite_start]**Professor:** Díbio [cite: 4]

---

### Integrantes

* **Rebeca de Souza Coutinho:** 222001430
* **Leticia Xavier de Oliveira:** 202065912
* **Alúızio Oliveira Gonçalves Filho:** 202042720

---

### Descrição do Projeto

[cite_start]Este projeto aborda o Problema de Alocação de Estudantes a Projetos (Student-Project Allocation Problem - SPA)[cite: 28]. [cite_start]O objetivo é implementar um algoritmo que encontre um **emparelhamento estável máximo** [cite: 9] [cite_start]entre 200 alunos [cite: 8] [cite_start]e 50 projetos [cite: 5] oferecidos por uma universidade. [cite_start]A seleção deve ser impessoal e competitiva [cite: 9][cite_start], considerando que os alunos possuem diferentes notas e preferências [cite: 7, 11][cite_start], e os projetos possuem diferentes capacidades e requisitos[cite: 6].

---

### Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Bibliotecas Principais:**
    * **Pandas:** Para a manipulação, estruturação e exibição final dos dados em formato de matriz/tabela.
    * **NetworkX:** Para a criação e manipulação da estrutura de grafo bipartido que modela o problema.
    * **Matplotlib:** Para a geração das visualizações estáticas do grafo, como os snapshots da evolução e a matriz de alocação.
    * **Seaborn:** Utilizado para criar uma visualização mais clara e esteticamente agradável da matriz de alocação (heatmap).
    * **Plotly:** Para a geração do grafo interativo final, permitindo zoom, navegação e a exibição de informações detalhadas ao passar o mouse sobre os nós.
    * **NumPy:** Para os cálculos matemáticos necessários para o posicionamento dos nós no layout radial.

---

### Estrutura do Repositório

```
.
├── data/
│   └── entradaProj2.25TAG.txt    # Arquivo de entrada com os dados dos alunos e projetos.
├── main.py                       # Script principal contendo toda a lógica e funcionalidades.
├── requirements.txt              # Lista de dependências Python para fácil instalação.
└── README.md                     # Este arquivo de documentação.
```

---

### Como Executar o Projeto

1.  **Clone o Repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [NOME_DA_PASTA]
    ```
2.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    # No Windows
    py -m venv venv
    venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Para gerar o `requirements.txt`, use `pip freeze > requirements.txt`)*

4.  **Execute o Script Principal:**
    ```bash
    python main.py
    ```
5.  **Fluxo de Execução:**
    * [cite_start]O programa primeiro executará a **PARTE 1**, exibindo sequencialmente os 10+ snapshots da evolução do emparelhamento[cite: 13]. **É preciso fechar cada janela de gráfico para que a próxima apareça.**
    * Após o último snapshot, a **PARTE 2** iniciará. Ela irá gerar o gráfico interativo com Plotly, a matriz de alocação (heatmap) e, por fim, os relatórios de texto detalhados serão impressos no terminal.

---

### Lógica do Algoritmo Proposta

[cite_start]O algoritmo implementado para resolver o problema é uma **Variação do Algoritmo de Gale-Shapley** [cite: 12][cite_start], especificamente adaptado para o cenário de alocação de muitos-para-um, como é o caso de Alunos-para-Projetos[cite: 15, 28]. A lógica se baseia no modelo "student-proposing", onde os alunos propõem e os projetos avaliam as propostas.

As principais características e "variações" em relação ao algoritmo clássico são:

1.  [cite_start]**Emparelhamento Muitos-para-Um:** Diferente do problema de casamento estável (um-para-um), os projetos possuem uma capacidade máxima (`v_max`) [cite: 6] e podem aceitar múltiplos alunos.

2.  **Preferência Baseada em Qualidade (Nota):** Os projetos não possuem uma lista de preferências estática sobre os alunos. [cite_start]A sua preferência é dinâmica e baseada unicamente na **Nota agregada** do aluno[cite: 7]. Um aluno com nota maior é sempre preferido a um aluno com nota menor.

3.  **Lógica de Rejeição e Troca:**
    * [cite_start]Um aluno só pode propor a um projeto se sua nota for igual ou superior ao requisito mínimo (`r_min`) do projeto[cite: 6].
    * Se um projeto recebe uma proposta de um aluno qualificado e tem vagas, o aluno é aceito provisoriamente.
    * Se o projeto está cheio, ele compara a nota do novo proponente com a do "pior" aluno já alocado (aquele com a menor nota). Se o novo aluno for melhor, a troca é feita, e o aluno rejeitado volta para a "fila" de alunos livres para propor ao próximo projeto de sua lista.

4.  **Término por Estabilidade:** O algoritmo é executado em um laço `while` que continua enquanto existirem alunos "livres" que ainda possuam projetos em sua lista para propor. [cite_start]O processo termina quando não é mais possível formar nenhum par estável, garantindo que o resultado final seja um **emparelhamento estável e máximo**[cite: 9, 10].

---
### Funcionalidades Implementadas

O script `main.py` gera as seguintes saídas para cumprir todos os requisitos do projeto:

* [cite_start]**Evolução em Snapshots:** Uma série de 10+ gráficos estáticos usando Matplotlib e um layout radial, mostrando o progresso da alocação[cite: 13].
* **Visualização Interativa Final:** Um grafo interativo com Plotly e layout circular, que permite explorar o resultado final com zoom e informações detalhadas ao passar o mouse sobre os nós.
* [cite_start]**Matriz de Alocação e Preferências:** Um gráfico de heatmap que representa visualmente a matriz de emparelhamentos, mostrando as preferências de todos os alunos e destacando as alocações finais bem-sucedidas[cite: 14].
* **Relatórios em Texto:** Impressão no terminal de duas tabelas detalhadas geradas com Pandas:
    * [cite_start]A matriz final com a ordem de escolha de cada aluno[cite: 14].
    * [cite_start]O índice de preferência dos projetos, calculado como a nota média dos alunos alocados[cite: 14].