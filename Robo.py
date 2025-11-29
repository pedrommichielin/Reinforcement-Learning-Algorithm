import pygame
import random
from collections import deque

LINHAS = 6
COLUNAS = 6
QTD_PRESENTES = random.randint(3, 9)
QTD_ZUMBIS = 3
QTD_PEDRAS = 4

def gerar_grid():
    grid = [['E' for _ in range(COLUNAS)] for _ in range(LINHAS)]
    posicoes = [(i, j) for i in range(LINHAS) for j in range(COLUNAS)]
    random.shuffle(posicoes)

    for _ in range(QTD_PRESENTES):
        i, j = posicoes.pop()
        grid[i][j] = 'P'

    for _ in range(QTD_ZUMBIS):
        i, j = posicoes.pop()
        grid[i][j] = 'Z'

    i, j = posicoes.pop()
    grid[i][j] = 'S'

    i, j = posicoes.pop()
    grid[i][j] = 'R'

    for _ in range(QTD_PEDRAS):
        i, j = posicoes.pop()
        grid[i][j] = 'PD'

    return grid
 
grid = gerar_grid()

porta_pos = None
for i in range(LINHAS):
    for j in range(COLUNAS):
        if grid[i][j] == 'R':
            robo_l, robo_c = i, j
        if grid[i][j] == 'S':
            porta_pos = (i, j)

grid[robo_l][robo_c] = 'E'
posicao_inicial_robo = (robo_l, robo_c)


direcoes = [
    ("CIMA", -1, 0),
    ("BAIXO", 1, 0),
    ("ESQUERDA", 0, -1),
    ("DIREITA", 0, 1)
]


visitadas = set()
conhecidas = set()  
bloqueios_conhecidos = set() 
presentes_coletados = set()
pontos = 0
qtd_presentes_encontrados = 0

ultimos_passos = deque(maxlen=10)
posicao_anterior = None
mortes_por_zumbi = 0
movimentos_sem_progresso = 0

def bfs_caminho(inicio, objetivos, bloqueios):
    fila = deque([inicio])
    veio_de = {inicio: None}
    
    while fila:
        atual = fila.popleft()
        
        if atual in objetivos:
            caminho = []
            while atual is not None:
                caminho.append(atual)
                atual = veio_de[atual]
            return caminho[::-1]
        
        for _, dl, dc in direcoes:
            nl, nc = atual[0] + dl, atual[1] + dc
            
            if not (0 <= nl < LINHAS and 0 <= nc < COLUNAS):
                continue
            
            if (nl, nc) in bloqueios:
                continue
            
            if (nl, nc) not in veio_de:
                veio_de[(nl, nc)] = atual
                fila.append((nl, nc))
    
    return None


def dfs_mapear_alcancaveis(pos_inicial, bloqueios):
    alcancaveis = set()
    pilha = [pos_inicial]
    explorados = {pos_inicial}
    
    while pilha:
        l, c = pilha.pop()
        
        if (l, c) not in bloqueios:
            alcancaveis.add((l, c))
        
        for _, dl, dc in direcoes:
            nl, nc = l + dl, c + dc
            
            if not (0 <= nl < LINHAS and 0 <= nc < COLUNAS):
                continue
            
            if (nl, nc) in explorados:
                continue
            
            explorados.add((nl, nc))
            
            if (nl, nc) in bloqueios:
                continue
            
            pilha.append((nl, nc))
    
    return alcancaveis


