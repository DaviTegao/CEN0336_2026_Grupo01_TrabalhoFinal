#pacotes

import sys

# Função para abrir 

def carregar_tabela(caminho): 
    with open(caminho, encoding="utf-8") as f:
        linhas = [l.strip() for l in f if l.strip()]

    brutas = []
    for n, linha in enumerate(linhas, 1):
        campos = [c.strip() for c in linha.split(";")]
        while campos and campos[-1] == "":
            campos.pop()
        if len(campos) != 3:
            print(f"[aviso] linha {n} ignorada (esperava 3 campos, achei {len(campos)}): {linha}")
            continue
        brutas.append(tuple(campos))
    return brutas

#  Conversão da tabela em dicionarios

def montar_dicionarios(brutas):
    perguntas = {}
    respostas = {}
    cod_p, cod_r = {}, {}

    def sigla_p(txt):
        if txt not in cod_p:
            cod_p[txt] = f"P{len(cod_p) + 1}"
            perguntas[cod_p[txt]] = txt
        return cod_p[txt]

    def sigla_r(txt):
        if txt not in cod_r:
            cod_r[txt] = f"R{len(cod_r) + 1}"
            respostas[cod_r[txt]] = txt
        return cod_r[txt]

    def sigla(txt):
        return sigla_p(txt) if txt.endswith("?") else sigla_r(txt)

    for q, _, _ in brutas:
        sigla_p(q)

    conversao = {}
    for q, sim, nao in brutas:
        conversao[cod_p[q]] = {"sim": sigla(sim), "nao": sigla(nao)}

    for p in perguntas:
        if p not in conversao:
            print(f"[aviso] {p} ('{perguntas[p]}') é citada mas não tem linha própria na tabela.")
    return perguntas, conversao, respostas
      
# Idintificador

def identificar(perguntas, conversao, respostas, inicio="P1"):
    px = inicio
    hist = []
    while True:
        while True:
            r = input(f"\n{perguntas[px]} (s/n): ").strip().lower()
            if r in ("s", "n", "sim", "nao", "não"):
                break
            print("Responda com s ou n.")
        chave = "sim" if r.startswith("s") else "nao"
        hist.append((perguntas[px], "Sim" if chave == "sim" else "Não"))
        destino = conversao[px][chave]
        if destino.startswith("R"):
            print(f"\n>>> Resultado: {respostas[destino]}")
            while True:
                d_hist = input("\nDeseja ver o histórico de perguntas? (s/n): ").strip().lower()
                if d_hist in ("s", "sim", "n", "nao", "não"):
                    break
                print("Responda com s ou n.")
            if d_hist in ("s", "sim"):
                print(f"\nCaminho percorrido:\n")
                for i, (pergunta, resp) in enumerate(hist, 1):
                    print(f"{i}. {pergunta} -> {resp}")
            return respostas[destino]
            return hist
        px = destino

# Executando o código

if __name__ == "__main__":
    caminho = sys.argv[1]
    brutas = carregar_tabela(caminho)
    perguntas, conversao, respostas = montar_dicionarios(brutas)

    identificar(perguntas, conversao, respostas)
