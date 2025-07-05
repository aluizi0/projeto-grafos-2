# Projeto 2 - Teoria e Aplicação de Grafos (TAG)
## Emparelhamento Estável Máximo Aluno-Projeto

**Universidade de Brasília (UnB) - Departamento de Ciência da Computação**
[cite_start]**Disciplina:** Teoria e Aplicação de Grafos, Turma A, 2025/1 [cite: 1, 2, 4]
[cite_start]**Professor:** Díbio [cite: 4]

---

### Integrantes

* **Nome do Integrante 1:** Matrícula 1
* **Nome do Integrante 2:** Matrícula 2
* **(Opcional) Nome do Integrante 3:** Matrícula 3

---

### Descrição do Projeto

Este projeto consiste na elaboração e implementação de uma solução para o **Problema de Alocação de Alunos a Projetos (Student-Project Allocation Problem)**. [cite_start]O objetivo é criar um emparelhamento estável e máximo entre um conjunto de 200 alunos e 50 projetos[cite: 5, 8].

As principais características e restrições do problema são:
* [cite_start]**Alunos:** 200 alunos se candidataram[cite: 8]. [cite_start]Cada aluno possui uma nota agregada (3: suficiente, 4: muito boa, 5: excelente) [cite: 7] [cite_start]e indica no máximo três projetos de sua preferência, em ordem[cite: 11].
* [cite_start]**Projetos:** 50 projetos são oferecidos[cite: 5]. [cite_start]Cada projeto estabelece uma quantidade mínima e máxima de vagas e exige uma nota mínima como requisito para a aceitação de um aluno[cite: 6].
* [cite_start]**Objetivo:** Implementar um algoritmo, baseado em variações do algoritmo de Gale-Shapley, que encontre um emparelhamento estável máximo[cite: 9, 10]. [cite_start]A solução deve ser apresentada em um notebook com visualizações do grafo bipartido e dos resultados[cite: 13].

---

### Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Bibliotecas Principais:**
    * **Pandas:** Para manipulação e estruturação eficiente dos dados de entrada.
    * **NetworkX:** Para a criação, manipulação e análise do grafo bipartido (Alunos-Projetos).
    * **Matplotlib:** Para a visualização gráfica do grafo e das etapas do emparelhamento.

---

### Como Executar o Projeto

O projeto finalizado está contido e documentado no notebook Jupyter/Colab. Para executar:

1.  **Pré-requisitos:** Ter um ambiente Python 3 instalado.
2.  **Clone o Repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_AQUI]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```
3.  **Instale as Dependências:**
    Recomenda-se criar um ambiente virtual.
    ```bash
    # Crie e ative um ambiente virtual (opcional, mas recomendado)
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate

    # Instale as bibliotecas
    pip install -r requirements.txt
    ```
    *(Nota: Certifiquem-se de criar um arquivo `requirements.txt` com `pip freeze > requirements.txt`)*

4.  **Abra e Execute o Notebook:**
    * A entrega principal é o arquivo `notebook_final.ipynb`.
    * Abra-o no Jupyter Notebook, Jupyter Lab ou Google Colab.
    * [cite_start]**Importante:** Faça o upload do arquivo de dados `entradaProj2.25TAG.txt` [cite: 16] para o ambiente do Colab/Jupyter antes de executar as células.
    * Execute as células em ordem para ver todo o processo, desde a leitura dos dados até a visualização dos resultados finais.

---

### Estrutura do Repositório

```
.
├── data/
│   └── entradaProj2.25TAG.txt    # Arquivo de entrada com os dados dos alunos e projetos
├── notebook_final.ipynb          # Notebook com a solução completa, explicações e resultados
├── src/                          # Módulos Python com a lógica principal (opcional)
│   ├── algorithm.py
│   └── ...
├── README.md                     # Este arquivo
└── requirements.txt              # Lista de dependências Python
```

---

### Lógica do Algoritmo Proposto

Conforme solicitado, a solução implementada é uma variação do **algoritmo de Gale-Shapley**, adaptada para o problema de alocação de estudantes a projetos (muitos-para-um). [cite_start]A lógica foi baseada nos conceitos apresentados no artigo de referência *Two algorithms for the student-project allocation problem* por Abraham, Irving & Manlove (2007)[cite: 15, 28].

Nossa implementação utiliza a **versão em que os alunos propõem aos projetos (Student-Proposing)**, com as seguintes adaptações e regras:

1.  **Propostas e Qualificação:**
    * Um aluno "livre" propõe ao próximo projeto em sua lista de preferências.
    * [cite_start]A proposta só é considerada válida se a nota do aluno (`N_aluno`) for maior ou igual ao requisito mínimo do projeto (`r_projeto`)[cite: 6, 7]. Caso contrário, o aluno é imediatamente rejeitado e passa para sua próxima opção.

2.  **Aceitação do Projeto:**
    * [cite_start]Se um projeto `P` recebe uma proposta de um aluno qualificado `A` e ainda tem vagas (número de alocados < `v_max`), `P` aceita `A` provisoriamente[cite: 6].
    * Se o projeto `P` já está com sua capacidade máxima preenchida, ele compara o aluno proponente `A` com o aluno de **menor nota** (`A_pior`) que já está em sua lista de alocados.
    * Se a nota de `A` for **superior** à nota de `A_pior`, `P` aceita `A`, e o aluno `A_pior` é dispensado, tornando-se "livre" novamente para propor a outros projetos.
    * Se a nota de `A` for inferior ou igual à de `A_pior`, `P` rejeita `A`.

3.  **Listas de Preferências Incompletas:**
    * [cite_start]O algoritmo lida com o fato de que os alunos podem ter no máximo 3 preferências[cite: 11]. Um aluno que é rejeitado por todos os projetos de sua lista fica permanentemente sem alocação.

4.  **Término:**
    * O algoritmo termina quando não há mais alunos "livres" que ainda possuam projetos em suas listas para os quais propor. O resultado é um emparelhamento estável.

---

### Resultados

[cite_start]Os resultados detalhados, incluindo a **visualização do grafo bipartido**, a **evolução do emparelhamento em 10 iterações**, o **índice de preferência por projeto** e a **matriz final de alocações**, estão todos apresentados e explicados no notebook `notebook_final.ipynb`[cite: 13, 14].