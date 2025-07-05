import re

# ===================================================================
# PASSO 1: DEFINIÇÃO DAS ESTRUTURAS DE DADOS (CLASSES)
# ===================================================================
class Aluno:
    def __init__(self, id, nota, preferencias):
        self.id = id
        self.nota = nota
        self.preferencias = preferencias # Lista com IDs de projetos
        self.projeto_alocado = None
        # Usado para rastrear a qual projeto o aluno irá propor em seguida
        self.proxima_proposta_idx = 0

class Projeto:
    def __init__(self, id, v_max, r_min):
        self.id = id
        self.v_max = v_max # Vagas máximas
        self.r_min = r_min # Requisito de nota mínima
        self.alunos_alocados = [] # Lista de objetos Aluno

# ===================================================================
# PASSO 2: FUNÇÃO PARA LER E PROCESSAR OS DADOS DE ENTRADA
# ===================================================================
def parse_input_file(file_path="data/entradaProj2.25TAG.txt"):
    """
    Lê o arquivo de entrada, processa os dados de projetos e alunos,
    e retorna listas de objetos. Lida com preferências inválidas e duplicadas.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada não foi encontrado em '{file_path}'")
        return None, None

    projetos = []
    alunos = []

    # Regex para extrair dados de projetos e alunos
    project_pattern = re.compile(r'\(P(\d+),\s*(\d+),\s*(\d+)\)')
    student_pattern = re.compile(r'\(A(\d+)\):\(P(\d+),\s*P(\d+),\s*P(\d+)\)\s*\((\d)\)')

    # Lê todos os projetos primeiro para validar as preferências dos alunos
    for line in lines:
        match = project_pattern.search(line)
        if match:
            proj_id, vagas, nota_min = map(int, match.groups())
            projetos.append(Projeto(id=proj_id, v_max=vagas, r_min=nota_min))
    
    valid_project_ids = {p.id for p in projetos}

    # Lê os dados dos alunos
    for line in lines:
        match = student_pattern.search(line)
        if match:
            parts = match.groups()
            aluno_id = int(parts[0])
            raw_prefs = list(map(int, parts[1:4]))
            nota = int(parts[4])

            # Limpa as preferências: remove duplicatas e projetos inválidos
            clean_prefs = []
            for pref_id in raw_prefs:
                if pref_id in valid_project_ids and pref_id not in clean_prefs:
                    clean_prefs.append(pref_id)
            
            alunos.append(Aluno(id=aluno_id, nota=nota, preferencias=clean_prefs))

    print(f"Dados carregados com sucesso: {len(projetos)} projetos e {len(alunos)} alunos.")
    return projetos, alunos

# ===================================================================
# PASSO 3: EXECUÇÃO E VERIFICAÇÃO
# ===================================================================
if __name__ == "__main__":
    lista_de_projetos, lista_de_alunos = parse_input_file()

    # Se os dados foram carregados, fazemos uma verificação rápida
    if lista_de_projetos and lista_de_alunos:
        print("\n--- Verificação Rápida de Dados ---")

        # Verificar o primeiro projeto (P1)
        primeiro_projeto = lista_de_projetos[0]
        print(f"Projeto ID: {primeiro_projeto.id}, Vagas: {primeiro_projeto.v_max}, Nota Mínima: {primeiro_projeto.r_min}")

        # Verificar o aluno A2 (que tinha preferência inválida P51)
        aluno_A2 = next((a for a in lista_de_alunos if a.id == 2), None)
        if aluno_A2:
            print(f"Aluno ID: {aluno_A2.id}, Nota: {aluno_A2.nota}, Preferências Válidas e Limpas: {aluno_A2.preferencias}")

        print("-----------------------------------")
        print("\nPróximo passo: Implementar o algoritmo de emparelhamento!")