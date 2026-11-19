import json
import math
import os
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import tkinter as tk
import unicodedata
import urllib.parse
import webbrowser
from tkinter import font as tkfont

LARGURA, ALTURA = 1100, 690
LATERAL = 230
BARRA_PLAYER = 88
M = 8
X0 = LATERAL + 50

FUNDO = "#000000"
PAINEL = "#121212"
CARD = "#181818"
CARD_HOVER = "#282828"
LINHA = "#2A2A2A"
VERDE = "#1ED68A"
VERMELHO = "#F2545B"
TEXTO = "#FFFFFF"
CINZA = "#A7A7A7"

PASTA_APP = os.path.dirname(os.path.abspath(__file__))
PASTA_MUSICAS = os.path.join(PASTA_APP, "musicas")
EXTENSOES = (".mp3", ".m4a", ".wav", ".aac")
PASTA_CAPAS = os.path.join(PASTA_MUSICAS, "capas_oficiais")
TAMANHOS_CAPA = (36, 60, 74, 76, 148, 150)

MUSICAS = [
    (1, "Só Pra Você Lembrar", "Filipe Ret", "Rap", "#F59E0B", "#7C2D12"),
    (2, "Última Vez", "Alee", "Trap", "#38BDF8", "#1E3A8A"),
    (3, "Celebridade", "Orochi", "Trap", "#FACC15", "#A16207"),
    (4, "Espaço Nave", "Brandão", "Trap", "#A78BFA", "#312E81"),
    (5, "For the Night", "Pop Smoke", "Drill", "#FF4FD8", "#9D174D"),
    (6, "No Idea", "Don Toliver", "R&B", "#22E39A", "#065F46"),
    (7, "Hiperfoco", "Veigh", "Trap", "#F43F5E", "#4C0519"),
    (8, "Swimming Pools", "Kendrick Lamar", "Rap", "#60A5FA", "#0C4A6E"),
]

CORES_EXTRAS = [("#60A5FA", "#1E3A8A"), ("#34D399", "#064E3B"), ("#F472B6", "#831843"),
                ("#FBBF24", "#78350F"), ("#C084FC", "#4C1D95"), ("#FB7185", "#881337")]

CAPAS_FIXAS = CAPAS_FIXAS = {
    "hiperfoco": (
        "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"
    ),
    "ultimavez": (
        "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"
    ),
    "celebridade": (
        "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"
        "M5SHJcX7Pzzve2yl2kmWAAAAAElFTkSuQmCC"
    ),
    "espaconave": (
        "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"
    ),
    "forthenight": (
        "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"
    ),
}