def mover_robo():
    global robo_l, robo_c, pontos, qtd_presentes_encontrados, posicao_anterior, movimentos_sem_progresso

    visitadas.add((robo_l, robo_c))
    conhecidas.add((robo_l, robo_c))
    

    alcancaveis = dfs_mapear_alcancaveis((robo_l, robo_c), bloqueios_conhecidos)
    
    nao_visitadas = alcancaveis - visitadas
    tudo_explorado = len(nao_visitadas) == 0
    
    if tudo_explorado:
        print(f"Tudo foi explorado!")

    melhor_pontuacao = -999999
    melhor_movimento = None

    for nome, dl, dc in direcoes:
        nl = robo_l + dl
        nc = robo_c + dc
        
        if not (0 <= nl < LINHAS and 0 <= nc < COLUNAS):
            continue

        conteudo = grid[nl][nc]
        pontuacao_temp = 0
        
        if (nl, nc) not in visitadas:
            pontuacao_temp += 2000 
        
        if (nl, nc) in conhecidas and conteudo == 'S':
            if tudo_explorado:
                pontuacao_temp += 50000  
                print(f"Indo para porta")
            else:
                pontuacao_temp -= 1000
        if (nl, nc) in conhecidas and conteudo == 'P':
            pontuacao_temp += 1000

        if (nl, nc) in bloqueios_conhecidos:
            pontuacao_temp -= 99999
        
        # Backtracking
        if (nl, nc) in visitadas:
            vizinhos_novos = 0
            for _, vdl, vdc in direcoes:
                vnl, vnc = nl + vdl, nc + vdc
                if (0 <= vnl < LINHAS and 0 <= vnc < COLUNAS and 
                    (vnl, vnc) not in visitadas and 
                    (vnl, vnc) not in bloqueios_conhecidos):
                    vizinhos_novos += 1
            
            if vizinhos_novos > 0:
                pontuacao_temp += vizinhos_novos * 300
            else:
                pontuacao_temp -= 500

        if posicao_anterior == (nl, nc):
            pontuacao_temp -= 600

        repeticoes = ultimos_passos.count((nl, nc))
        pontuacao_temp -= repeticoes * 400

        if pontuacao_temp > melhor_pontuacao:
            melhor_pontuacao = pontuacao_temp
            melhor_movimento = (nl, nc, conteudo)

    if melhor_movimento is None:
        print("Sem movimento possível!")
        return True

    nl, nc, conteudo = melhor_movimento

    tamanho_visitadas_antes = len(visitadas)
    
    ultimos_passos.append((nl, nc))
    posicao_anterior = (robo_l, robo_c)

    if conteudo == 'Z':
        pontos -= 20
        print(f"Zumbi! -20 pontos (Total: {pontos})")
        bloqueios_conhecidos.add((nl, nc))
        conhecidas.add((nl, nc))
        aciona_morte_robo()
        return False

    if conteudo == 'PD':
        pontos -= 5
        print(f"Pedra! -5 pontos (Total: {pontos})")
        bloqueios_conhecidos.add((nl, nc))
        conhecidas.add((nl, nc))
        return False

    if conteudo == 'P':
        pontos += 10
        qtd_presentes_encontrados += 1
        print(f"Presente coletado! +10 pontos (Total: {pontos})")
        presentes_coletados.add((nl, nc))
        grid[nl][nc] = 'E'

    if conteudo == 'S':
        conhecidas.add((nl, nc))
        if tudo_explorado:
            pontos += 50
            print(f"Porta alcançada! Explorou tudo! +50 pontos (Total: {pontos})")
            return True
        else:
            pontos -= 10
            print(f"Porta fechada! Ainda faltam {len(nao_visitadas)} lugares a serem visitados. -10 pontos (Total: {pontos})")
            return False
        
    if movimentos_sem_progresso >= 10:
        print("Loop detectado! Usando BFS para avançar até célula não visitada.")
        caminho = bfs_caminho((robo_l, robo_c), nao_visitadas, bloqueios_conhecidos)
        
        if caminho and len(caminho) > 1:
            proximo = caminho[1]
            robo_l, robo_c = proximo
            movimentos_sem_progresso = 0
            visitadas.add(proximo)
            return False

    robo_l, robo_c = nl, nc
    
    if len(visitadas) == tamanho_visitadas_antes:
        movimentos_sem_progresso += 1
    else:
        movimentos_sem_progresso = 0
    
    return False


def aciona_morte_robo():
    global robo_l, robo_c, mortes_por_zumbi, movimentos_sem_progresso
    mortes_por_zumbi += 1
    movimentos_sem_progresso = 0
    print(f"Robô reiniciado na posição inicial. Total de mortes: {mortes_por_zumbi}")
    robo_l, robo_c = posicao_inicial_robo
    ultimos_passos.clear()

TAM = 80

pygame.init()
tela = pygame.display.set_mode((COLUNAS * TAM, LINHAS * TAM))
pygame.display.set_caption("Robô Explorador - Aprendizado por Descoberta")


def criar_quadrado(cor):
    superficie = pygame.Surface((TAM, TAM))
    superficie.fill(cor)
    return superficie


def carregar_imagem(nome):
    try:
        img = pygame.image.load(nome).convert_alpha()
        return pygame.transform.scale(img, (TAM, TAM))
    except:
        return criar_quadrado((200, 200, 200))


imagens = {
    'R': carregar_imagem("C:/Users/pedro/Documents/SetimoSemestre/IA/images/robo.png"),
    'S': carregar_imagem("C:/Users/pedro/Documents/SetimoSemestre/IA/images/door.png"),
    'P': carregar_imagem("C:/Users/pedro/Documents/SetimoSemestre/IA/images/presente.png"),
    'Z': carregar_imagem("C:/Users/pedro/Documents/SetimoSemestre/IA/images/zombies.png"),
    'PD': carregar_imagem("C:/Users/pedro/Documents/SetimoSemestre/IA/images/pedra.png"),
    'E': criar_quadrado((60, 60, 60))
}


rodando = True
clock = pygame.time.Clock()

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    jogo_acabou = mover_robo()
    if jogo_acabou:
        print(f"\n{'='*40}")
        print(f"🏁 FIM DE JOGO")
        print(f"Pontuação final: {pontos}")
        print(f"Presentes coletados: {qtd_presentes_encontrados}/{QTD_PRESENTES}")
        print(f"Mortes por zumbi: {mortes_por_zumbi}")
        print(f"Células conhecidas: {len(conhecidas)}")
        print(f"Células visitadas: {len(visitadas)}")
        print(f"Bloqueios descobertos: {len(bloqueios_conhecidos)}")
        print(f"{'='*40}\n")
        rodando = False

    for i in range(LINHAS):
        for j in range(COLUNAS):
            tela.blit(imagens[grid[i][j]], (j * TAM, i * TAM))
            pygame.draw.rect(tela, (0, 0, 0), (j * TAM, i * TAM, TAM, TAM), 2)
            if (i, j) not in visitadas:
                sombra = pygame.Surface((TAM, TAM))
                sombra.set_alpha(100)
                sombra.fill((255, 0, 0))
                tela.blit(sombra, (j * TAM, i * TAM))

    tela.blit(imagens['R'], (robo_c * TAM, robo_l * TAM))

    pygame.display.update()
    clock.tick(5)

pygame.quit()