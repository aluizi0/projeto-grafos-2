import re
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import copy

# ===================================================================
# ESTRUTURAS DE DADOS (CLASSES)
# ===================================================================
class Aluno:
    def __init__(self, id, nota, preferencias):
        self.id = id; self.nota = nota; self.preferencias = preferencias
        self.projeto_alocado = None; self.proxima_proposta_idx = 0

class Projeto:
    def __init__(self, id, v_max, r_min):
        self.id = id; self.v_max = v_max; self.r_min = r_min
        self.alunos_alocados = []

# ===================================================================
# PARSER DO ARQUIVO DE ENTRADA
# ===================================================================
def parse_input_file(file_path="data/entradaProj2.25TAG.txt"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f: lines = f.readlines()
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{file_path}' não encontrado."); return None, None
    projetos, alunos = [], []
    project_pattern = re.compile(r'\(P(\d+),\s*(\d+),\s*(\d+)\)')
    student_pattern = re.compile(r'\(A(\d+)\):\(P(\d+),\s*P(\d+),\s*P(\d+)\)\s*\((\d)\)')
    for line in lines:
        match = project_pattern.search(line)
        if match: projetos.append(Projeto(*map(int, match.groups())))
    valid_project_ids = {p.id for p in projetos}
    for line in lines:
        match = student_pattern.search(line)
        if match:
            parts = match.groups()
            aluno_id, raw_prefs, nota = int(parts[0]), list(map(int, parts[1:4])), int(parts[4])
            clean_prefs = []
            for pref_id in raw_prefs:
                if pref_id in valid_project_ids and pref_id not in clean_prefs: clean_prefs.append(pref_id)
            alunos.append(Aluno(id=aluno_id, nota=nota, preferencias=clean_prefs))
    print(f"Dados carregados: {len(projetos)} projetos e {len(alunos)} alunos.")
    return projetos, alunos

# ===================================================================
# ALGORITMO DE EMPARELHAMENTO (GERADOR DE SNAPSHOTS)
# ===================================================================
def executar_emparelhamento_com_snapshots(lista_de_alunos, lista_de_projetos, num_snapshots=10):
    alunos = copy.deepcopy(lista_de_alunos)
    projetos = copy.deepcopy(lista_de_projetos)
    alunos_livres = list(alunos)
    projetos_map = {p.id: p for p in projetos}
    propostas_count, snapshots_feitos, passo_propostas = 0, 0, 50

    yield alunos, projetos # Snapshot 0: Estado Inicial
    while alunos_livres:
        propostas_count += 1; aluno = alunos_livres.pop(0)
        if aluno.proxima_proposta_idx >= len(aluno.preferencias): continue
        proj_id = aluno.preferencias[aluno.proxima_proposta_idx]; projeto = projetos_map[proj_id]
        aluno.proxima_proposta_idx += 1
        if aluno.nota >= projeto.r_min:
            if len(projeto.alunos_alocados) < projeto.v_max:
                projeto.alunos_alocados.append(aluno); aluno.projeto_alocado = projeto.id
            else:
                pior_aluno = min(projeto.alunos_alocados, key=lambda x: x.nota)
                if aluno.nota > pior_aluno.nota:
                    projeto.alunos_alocados.remove(pior_aluno); pior_aluno.projeto_alocado = None
                    alunos_livres.append(pior_aluno); projeto.alunos_alocados.append(aluno)
                    aluno.projeto_alocado = projeto.id
                else: alunos_livres.append(aluno)
        else: alunos_livres.append(aluno)
        if propostas_count % passo_propostas == 0 and snapshots_feitos < num_snapshots:
            snapshots_feitos += 1
            yield copy.deepcopy(alunos), copy.deepcopy(projetos)
    
    if snapshots_feitos >= num_snapshots:
         yield alunos, projetos

# ===================================================================
# FUNÇÕES DE VISUALIZAÇÃO E RELATÓRIO
# ===================================================================
def visualizar_layout_radial(lista_de_alunos, lista_de_projetos, titulo):
    B = nx.Graph()
    aluno_nodes = {f"A{a.id}": a for a in lista_de_alunos}
    projeto_nodes = {f"P{p.id}": p for p in lista_de_projetos}
    B.add_nodes_from(aluno_nodes.keys(), bipartite=0)
    B.add_nodes_from(projeto_nodes.keys(), bipartite=1)
    edge_colors, edge_widths = [], []
    for aluno in lista_de_alunos:
        for proj_id in aluno.preferencias:
            B.add_edge(f"A{aluno.id}", f"P{proj_id}")
            if aluno.projeto_alocado == proj_id:
                edge_colors.append("green"); edge_widths.append(1.5)
            else:
                edge_colors.append("lightgray"); edge_widths.append(0.4)
    pos = dict()
    angulo_proj = np.linspace(0, 2 * np.pi, len(projeto_nodes) + 1)
    for i, node in enumerate(projeto_nodes.keys()):
        pos[node] = (np.cos(angulo_proj[i]), np.sin(angulo_proj[i]))
    angulo_aluno = np.linspace(0, 2 * np.pi, len(aluno_nodes) + 1)
    for i, node in enumerate(aluno_nodes.keys()):
        pos[node] = (2 * np.cos(angulo_aluno[i]), 2 * np.sin(angulo_aluno[i]))
    node_colors = []
    for node in B.nodes():
        if node.startswith('A'):
            if aluno_nodes[node].projeto_alocado:
                node_colors.append("skyblue")
            else:
                node_colors.append("#D3D3D3")
        else:
            node_colors.append("crimson")
    plt.figure(figsize=(20, 20))
    nx.draw(B, pos, with_labels=True, node_size=350, font_size=8, font_color='black',
            node_color=node_colors, edge_color=edge_colors, width=edge_widths)
    plt.title(titulo, size=20)
    plt.show()

def gerar_relatorio_texto_final(lista_de_alunos, lista_de_projetos):
    print("\n--- MATRIZ FINAL DE EMPARELHAMENTOS (ORDEM DA ESCOLHA) ---")
    dados_alunos = []
    for aluno in lista_de_alunos:
        ordem_pref = "N/A"
        if aluno.projeto_alocado:
            try: ordem_pref = aluno.preferencias.index(aluno.projeto_alocado) + 1
            except ValueError: ordem_pref = "Erro"
        dados_alunos.append({"ID Aluno": f"A{aluno.id}", "Nota": aluno.nota, "Projeto Alocado": f"P{aluno.projeto_alocado}" if aluno.projeto_alocado else "Nenhum", "Ordem da Escolha": ordem_pref})
    pd.set_option('display.max_rows', None)
    print(pd.DataFrame(dados_alunos))
    print("\n--- ÍNDICE DE PREFERÊNCIA POR PROJETO (NOTA MÉDIA) ---")
    dados_projetos = []
    for projeto in lista_de_projetos:
        if projeto.alunos_alocados:
            nota_media = sum(a.nota for a in projeto.alunos_alocados) / len(projeto.alunos_alocados)
            dados_projetos.append({"ID Projeto": f"P{projeto.id}", "Vagas": f"{len(projeto.alunos_alocados)}/{projeto.v_max}", "Nota Média Alocados": f"{nota_media:.2f}"})
    df_projetos_ordenado = pd.DataFrame(dados_projetos).sort_values(by="Nota Média Alocados", ascending=False)
    print(df_projetos_ordenado.to_string())

# ===================================================================
# EXECUÇÃO PRINCIPAL
# ===================================================================
if __name__ == "__main__":
    lista_de_projetos_inicial, lista_de_alunos_inicial = parse_input_file()
    if lista_de_projetos_inicial and lista_de_alunos_inicial:
        gerador_de_snapshots = executar_emparelhamento_com_snapshots(lista_de_alunos_inicial, lista_de_projetos_inicial, num_snapshots=10)
        print("\n--- INICIANDO VISUALIZAÇÃO DA EVOLUÇÃO ---")
        print("Feche cada janela do gráfico para ver a próxima iteração.")
        alunos_estado_final, projetos_estado_final = None, None
        
        for i, (alunos_snapshot, projetos_snapshot) in enumerate(gerador_de_snapshots):
            titulo_plot = f"Evolução do Emparelhamento - Passo {i}" if i > 0 else "Estado Inicial"
            print(f"\nGerando {titulo_plot}...")
            visualizar_layout_radial(alunos_snapshot, projetos_snapshot, titulo=titulo_plot)
            
            # --- LINHA CORRIGIDA ---
            # Atualiza AMBAS as variáveis com o estado mais recente do snapshot
            alunos_estado_final, projetos_estado_final = alunos_snapshot, projetos_snapshot

        total_alunos_alocados = sum(1 for a in alunos_estado_final if a.projeto_alocado)
        print("\n--- Resumo da Alocação Final ---")
        print(f"Total de alunos alocados: {total_alunos_alocados}")
        print(f"Total de alunos não alocados: {len(alunos_estado_final) - total_alunos_alocados}")
        
        # Agora esta chamada funcionará, pois projetos_estado_final não será mais None
        gerar_relatorio_texto_final(alunos_estado_final, projetos_estado_final)
        
        print("\n--- FIM DA EXECUÇÃO ---")