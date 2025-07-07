import re
import copy
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import plotly.graph_objects as go

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
            clean_prefs = [p_id for p_id in raw_prefs if p_id in valid_project_ids and p_id not in locals().get('clean_prefs', [])]
            alunos.append(Aluno(id=aluno_id, nota=nota, preferencias=clean_prefs))
    print(f"Dados carregados: {len(projetos)} projetos e {len(alunos)} alunos.")
    return projetos, alunos

# ===================================================================
# ALGORITMOS DE EMPARELHAMENTO
# ===================================================================
def encontrar_emparelhamento_estavel_maximo(lista_de_alunos, lista_de_projetos):
    alunos = copy.deepcopy(lista_de_alunos); projetos = copy.deepcopy(lista_de_projetos)
    projetos_map = {p.id: p for p in projetos}
    alunos_livres = [aluno for aluno in alunos if aluno.preferencias]
    while alunos_livres:
        aluno = alunos_livres.pop(0)
        if aluno.proxima_proposta_idx >= len(aluno.preferencias): continue
        id_projeto_alvo = aluno.preferencias[aluno.proxima_proposta_idx]
        projeto = projetos_map[id_projeto_alvo]
        if aluno.nota >= projeto.r_min:
            if len(projeto.alunos_alocados) < projeto.v_max:
                projeto.alunos_alocados.append(aluno); aluno.projeto_alocado = projeto
            else:
                pior_aluno = min(projeto.alunos_alocados, key=lambda x: x.nota)
                if aluno.nota > pior_aluno.nota:
                    projeto.alunos_alocados.remove(pior_aluno); pior_aluno.projeto_alocado = None
                    alunos_livres.append(pior_aluno); projeto.alunos_alocados.append(aluno)
                    aluno.projeto_alocado = projeto
                else: aluno.proxima_proposta_idx += 1; alunos_livres.append(aluno)
        else: aluno.proxima_proposta_idx += 1; alunos_livres.append(aluno)
    return alunos, projetos

def executar_emparelhamento_com_snapshots(lista_de_alunos, lista_de_projetos, num_snapshots=10):
    alunos = copy.deepcopy(lista_de_alunos); projetos = copy.deepcopy(lista_de_projetos)
    alunos_livres = list(alunos)
    projetos_map = {p.id: p for p in projetos}
    propostas_count, snapshots_feitos, passo_propostas = 0, 0, 50
    yield alunos, projetos
    while alunos_livres:
        propostas_count += 1; aluno = alunos_livres.pop(0)
        if aluno.proxima_proposta_idx >= len(aluno.preferencias): continue
        proj_id = aluno.preferencias[aluno.proxima_proposta_idx]
        projeto = projetos_map[proj_id]
        if aluno.nota >= projeto.r_min:
            if len(projeto.alunos_alocados) < projeto.v_max:
                projeto.alunos_alocados.append(aluno); aluno.projeto_alocado = projeto
            else:
                pior_aluno = min(projeto.alunos_alocados, key=lambda x: x.nota)
                if aluno.nota > pior_aluno.nota:
                    projeto.alunos_alocados.remove(pior_aluno); pior_aluno.projeto_alocado = None
                    alunos_livres.append(pior_aluno); projeto.alunos_alocados.append(aluno)
                    aluno.projeto_alocado = projeto
                else: aluno.proxima_proposta_idx += 1; alunos_livres.append(aluno)
        else: aluno.proxima_proposta_idx += 1; alunos_livres.append(aluno)
        if propostas_count % passo_propostas == 0 and snapshots_feitos < num_snapshots:
            snapshots_feitos += 1
            yield copy.deepcopy(alunos), copy.deepcopy(projetos)
    yield alunos, projetos