def misturar(cor1, cor2, t):
    a = [int(cor1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(cor2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def tempo(segundos):
    if segundos is None:
        return "--:--"
    segundos = int(segundos)
    return f"{segundos // 60}:{segundos % 60:02d}"


def simplificar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", sem_acento.lower())


def abrir_no_youtube(musica):
    busca = urllib.parse.quote_plus(f"{musica[1]} {musica[2]}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={busca}")


def abrir_pasta(caminho):
    if sys.platform == "darwin":
        subprocess.Popen(["open", caminho])
    elif sys.platform.startswith("win"):
        os.startfile(caminho)
    else:
        subprocess.Popen(["xdg-open", caminho])


def baixar(url):
    if shutil.which("curl"):
        resultado = subprocess.run(["curl", "-sfL", "--max-time", "10", url], capture_output=True)
        if resultado.returncode == 0:
            return resultado.stdout
    import urllib.request
    with urllib.request.urlopen(url, timeout=10) as resposta:
        return resposta.read()


class Capas:
    def __init__(self, musicas):
        self.pronto = False
        self.novas = 0
        self.imagens = {}
        os.makedirs(PASTA_CAPAS, exist_ok=True)
        threading.Thread(target=self.baixar_todas, args=(musicas,), daemon=True).start()

    def arquivo(self, musica, tamanho):
        return os.path.join(PASTA_CAPAS, f"{simplificar(musica[1] + musica[2])}_{tamanho}.png")

    def baixar_todas(self, musicas):
        erros = []
        for musica in musicas:
            if simplificar(musica[1]) in CAPAS_FIXAS:
                continue
            if all(os.path.exists(self.arquivo(musica, t)) for t in TAMANHOS_CAPA):
                continue
            try:
                self.baixar_capa(musica)
                self.novas += 1
            except Exception as erro:
                erros.append(f"{musica[1]}: {erro}")
        if erros:
            with open(os.path.join(PASTA_CAPAS, "erros.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(erros))
        self.pronto = True

    def baixar_capa(self, musica):
        arte = self.achar_capa(musica)
        for tamanho in TAMANHOS_CAPA:
            conteudo = baixar(re.sub(r"\d+x\d+bb\.\w+$", f"{tamanho}x{tamanho}bb.png", arte))
            if not conteudo.startswith(b"\x89PNG"):
                raise ValueError("a capa não veio em PNG")
            with open(self.arquivo(musica, tamanho), "wb") as f:
                f.write(conteudo)

    def achar_capa(self, musica):
        titulo, artista = simplificar(musica[1]), simplificar(musica[2])
        melhor, melhor_nota = None, 0
        for pais in ("br", "us"):
            busca = urllib.parse.urlencode({"term": f"{musica[1]} {musica[2]}", "media": "music",
                                            "entity": "song", "limit": 25, "country": pais})
            for item in json.loads(baixar("https://itunes.apple.com/search?" + busca)).get("results", []):
                nome = simplificar(item.get("trackName", ""))
                quem = simplificar(item.get("artistName", ""))
                nota = 0
                if artista and (artista in quem or quem in artista):
                    nota += 2
                if titulo == nome:
                    nota += 2
                elif titulo in nome:
                    nota += 1
                if nota > melhor_nota:
                    melhor, melhor_nota = item, nota
            if melhor_nota >= 3:
                break
        if melhor is None or (artista and melhor_nota < 3):
            raise ValueError("não achei essa música com esse artista na loja")
        return melhor["artworkUrl100"]

    def imagem(self, musica, tamanho):
        if simplificar(musica[1]) in CAPAS_FIXAS:
            return self.capa_fixa(musica, tamanho)
        caminho = self.arquivo(musica, tamanho)
        if caminho not in self.imagens:
            if not os.path.exists(caminho):
                return None
            try:
                self.imagens[caminho] = tk.PhotoImage(file=caminho)
            except tk.TclError:
                return None
        return self.imagens[caminho]

    def capa_fixa(self, musica, tamanho):
        chave = (simplificar(musica[1]), tamanho)
        if chave not in self.imagens:
            zoom, divide = min(((z, d) for z in range(1, 10) for d in range(1, 30)),
                               key=lambda zd: abs(100 * zd[0] / zd[1] - tamanho))
            try:
                foto = tk.PhotoImage(data=CAPAS_FIXAS[chave[0]]).zoom(zoom).subsample(divide)
            except tk.TclError:
                foto = None
            self.imagens[chave] = foto
        return self.imagens[chave]


class Biblioteca:
    def __init__(self, banco):
        self.banco = banco
        self.duracoes = {}
        os.makedirs(PASTA_MUSICAS, exist_ok=True)
        self.banco.execute("DROP TABLE IF EXISTS musicas")
        self.banco.execute("""
            CREATE TABLE musicas (
                id INTEGER PRIMARY KEY, titulo TEXT, artista TEXT, genero TEXT,
                cor1 TEXT, cor2 TEXT, arquivo TEXT)""")
        self.banco.execute("""
            CREATE TABLE IF NOT EXISTS curtidas (musica_id INTEGER PRIMARY KEY)""")
        self.banco.executemany("INSERT INTO musicas VALUES (?, ?, ?, ?, ?, ?, ?)", self.montar_catalogo())
        self.banco.commit()

    def montar_catalogo(self):
        arquivos = sorted(f for f in os.listdir(PASTA_MUSICAS) if f.lower().endswith(EXTENSOES))
        usados = set()
        catalogo = []
        for musica in MUSICAS:
            achado = next((f for f in arquivos if f not in usados
                           and simplificar(musica[1]) in simplificar(f)), None)
            if achado:
                usados.add(achado)
            catalogo.append(musica + (achado,))
        proximo_id = 100
        for arquivo in arquivos:
            if arquivo in usados:
                continue
            nome = os.path.splitext(arquivo)[0]
            artista, titulo = nome.split(" - ", 1) if " - " in nome else ("", nome)
            cor1, cor2 = CORES_EXTRAS[proximo_id % len(CORES_EXTRAS)]
            catalogo.append((proximo_id, titulo.strip(), artista.strip(), "Minhas", cor1, cor2, arquivo))
            proximo_id += 1
        return catalogo

    def listar(self):
        return self.banco.execute("SELECT * FROM musicas ORDER BY id").fetchall()

    def buscar(self, musica_id):
        return self.banco.execute("SELECT * FROM musicas WHERE id = ?", (musica_id,)).fetchone()

    def caminho(self, musica):
        return os.path.join(PASTA_MUSICAS, musica[6]) if musica and musica[6] else None

    def com_arquivo(self):
        return sum(1 for m in self.listar() if m[6])

    def duracao(self, musica):
        if not musica or not musica[6]:
            return None
        if musica[0] not in self.duracoes:
            self.duracoes[musica[0]] = None
            if sys.platform == "darwin":
                try:
                    saida = subprocess.run(["afinfo", self.caminho(musica)], capture_output=True,
                                           text=True, timeout=5).stdout
                    achou = re.search(r"estimated duration: ([\d.]+)", saida)
                    if achou:
                        self.duracoes[musica[0]] = float(achou.group(1))
                except (OSError, subprocess.SubprocessError):
                    pass
        return self.duracoes[musica[0]]

    def curtida(self, musica_id):
        return self.banco.execute(
            "SELECT 1 FROM curtidas WHERE musica_id = ?", (musica_id,)).fetchone() is not None

    def curtir(self, musica_id):
        with self.banco:
            if self.curtida(musica_id):
                self.banco.execute("DELETE FROM curtidas WHERE musica_id = ?", (musica_id,))
            else:
                self.banco.execute("INSERT INTO curtidas VALUES (?)", (musica_id,))


class Playlists:
    def __init__(self, banco):
        self.banco = banco
        self.banco.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)""")
        self.banco.execute("""
            CREATE TABLE IF NOT EXISTS playlist_musicas (
                playlist_id INTEGER, musica_id INTEGER, ordem INTEGER,
                UNIQUE(playlist_id, musica_id))""")
        if not self.listar():
            rap = self.criar("Rap BR")
            for musica_id in (1, 2, 3, 4):
                self.adicionar(rap, musica_id)
            gringa = self.criar("Gringas")
            for musica_id in (5, 6, 8):
                self.adicionar(gringa, musica_id)

    def listar(self):
        return self.banco.execute("SELECT * FROM playlists ORDER BY id").fetchall()

    def buscar(self, playlist_id):
        return self.banco.execute("SELECT * FROM playlists WHERE id = ?", (playlist_id,)).fetchone()

    def criar(self, nome):
        with self.banco:
            cursor = self.banco.execute("INSERT INTO playlists (nome) VALUES (?)", (nome,))
        return cursor.lastrowid

    def apagar(self, playlist_id):
        with self.banco:
            self.banco.execute("DELETE FROM playlist_musicas WHERE playlist_id = ?", (playlist_id,))
            self.banco.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))

    def musicas(self, playlist_id):
        return [linha[0] for linha in self.banco.execute(
            """SELECT pm.musica_id FROM playlist_musicas pm
               JOIN musicas m ON m.id = pm.musica_id
               WHERE pm.playlist_id = ? ORDER BY pm.ordem""", (playlist_id,))]

    def adicionar(self, playlist_id, musica_id):
        try:
            with self.banco:
                self.banco.execute("INSERT INTO playlist_musicas VALUES (?, ?, ?)",
                                   (playlist_id, musica_id, time.time()))
            return True
        except sqlite3.IntegrityError:
            return False

    def remover(self, playlist_id, musica_id):
        with self.banco:
            self.banco.execute("DELETE FROM playlist_musicas WHERE playlist_id = ? AND musica_id = ?",
                               (playlist_id, musica_id))


class Player:
    def __init__(self, biblioteca):
        self.biblioteca = biblioteca
        self.estado = "parado"
        self.musica = None
        self.fila = []
        self.posicao_fila = 0
        self.inicio = 0
        self.pausado_em = 0
        self.processo = None

    def tocar(self, fila, posicao=0):
        musica = self.biblioteca.buscar(fila[posicao])
        if not musica[6]:
            return False
        self._calar()
        self.fila = list(fila)
        self.posicao_fila = posicao
        self.musica = musica
        self.pausado_em = 0
        self.inicio = time.time()
        self.processo = self._abrir_som(self.biblioteca.caminho(musica))
        self.estado = "tocando"
        return True

    def pausar(self):
        if self.estado != "tocando":
            return False
        self.pausado_em = self.segundos()
        self._sinal(signal.SIGSTOP if hasattr(signal, "SIGSTOP") else None)
        self.estado = "pausado"
        return True

    def continuar(self):
        if self.estado != "pausado":
            return False
        self._sinal(signal.SIGCONT if hasattr(signal, "SIGCONT") else None)
        self.inicio = time.time() - self.pausado_em
        self.estado = "tocando"
        return True

    def alternar(self):
        if self.estado == "tocando":
            self.pausar()
        elif self.estado == "pausado":
            self.continuar()

    def proxima(self, passo=1):
        if not self.fila:
            return
        for i in range(1, len(self.fila) + 1):
            posicao = (self.posicao_fila + passo * i) % len(self.fila)
            if self.tocar(self.fila, posicao):
                return
        self.parar()

    def parar(self):
        self._calar()
        self.estado = "parado"

    def segundos(self):
        if self.estado == "tocando":
            return time.time() - self.inicio
        return self.pausado_em

    def duracao(self):
        return self.biblioteca.duracao(self.musica)

    def acabou(self):
        return (self.estado == "tocando" and self.processo is not None
                and self.processo.poll() is not None)

    def _abrir_som(self, caminho):
        if sys.platform == "darwin":
            comando = ["afplay", caminho]
        elif shutil.which("ffplay"):
            comando = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", caminho]
        else:
            comando = ["mpg123", "-q", caminho]
        try:
            return subprocess.Popen(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            return None

    def _sinal(self, sinal):
        if self.processo is not None and sinal is not None and self.processo.poll() is None:
            os.kill(self.processo.pid, sinal)

    def _calar(self):
        if self.processo is not None:
            if self.estado == "pausado":
                self._sinal(getattr(signal, "SIGCONT", None))
            self.processo.terminate()
            self.processo = None


class Tela(tk.Canvas):
    def __init__(self, app):
        super().__init__(app.janela, width=LARGURA, height=ALTURA, bg=FUNDO, highlightthickness=0)
        self.app = app
        self.contador_tags = 0

    def retangulo(self, x1, y1, x2, y2, raio=12, **opcoes):
        pontos = [x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio, x2, y2 - raio, x2, y2,
                  x2 - raio, y2, x1 + raio, y2, x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1]
        opcoes.setdefault("outline", "")
        return self.create_polygon(pontos, smooth=True, **opcoes)

    def degrade(self, x1, y1, x2, y2, cor1, cor2, tags=(), passos=40):
        altura = (y2 - y1) / passos
        for i in range(passos):
            cor = misturar(cor1, cor2, i / (passos - 1))
            self.create_rectangle(x1, y1 + i * altura, x2, y1 + (i + 1) * altura + 1,
                                  fill=cor, outline="", tags=tags)

    def cortar(self, texto, fonte, largura):
        if fonte.measure(texto) <= largura:
            return texto
        while texto and fonte.measure(texto + "…") > largura:
            texto = texto[:-1]
        return texto.rstrip() + "…"

    def capa(self, x1, y1, x2, y2, musica, tags=()):
        foto = self.app.capas.imagem(musica, round(x2 - x1))
        if foto is not None:
            self.create_image(x1, y1, image=foto, anchor="nw", tags=tags)
            return
        self.degrade(x1, y1, x2, y2, musica[4], musica[5], tags, passos=24)
        self.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=musica[1][:1].upper(), fill=TEXTO,
                         font=self.app.fonte(max(9, int((x2 - x1) * 0.42)), "bold"), tags=tags)

    def logo(self, x, y):
        self.create_oval(x - 16, y - 16, x + 16, y + 16, fill=VERDE, outline="")
        for i, altura in enumerate((6, 12, 9, 4)):
            bx = x - 9 + i * 5.5
            self.create_rectangle(bx, y - altura, bx + 3, y + altura, fill=FUNDO, outline="")

    def clicavel(self, tag, ao_clicar, ao_entrar=None, ao_sair=None):
        def entrar(evento):
            self.config(cursor="hand2")
            if ao_entrar:
                ao_entrar()

        def sair(evento):
            self.config(cursor="")
            if ao_sair:
                ao_sair()

        self.tag_bind(tag, "<Enter>", entrar)
        self.tag_bind(tag, "<Leave>", sair)
        self.tag_bind(tag, "<Button-1>", lambda evento: ao_clicar())

    def nova_tag(self):
        self.contador_tags += 1
        return f"botao{self.contador_tags}"

    def botao(self, x, y, texto, ao_clicar, cor=VERDE, cor_texto=FUNDO, largura=None, borda=None):
        tag = self.nova_tag()
        largura = largura or (self.app.fonte(12, "bold").measure(texto) + 44)
        fundo = self.retangulo(x, y, x + largura, y + 40, raio=20, fill=cor, tags=tag,
                               outline=borda or "", width=1)
        self.create_text(x + largura / 2, y + 20, text=texto, fill=cor_texto,
                         font=self.app.fonte(12, "bold"), tags=tag)
        self.clicavel(tag, ao_clicar,
                      lambda: self.itemconfig(fundo, fill=misturar(cor, "#FFFFFF", 0.15)),
                      lambda: self.itemconfig(fundo, fill=cor))
        return x + largura

    def botao_play(self, cx, cy, raio, ao_clicar, tocando=False, tags=(), tag=None, cor=VERDE):
        tag = tag or self.nova_tag()
        todas = (tag,) + tuple(tags)
        self.create_oval(cx - raio, cy - raio, cx + raio, cy + raio, fill=cor, outline="", tags=todas)
        if tocando:
            l = raio * 0.16
            for dx in (-raio * 0.26, raio * 0.26):
                self.create_rectangle(cx + dx - l, cy - raio * 0.38, cx + dx + l, cy + raio * 0.38,
                                      fill=FUNDO, outline="", tags=todas)
        else:
            r = raio * 0.4
            self.create_polygon(cx - r * 0.6, cy - r, cx - r * 0.6, cy + r, cx + r * 1.05, cy,
                                fill=FUNDO, tags=todas)
        self.clicavel(tag, ao_clicar)

    def fundo_principal(self):
        self.retangulo(LATERAL + M, M, LARGURA - M, ALTURA - BARRA_PLAYER, raio=10, fill=PAINEL)

    def cabecalho(self, cor, altura):
        x1, y1, x2 = LATERAL + M, M, LARGURA - M
        self.create_rectangle(LATERAL, 0, LARGURA, M, fill=FUNDO, outline="")
        self.degrade(x1, y1, x2, y1 + altura, cor, PAINEL)
        r = 10
        for x in (x1, x2 - r):
            self.create_rectangle(x, y1, x + r, y1 + r, fill=FUNDO, outline="")
        self.create_oval(x1, y1, x1 + 2 * r, y1 + 2 * r, fill=cor, outline="")
        self.create_oval(x2 - 2 * r, y1, x2, y1 + 2 * r, fill=cor, outline="")

    def menu_lateral(self):
        self.create_rectangle(0, 0, LATERAL + M, ALTURA, fill=FUNDO, outline="")
        self.retangulo(M, M, LATERAL, 168, raio=10, fill=PAINEL)
        self.logo(36, 44)
        self.create_text(60, 44, text="streamify", anchor="w", fill=TEXTO,
                         font=self.app.fonte(20, "bold"))
        itens = [("⌂   Início", TelaInicio), ("♥   Curtidas", TelaCurtidas),
                 ("≡   Playlists", TelaPlaylists)]
        y = 88
        for texto, classe in itens:
            tag = self.nova_tag()
            ativo = type(self) is classe
            item = self.create_text(26, y, text=texto, anchor="w", fill=TEXTO if ativo else CINZA,
                                    font=self.app.fonte(13, "bold"), tags=tag)
            self.clicavel(tag, lambda c=classe: self.app.mostrar(c),
                          lambda i=item: self.itemconfig(i, fill=TEXTO),
                          lambda i=item, a=ativo: self.itemconfig(i, fill=TEXTO if a else CINZA))
            y += 30
        self.retangulo(M, 176, LATERAL, ALTURA - BARRA_PLAYER, raio=10, fill=PAINEL)
        self.create_text(26, 204, text="Sua biblioteca", anchor="w", fill=CINZA,
                         font=self.app.fonte(12, "bold"))
        y = 238
        for playlist in self.app.playlists.listar()[:6]:
            tag = self.nova_tag()
            ativo = isinstance(self, TelaPlaylist) and self.playlist_id == playlist[0]
            fundo = self.retangulo(M + 8, y - 22, LATERAL - 8, y + 22, raio=6,
                                   fill=CARD_HOVER if ativo else PAINEL, tags=tag)
            ids = self.app.playlists.musicas(playlist[0])
            if ids:
                self.capa(26, y - 18, 62, y + 18, self.app.biblioteca.buscar(ids[0]), tags=(tag,))
            else:
                self.retangulo(26, y - 18, 62, y + 18, raio=4, fill=CARD_HOVER, tags=tag)
                self.create_text(44, y, text="♪", fill=CINZA, font=self.app.fonte(14), tags=tag)
            nome = self.cortar(playlist[1], self.app.fonte(12, "bold"), LATERAL - 90)
            self.create_text(74, y - 8, text=nome, anchor="w",
                             fill=VERDE if ativo else TEXTO, font=self.app.fonte(12, "bold"), tags=tag)
            self.create_text(74, y + 10, text=f"Playlist · {len(ids)} músicas", anchor="w",
                             fill=CINZA, font=self.app.fonte(10), tags=tag)
            self.clicavel(tag, lambda p=playlist[0]: self.app.abrir_playlist(p),
                          lambda f=fundo: self.itemconfig(f, fill=CARD_HOVER),
                          lambda f=fundo, a=ativo: self.itemconfig(f, fill=CARD_HOVER if a else PAINEL))
            y += 52

    def barra_player(self):
        self.delete("player")
        p = self.app.player
        y0 = ALTURA - BARRA_PLAYER
        self.create_rectangle(0, y0, LARGURA, ALTURA, fill=FUNDO, outline="", tags="player")
        meio = y0 + BARRA_PLAYER / 2
        if p.musica is None:
            self.create_text(LARGURA / 2, meio, text="Escolhe uma música pra começar",
                             fill=CINZA, font=self.app.fonte(12), tags="player")
            return
        m = p.musica
        self.capa(16, meio - 30, 76, meio + 30, m, tags="player")
        fonte_titulo = self.app.fonte(13, "bold")
        self.create_text(90, meio - 10, text=self.cortar(m[1], fonte_titulo, 190), anchor="w",
                         fill=TEXTO, font=fonte_titulo, tags="player")
        self.create_text(90, meio + 12, text=m[2], anchor="w", fill=CINZA,
                         font=self.app.fonte(11), tags="player")
        tag = "player_curtir"
        curtida = self.app.biblioteca.curtida(m[0])
        self.create_text(300, meio, text="♥" if curtida else "♡",
                         fill=VERDE if curtida else CINZA, font=self.app.fonte(18),
                         tags=("player", tag))
        self.clicavel(tag, lambda: self.app.curtir(m[0]))
        cx = LARGURA / 2
        for lado in (-1, 1):
            tag = f"player_pular{lado}"
            x, yc = cx + lado * 50, meio - 12
            self.create_rectangle(x - 12, yc - 12, x + 12, yc + 12, fill=FUNDO, outline="",
                                  tags=("player", tag))
            self.create_polygon(x - 6 * lado, yc - 7, x - 6 * lado, yc + 7, x + 5 * lado, yc,
                                fill=CINZA, tags=("player", tag))
            self.create_rectangle(x + 5 * lado, yc - 7, x + 7 * lado, yc + 7, fill=CINZA,
                                  outline="", tags=("player", tag))
            self.clicavel(tag, lambda s=lado: self.app.pular(s))
        self.botao_play(cx, meio - 12, 17, self.app.alternar, p.estado == "tocando",
                        tags=("player",), tag="player_play", cor=TEXTO)
        x1, x2, yb = cx - 230, cx + 230, meio + 22
        duracao = p.duracao()
        fracao = min(1, p.segundos() / duracao) if duracao else 0
        self.create_text(x1 - 10, yb, text=tempo(p.segundos()), anchor="e", fill=CINZA,
                         font=self.app.fonte(10), tags="player")
        self.create_text(x2 + 10, yb, text=tempo(duracao), anchor="w", fill=CINZA,
                         font=self.app.fonte(10), tags="player")
        self.retangulo(x1, yb - 2, x2, yb + 2, raio=2, fill="#4D4D4D", tags="player")
        if fracao > 0.01:
            fim = x1 + (x2 - x1) * fracao
            self.retangulo(x1, yb - 2, fim, yb + 2, raio=2, fill=TEXTO, tags="player")
            self.create_oval(fim - 5, yb - 5, fim + 5, yb + 5, fill=TEXTO, outline="", tags="player")
        if p.estado == "tocando":
            for i in range(5):
                h = 4 + 12 * abs(math.sin(time.time() * (5 + i * 1.7) + i))
                x = LARGURA - 70 + i * 7
                self.create_rectangle(x, meio + 8 - h, x + 4, meio + 8, fill=VERDE,
                                      outline="", tags="player")
        elif not m[6]:
            self.create_text(LARGURA - 24, meio, text="↗ YouTube", anchor="e", fill=CINZA,
                             font=self.app.fonte(10), tags="player")

    def lista_de_musicas(self, ids, y, ao_remover=None):
        x0, x_fim = X0 - 10, LARGURA - 40
        self.create_text(x0 + 14, y, text="#", anchor="w", fill=CINZA, font=self.app.fonte(10))
        self.create_text(x0 + 50, y, text="Título", anchor="w", fill=CINZA, font=self.app.fonte(10))
        self.create_text(x0 + 380, y, text="Artista", anchor="w", fill=CINZA, font=self.app.fonte(10))
        self.create_text(x_fim - 70, y, text="Duração", anchor="e", fill=CINZA, font=self.app.fonte(10))
        self.create_line(x0, y + 16, x_fim, y + 16, fill=LINHA)
        y += 28
        p = self.app.player
        for numero, musica_id in enumerate(ids):
            m = self.app.biblioteca.buscar(musica_id)
            tag = self.nova_tag()
            fundo = self.retangulo(x0, y, x_fim, y + 52, raio=6, fill=PAINEL, tags=tag)
            atual = p.musica is not None and p.musica[0] == musica_id and p.estado != "parado"
            self.create_text(x0 + 18, y + 26, text="♪" if atual else str(numero + 1),
                             fill=VERDE if atual else CINZA, font=self.app.fonte(12), tags=tag)
            self.capa(x0 + 42, y + 8, x0 + 78, y + 44, m, tags=tag)
            self.create_text(x0 + 90, y + 17, text=m[1], anchor="w", fill=VERDE if atual else TEXTO,
                             font=self.app.fonte(12, "bold"), tags=tag)
            self.create_text(x0 + 90, y + 35, text=m[3] if m[6] else f"{m[3]}  ·  ↗ YouTube",
                             anchor="w", fill=CINZA, font=self.app.fonte(10), tags=tag)
            self.create_text(x0 + 380, y + 26, text=m[2], anchor="w", fill=CINZA,
                             font=self.app.fonte(11), tags=tag)
            self.create_text(x_fim - 70, y + 26, text=tempo(self.app.biblioteca.duracao(m)),
                             anchor="e", fill=CINZA, font=self.app.fonte(11), tags=tag)
            self.clicavel(tag, lambda i=numero: self.app.tocar(ids, i),
                          lambda f=fundo: self.itemconfig(f, fill=CARD_HOVER),
                          lambda f=fundo: self.itemconfig(f, fill=PAINEL))
            if ao_remover:
                tag_x = self.nova_tag()
                self.create_text(x_fim - 24, y + 26, text="✕", fill=CINZA,
                                 font=self.app.fonte(12), tags=tag_x)
                self.clicavel(tag_x, lambda mid=musica_id: ao_remover(mid))
            y += 54
        if not ids:
            self.create_text(x0 + 14, y + 20, text="Nada aqui ainda. Vai no Início e adiciona umas músicas!",
                             anchor="w", fill=CINZA, font=self.app.fonte(12))

    def desenhar(self):
        pass


class TelaInicio(Tela):
    rolagem = 0

    def __init__(self, app):
        super().__init__(app)
        self.bind("<MouseWheel>", self.rolar)
        self.bind("<Button-4>", lambda e: self.rolar(e, 1))
        self.bind("<Button-5>", lambda e: self.rolar(e, -1))

    def rolar(self, evento, direcao=None):
        direcao = direcao or (1 if evento.delta > 0 else -1)
        linhas = math.ceil(len(self.app.biblioteca.listar()) / 4)
        maximo = max(0, linhas * 236 - 440)
        TelaInicio.rolagem = max(0, min(maximo, TelaInicio.rolagem - direcao * 40))
        self.desenhar()

    def desenhar(self):
        self.delete("all")
        self.fundo_principal()
        largura, altura, espaco = 176, 226, 22
        musicas = self.app.biblioteca.listar()
        todas = [m[0] for m in musicas]
        p = self.app.player
        fonte_titulo = self.app.fonte(13, "bold")
        for indice, musica in enumerate(musicas):
            coluna, linha = indice % 4, indice // 4
            x1 = X0 + coluna * (largura + espaco)
            y1 = 150 + linha * (altura + 10) - TelaInicio.rolagem
            if y1 > ALTURA or y1 + altura < 0:
                continue
            tag = self.nova_tag()
            fundo = self.retangulo(x1, y1, x1 + largura, y1 + altura, raio=10, fill=CARD, tags=tag)
            self.capa(x1 + 14, y1 + 14, x1 + largura - 14, y1 + largura - 14, musica, tags=tag)
            self.create_text(x1 + 14, y1 + largura + 8,
                             text=self.cortar(musica[1], fonte_titulo, largura - 54), anchor="w",
                             fill=TEXTO, font=fonte_titulo, tags=tag)
            artista = musica[2] or "Artista ?"
            self.create_text(x1 + 14, y1 + largura + 30,
                             text=self.cortar(artista, self.app.fonte(11), largura - 54),
                             anchor="w", fill=CINZA, font=self.app.fonte(11), tags=tag)
            self.clicavel(tag, lambda i=indice: self.app.tocar(todas, i),
                          lambda f=fundo: self.itemconfig(f, fill=CARD_HOVER),
                          lambda f=fundo: self.itemconfig(f, fill=CARD))
            tocando = p.musica is not None and p.musica[0] == musica[0] and p.estado == "tocando"
            self.botao_play(x1 + largura - 38, y1 + largura - 38, 21,
                            (self.app.alternar if tocando else lambda i=indice: self.app.tocar(todas, i)),
                            tocando, cor=VERDE if musica[6] else VERMELHO)
            tag_mais = self.nova_tag()
            cx, cy = x1 + largura - 26, y1 + largura + 19
            circulo = self.create_oval(cx - 12, cy - 12, cx + 12, cy + 12, outline=CINZA, width=1.5,
                                       fill=CARD, tags=tag_mais)
            self.create_text(cx, cy - 1, text="+", fill=CINZA, font=self.app.fonte(14, "bold"),
                             tags=tag_mais)
            self.clicavel(tag_mais, lambda mid=musica[0], x=cx, y=cy + 12:
                          self.app.menu_adicionar(mid, x, y),
                          lambda c=circulo: self.itemconfig(c, outline=TEXTO),
                          lambda c=circulo: self.itemconfig(c, outline=CINZA))

        self.cabecalho("#1B4B3A", 136)
        hora = time.localtime().tm_hour
        saudacao = "Bom dia" if hora < 12 else "Boa tarde" if hora < 18 else "Boa noite"
        self.create_text(X0, 52, text=saudacao, anchor="w", fill=TEXTO,
                         font=self.app.fonte(28, "bold"))
        tem = self.app.biblioteca.com_arquivo()
        total = len(musicas)
        self.create_text(X0, 90, text=f"{total} músicas  ·  {tem} tocam aqui  ·  as vermelhas abrem no YouTube",
                         anchor="w", fill=CINZA, font=self.app.fonte(11))
        self.botao(LARGURA - 240, 34, "Abrir pasta de músicas", lambda: abrir_pasta(PASTA_MUSICAS),
                   cor="#1F1F1F", cor_texto=TEXTO, borda="#535353")
        self.menu_lateral()
        self.barra_player()


class TelaCurtidas(Tela):
    def desenhar(self):
        self.delete("all")
        self.fundo_principal()
        self.cabecalho("#1D5A4A", 240)
        self.menu_lateral()
        self.degrade(X0, 40, X0 + 160, 200, VERDE, "#0B4F3A", passos=30)
        self.create_text(X0 + 80, 120, text="♥", fill=TEXTO, font=self.app.fonte(60))
        ids = [m[0] for m in self.app.biblioteca.listar() if self.app.biblioteca.curtida(m[0])]
        self.create_text(X0 + 184, 84, text="Playlist", anchor="w", fill=TEXTO, font=self.app.fonte(11))
        self.create_text(X0 + 182, 126, text="Músicas curtidas", anchor="w", fill=TEXTO,
                         font=self.app.fonte(36, "bold"))
        self.create_text(X0 + 184, 170, text=f"{len(ids)} músicas  ·  clica no ♡ do player pra curtir",
                         anchor="w", fill=CINZA, font=self.app.fonte(11))
        self.lista_de_musicas(ids, 236)
        self.barra_player()


class TelaPlaylists(Tela):
    def desenhar(self):
        self.delete("all")
        self.fundo_principal()
        self.cabecalho("#24304F", 200)
        self.menu_lateral()
        self.create_text(X0, 56, text="Suas playlists", anchor="w", fill=TEXTO,
                         font=self.app.fonte(28, "bold"))
        self.campo = tk.Entry(self.app.janela, font=self.app.fonte(13), bg="#242424", fg=TEXTO,
                              insertbackground=TEXTO, relief="flat", width=26,
                              highlightthickness=1, highlightbackground="#3E3E3E", highlightcolor=VERDE)
        self.create_window(X0, 108, window=self.campo, anchor="w", height=40)
        self.campo.bind("<Return>", lambda evento: self.criar())
        self.botao(X0 + 330, 88, "+ Criar playlist", self.criar)
        if getattr(self, "erro", ""):
            self.create_text(X0, 144, text=self.erro, anchor="w", fill=VERMELHO, font=self.app.fonte(11))

        largura, espaco = 176, 22
        for indice, playlist in enumerate(self.app.playlists.listar()):
            coluna, linha = indice % 4, indice // 4
            x1 = X0 + coluna * (largura + espaco)
            y1 = 168 + linha * 236
            ids = self.app.playlists.musicas(playlist[0])
            tag = self.nova_tag()
            fundo = self.retangulo(x1, y1, x1 + largura, y1 + 226, raio=10, fill=CARD, tags=tag)
            self.capa_playlist(x1 + 14, y1 + 14, x1 + largura - 14, y1 + largura - 14, ids, tag)
            self.create_text(x1 + 14, y1 + largura + 8, text=playlist[1], anchor="w", fill=TEXTO,
                             font=self.app.fonte(13, "bold"), tags=tag)
            self.create_text(x1 + 14, y1 + largura + 30, text=f"{len(ids)} músicas", anchor="w",
                             fill=CINZA, font=self.app.fonte(11), tags=tag)
            self.clicavel(tag, lambda p=playlist[0]: self.app.abrir_playlist(p),
                          lambda f=fundo: self.itemconfig(f, fill=CARD_HOVER),
                          lambda f=fundo: self.itemconfig(f, fill=CARD))
        self.barra_player()

    def capa_playlist(self, x1, y1, x2, y2, ids, tag):
        if not ids:
            self.degrade(x1, y1, x2, y2, "#333333", "#1E1E1E", (tag,))
            self.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="♪", fill=CINZA,
                             font=self.app.fonte(40), tags=tag)
            return
        meio_x, meio_y = (x1 + x2) / 2, (y1 + y2) / 2
        quadros = [(x1, y1, meio_x, meio_y), (meio_x, y1, x2, meio_y),
                   (x1, meio_y, meio_x, y2), (meio_x, meio_y, x2, y2)]
        for i, (a, b, c, d) in enumerate(quadros):
            m = self.app.biblioteca.buscar(ids[i % len(ids)])
            self.capa(a, b, c, d, m, tags=(tag,))

    def criar(self):
        nome = self.campo.get().strip()
        if not nome:
            self.erro = "Dá um nome pra playlist primeiro!"
            self.desenhar()
            return
        self.erro = ""
        self.app.playlists.criar(nome[:28])
        self.desenhar()


class TelaPlaylist(Tela):
    def __init__(self, app, playlist_id):
        super().__init__(app)
        self.playlist_id = playlist_id

    def desenhar(self):
        self.delete("all")
        playlist = self.app.playlists.buscar(self.playlist_id)
        ids = self.app.playlists.musicas(self.playlist_id)
        primeira = self.app.biblioteca.buscar(ids[0]) if ids else None
        cor = misturar(primeira[5], "#121212", 0.35) if primeira else "#333333"
        self.fundo_principal()
        self.cabecalho(cor, 250)
        self.menu_lateral()
        if primeira:
            self.capa(X0, 40, X0 + 150, 190, primeira)
        else:
            self.retangulo(X0, 40, X0 + 150, 190, raio=6, fill="#282828")
            self.create_text(X0 + 75, 115, text="♪", fill=CINZA, font=self.app.fonte(50))
        self.create_text(X0 + 175, 66, text="Playlist", anchor="w", fill=TEXTO, font=self.app.fonte(11))
        self.create_text(X0 + 172, 106, text=playlist[1], anchor="w", fill=TEXTO,
                         font=self.app.fonte(36, "bold"))
        total = sum(self.app.biblioteca.duracao(self.app.biblioteca.buscar(i)) or 0 for i in ids)
        texto_total = f"{len(ids)} músicas" + (f"  ·  {tempo(total)}" if total else "")
        self.create_text(X0 + 175, 144, text=texto_total, anchor="w",
                         fill=CINZA, font=self.app.fonte(11))
        x = X0 + 175
        if ids:
            x = self.botao(x, 162, "▶  Tocar tudo", lambda: self.app.tocar(ids, 0)) + 12
        self.botao(x, 162, "Apagar playlist", self.apagar, cor=PAINEL, cor_texto=CINZA, borda="#535353")
        self.lista_de_musicas(ids, 236, ao_remover=self.remover)
        self.barra_player()

    def remover(self, musica_id):
        self.app.playlists.remover(self.playlist_id, musica_id)
        self.desenhar()

    def apagar(self):
        self.app.playlists.apagar(self.playlist_id)
        self.app.mostrar(TelaPlaylists)


class AppStreamify:
    def __init__(self):
        self.banco = sqlite3.connect(os.path.join(PASTA_APP, "streamify.db"))
        self.biblioteca = Biblioteca(self.banco)
        self.playlists = Playlists(self.banco)
        self.player = Player(self.biblioteca)

        self.janela = tk.Tk()
        self.capas = Capas(self.biblioteca.listar())
        self.janela.title("Streamify")
        self.janela.configure(bg=FUNDO)
        self.janela.resizable(False, False)
        x = (self.janela.winfo_screenwidth() - LARGURA) // 2
        y = (self.janela.winfo_screenheight() - ALTURA) // 3
        self.janela.geometry(f"{LARGURA}x{ALTURA}+{x}+{max(0, y)}")
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar)
        self.janela.bind("<space>", lambda evento: self.alternar_tecla(evento))

        instaladas = set(tkfont.families())
        opcoes = ["Helvetica Neue", "Avenir Next", "Segoe UI", "Inter", "DejaVu Sans", "Helvetica"]
        self.familia = next((f for f in opcoes if f in instaladas), "Helvetica")
        self.fontes = {}

        self.tela = None
        self.mostrar(TelaInicio)
        self.atualizar_player()
        self.esperar_capas()

    def esperar_capas(self, vistas=0):
        if self.capas.novas != vistas:
            vistas = self.capas.novas
            self.tela.desenhar()
        if not self.capas.pronto or self.capas.novas != vistas:
            self.janela.after(500, lambda: self.esperar_capas(vistas))

    def fonte(self, tamanho, peso="normal"):
        chave = (tamanho, peso)
        if chave not in self.fontes:
            self.fontes[chave] = tkfont.Font(family=self.familia, size=tamanho, weight=peso)
        return self.fontes[chave]

    def mostrar(self, classe_tela, *argumentos):
        if self.tela is not None:
            self.tela.destroy()
        self.tela = classe_tela(self, *argumentos)
        self.tela.pack()
        self.tela.desenhar()

    def abrir_playlist(self, playlist_id):
        self.mostrar(TelaPlaylist, playlist_id)

    def tocar(self, fila, posicao):
        if self.player.tocar(fila, posicao):
            self.tela.desenhar()
        else:
            abrir_no_youtube(self.biblioteca.buscar(fila[posicao]))
            self.aviso("Sem .mp3 na pasta: abri no YouTube ↗")

    def alternar(self):
        self.player.alternar()
        self.tela.desenhar()

    def alternar_tecla(self, evento):
        if not isinstance(evento.widget, tk.Entry):
            self.alternar()

    def pular(self, passo):
        self.player.proxima(passo)
        self.tela.desenhar()

    def curtir(self, musica_id):
        self.biblioteca.curtir(musica_id)
        self.tela.desenhar()

    def menu_adicionar(self, musica_id, x, y):
        menu = tk.Menu(self.janela, tearoff=0, bg=CARD, fg=TEXTO,
                       activebackground=CARD_HOVER, activeforeground=TEXTO)
        menu.add_command(label="Adicionar à playlist:", state="disabled")
        for playlist in self.playlists.listar():
            menu.add_command(label=playlist[1],
                             command=lambda p=playlist[0]: self.adicionar(p, musica_id))
        menu.tk_popup(self.tela.winfo_rootx() + int(x), self.tela.winfo_rooty() + int(y))

    def adicionar(self, playlist_id, musica_id):
        if self.playlists.adicionar(playlist_id, musica_id):
            self.aviso("Adicionada na playlist ✓")
        else:
            self.aviso("Essa música já está nessa playlist")

    def aviso(self, texto):
        tela = self.tela
        tela.delete("aviso")
        cx, y = LARGURA / 2 + LATERAL / 2, ALTURA - BARRA_PLAYER - 36
        tela.retangulo(cx - 170, y - 20, cx + 170, y + 20, raio=20, fill=TEXTO, tags="aviso")
        tela.create_text(cx, y, text=texto, fill=FUNDO, font=self.fonte(12, "bold"), tags="aviso")
        self.janela.after(1800, lambda: tela.winfo_exists() and tela.delete("aviso"))

    def atualizar_player(self):
        if self.player.acabou():
            self.player.proxima()
            self.tela.desenhar()
        else:
            self.tela.barra_player()
            self.tela.tag_raise("aviso")
        self.janela.after(150, self.atualizar_player)

    def fechar(self):
        self.player.parar()
        self.banco.close()
        self.janela.destroy()

    def rodar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    AppStreamify().rodar()