# ===================================================================
# FUNÇÕES DE VISUALIZAÇÃO E RELATÓRIO
# ===================================================================
def visualizar_layout_radial_matplotlib(lista_de_alunos, lista_de_projetos, titulo):
    B = nx.Graph()
    aluno_nodes = {f"A{a.id}": a for a in lista_de_alunos}; projeto_nodes = {f"P{p.id}": p for p in lista_de_projetos}
    B.add_nodes_from(aluno_nodes.keys(), bipartite=0); B.add_nodes_from(projeto_nodes.keys(), bipartite=1)
    edge_colors, edge_widths = [], []
    for aluno in lista_de_alunos:
        for proj_id in aluno.preferencias:
            B.add_edge(f"A{aluno.id}", f"P{proj_id}")
            if aluno.projeto_alocado and aluno.projeto_alocado.id == proj_id: edge_colors.append("green"); edge_widths.append(1.5)
            else: edge_colors.append("lightgray"); edge_widths.append(0.4)
    pos = dict()
    angulo_proj = np.linspace(0, 2*np.pi, len(projeto_nodes)+1); angulo_aluno = np.linspace(0, 2*np.pi, len(aluno_nodes)+1)
    for i, node in enumerate(projeto_nodes.keys()): pos[node] = (np.cos(angulo_proj[i]), np.sin(angulo_proj[i]))
    for i, node in enumerate(aluno_nodes.keys()): pos[node] = (2*np.cos(angulo_aluno[i]), 2*np.sin(angulo_aluno[i]))
    node_colors = []
    for node in B.nodes():
        if node.startswith('A'):
            if aluno_nodes[node].projeto_alocado: node_colors.append("skyblue")
            else: node_colors.append("#D3D3D3")
        else: node_colors.append("crimson")
    plt.figure(figsize=(20, 20)); nx.draw(B, pos, with_labels=True, node_size=350, font_size=8, font_color='black', node_color=node_colors, edge_color=edge_colors, width=edge_widths)
    plt.title(titulo, size=20); plt.show()

def visualizar_grafo_final_plotly_circular(lista_de_alunos, lista_de_projetos):
    print("\n[PLOT] Gerando visualização circular interativa do resultado final...")
    B = nx.Graph(); aluno_map = {f"A{a.id}": a for a in lista_de_alunos}; projeto_map = {f"P{p.id}": p for p in lista_de_projetos}
    B.add_nodes_from(aluno_map.keys(), bipartite=0); B.add_nodes_from(projeto_map.keys(), bipartite=1)
    pos = dict()
    angulo_proj = np.linspace(0, 2*np.pi, len(projeto_map)+1); angulo_aluno = np.linspace(0, 2*np.pi, len(aluno_map)+1)
    for i, node in enumerate(projeto_map.keys()): pos[node] = (np.cos(angulo_proj[i]), np.sin(angulo_proj[i]))
    for i, node in enumerate(aluno_map.keys()): pos[node] = (2*np.cos(angulo_aluno[i]), 2*np.sin(angulo_aluno[i]))
    arestas_alocadas, arestas_preferencia = [], []
    for aluno in lista_de_alunos:
        for proj_id in aluno.preferencias:
            aresta = (f"A{aluno.id}", f"P{proj_id}")
            if aluno.projeto_alocado and aluno.projeto_alocado.id == proj_id: arestas_alocadas.append(aresta)
            else: arestas_preferencia.append(aresta)
    edge_traces, node_x, node_y, node_text, node_color = [], [], [], [], []
    edge_x_pref, edge_y_pref = [], [];
    for edge in arestas_preferencia: x0, y0 = pos[edge[0]]; x1, y1 = pos[edge[1]]; edge_x_pref.extend([x0, x1, None]); edge_y_pref.extend([y0, y1, None])
    edge_traces.append(go.Scatter(x=edge_x_pref, y=edge_y_pref, line=dict(width=0.5, color='lightgray'), hoverinfo='none', mode='lines'))
    edge_x_alloc, edge_y_alloc = [], []
    for edge in arestas_alocadas: x0, y0 = pos[edge[0]]; x1, y1 = pos[edge[1]]; edge_x_alloc.extend([x0, x1, None]); edge_y_alloc.extend([y0, y1, None])
    edge_traces.append(go.Scatter(x=edge_x_alloc, y=edge_y_alloc, line=dict(width=2, color='green'), hoverinfo='none', mode='lines'))
    for node in B.nodes():
        x, y = pos[node]; node_x.append(x); node_y.append(y)
        if node.startswith('A'):
            aluno = aluno_map[node]; status = f"Alocado em P{aluno.projeto_alocado.id}" if aluno.projeto_alocado else "Não Alocado"
            node_text.append(f"<b>{node}</b><br>Nota: {aluno.nota}<br>Status: {status}"); node_color.append("skyblue" if aluno.projeto_alocado else "lightgray")
        else:
            projeto = projeto_map[node]; node_text.append(f"<b>{node}</b><br>Vagas: {len(projeto.alunos_alocados)}/{projeto.v_max}<br>Nota Mínima: {projeto.r_min}"); node_color.append("crimson")
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=[node.replace('A','').replace('P','') for node in B.nodes()], textfont=dict(size=8), hoverinfo='text', hovertext=node_text, marker=dict(color=node_color, size=15, line_width=1, line_color='black'))
    fig = go.Figure(data=edge_traces + [node_trace], layout=go.Layout(title=dict(text='<br>Resultado Final (Layout Circular Interativo)', font=dict(size=16)), showlegend=False, hovermode='closest', margin=dict(b=20,l=5,r=5,t=40), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    fig.show()

def plotar_matriz_de_alocacao(lista_de_alunos, lista_de_projetos):
    print("\n[PLOT] Gerando a Matriz de Alocações (Heatmap)...")
    proj_ids = [f"P{p.id}" for p in sorted(lista_de_projetos, key=lambda p: p.id)]; aluno_ids = [f"A{a.id}" for a in sorted(lista_de_alunos, key=lambda a: a.id)]
    df_matrix = pd.DataFrame(0, index=proj_ids, columns=aluno_ids)
    for aluno in lista_de_alunos:
        aluno_id_str = f"A{aluno.id}"
        for proj_id in aluno.preferencias:
            proj_id_str = f"P{proj_id}"
            if proj_id_str in df_matrix.index: df_matrix.loc[proj_id_str, aluno_id_str] = 1
        if aluno.projeto_alocado:
            proj_id_str = f"P{aluno.projeto_alocado.id}"
            if proj_id_str in df_matrix.index: df_matrix.loc[proj_id_str, aluno_id_str] = 2
    cmap = matplotlib.colors.ListedColormap(["#FFFFFF", "#134796", "#2E8B57"])
    plt.figure(figsize=(30, 16))
    ax = sns.heatmap(df_matrix, cmap=cmap, cbar=True, linewidths=0.2, linecolor='lightgray', xticklabels=10)
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0.33, 1, 1.67]); cbar.set_ticklabels(['Sem Preferência', 'Preferência', 'Alocado'])
    plt.title("Matriz de Emparelhamentos (Verde = Alocado, Azul = Preferência)", size=20)
    plt.xlabel("Alunos", size=14); plt.ylabel("Projetos", size=14)
    plt.xticks(rotation=90, size=7); plt.yticks(rotation=0, size=9); plt.tight_layout()
    plt.show()

def gerar_relatorio_texto_final(lista_de_alunos):
    dados_alunos = []
    for a in lista_de_alunos:
        ordem_da_escolha = "N/A"
        if a.projeto_alocado:
            try: ordem_da_escolha = a.preferencias.index(a.projeto_alocado.id) + 1
            except ValueError: ordem_da_escolha = "Erro"
        dados_alunos.append({"ID Aluno": f"A{a.id}", "Nota": a.nota, "Projeto Alocado": f"P{a.projeto_alocado.id}" if a.projeto_alocado else "Nenhum", "Ordem da Escolha": ordem_da_escolha})
    df_alunos = pd.DataFrame(dados_alunos)
    print("\n--- MATRIZ FINAL DETALHADA (TERMINAL) ---")
    print(df_alunos.to_string())

# ===================================================================
# EXECUÇÃO PRINCIPAL
# ===================================================================
if __name__ == "__main__":
    projetos_inicial, alunos_inicial = parse_input_file()
    if projetos_inicial and alunos_inicial:
        print("\n" + "="*50); print("INICIANDO PARTE 1: VISUALIZAÇÃO DA EVOLUÇÃO EM 10 PASSOS"); print("="*50)
        print("Feche cada janela do gráfico para ver a próxima iteração.")
        gerador_de_snapshots = executar_emparelhamento_com_snapshots(alunos_inicial, projetos_inicial, num_snapshots=10)
        for i, (alunos_snapshot, projetos_snapshot) in enumerate(gerador_de_snapshots):
            titulo_plot = f"Evolução do Emparelhamento - Snapshot {i}/10"
            if i == 0: titulo_plot = "Estado Inicial (Nenhuma alocação)"
            print(f"\nGerando {titulo_plot}...")
            visualizar_layout_radial_matplotlib(alunos_snapshot, projetos_snapshot, titulo=titulo_plot)

        print("\n" + "="*50); print("INICIANDO PARTE 2: RESULTADO FINAL E RELATÓRIOS VISUAIS"); print("="*50)
        print("Executando o algoritmo para encontrar o emparelhamento estável máximo...")
        alunos_finais, projetos_finais = encontrar_emparelhamento_estavel_maximo(alunos_inicial, projetos_inicial)
        print("Emparelhamento concluído.")
        
        # Gera o grafo interativo principal
        visualizar_grafo_final_plotly_circular(alunos_finais, projetos_finais)

        # Gera a visualização da matriz final
        plotar_matriz_de_alocacao(alunos_finais, projetos_finais)

        # Gera o relatório de texto final
        gerar_relatorio_texto_final(alunos_finais)

        print("\n--- FIM DA EXECUÇÃO ---")