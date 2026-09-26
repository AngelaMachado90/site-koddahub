#!/usr/bin/env bash
set -Eeuo pipefail

PROJETO="/home/kodda/projects/site-koddahub"
PRODUCAO="/home/kodda/public_html"

PASTA_PRODUCAO="${PRODUCAO}/assets/images/blog"
PASTA_PUBLICA="${PROJETO}/public/assets/images/blog"
PASTA_ORIGINAIS="${PROJETO}/docs/editorial/assets/capas-originais"
PASTA_ARTIGOS="${PROJETO}/docs/editorial/publicados"
ARQUIVO_TESTE="${PROJETO}/tests/test_blog.py"
DIST="${PROJETO}/dist"

PUBLICAR=false
FORCAR=false

for argumento in "$@"; do
  case "$argumento" in
    --deploy|--publicar)
      PUBLICAR=true
      ;;
    --force|--forcar)
      FORCAR=true
      ;;
    -h|--help)
      cat <<'EOF'
Uso:
  ./scripts/atualizar_capas_blog.sh
  ./scripts/atualizar_capas_blog.sh --forcar
  ./scripts/atualizar_capas_blog.sh --publicar
  ./scripts/atualizar_capas_blog.sh --forcar --publicar

Comportamento:
  1. Arquiva PNGs originais de produção no projeto.
  2. Descobre automaticamente o artigo correspondente.
  3. Converte a capa para WebP usando o slug do artigo.
  4. Atualiza o campo cover: do Markdown.
  5. Atualiza referências antigas nos testes.
  6. Remove a capa anterior somente se ela ficar órfã.
  7. Executa testes e build.
  8. Faz rsync --dry-run.
  9. Só publica com --publicar.

Regras de descoberta:
  - blogcapa-DDMMAA.png -> procura artigo pela data de publicação.
  - nome-do-artigo.png -> procura por slug exato.
  - nome parcial -> procura correspondência única por palavras do slug/título.
  - exceções podem ser declaradas no arquivo:
      docs/editorial/assets/capas-blog.map

Formato do arquivo de exceções:
  arquivo.png|slug-do-artigo
EOF
      exit 0
      ;;
    *)
      echo "ERRO: argumento desconhecido: $argumento" >&2
      exit 2
      ;;
  esac
done

MAPA="${PROJETO}/docs/editorial/assets/capas-blog.map"

if [[ -t 1 ]]; then
  COR_RESET=$'\033[0m'
  COR_AZUL=$'\033[1;34m'
  COR_CIANO=$'\033[1;36m'
  COR_VERDE=$'\033[1;32m'
  COR_AMARELO=$'\033[1;33m'
  COR_VERMELHO=$'\033[1;31m'
  COR_CINZA=$'\033[0;90m'
else
  COR_RESET=""
  COR_AZUL=""
  COR_CIANO=""
  COR_VERDE=""
  COR_AMARELO=""
  COR_VERMELHO=""
  COR_CINZA=""
fi

log() {
  printf '\n%b===== %s =====%b\n' "$COR_CIANO" "$1" "$COR_RESET"
}

info() {
  printf '%bINFO:%b %s\n' "$COR_AZUL" "$COR_RESET" "$*"
}

sucesso() {
  printf '%bOK:%b %s\n' "$COR_VERDE" "$COR_RESET" "$*"
}

aviso() {
  printf '%bAVISO:%b %s\n' "$COR_AMARELO" "$COR_RESET" "$*" >&2
}

erro() {
  printf '%bERRO:%b %s\n' "$COR_VERMELHO" "$COR_RESET" "$*" >&2
  exit 1
}

exigir_comando() {
  command -v "$1" >/dev/null 2>&1 || erro "Comando obrigatório não encontrado: $1"
}

exigir_arquivo() {
  [[ -f "$1" ]] || erro "Arquivo não encontrado: $1"
}

ajustar_permissao() {
  local arquivo="$1"
  chmod 644 "$arquivo"
  if [[ "$(id -u)" -eq 0 ]] && id kodda >/dev/null 2>&1; then
    chown kodda:kodda "$arquivo"
  fi
}

for comando in cwebp python3 rsync grep sed find file stat cp; do
  exigir_comando "$comando"
done

[[ -d "$PROJETO" ]] || erro "Projeto não encontrado: $PROJETO"
[[ -d "$PASTA_PRODUCAO" ]] || erro "Pasta de produção não encontrada: $PASTA_PRODUCAO"
[[ -d "$PASTA_ARTIGOS" ]] || erro "Pasta editorial não encontrada: $PASTA_ARTIGOS"

mkdir -p "$PASTA_PUBLICA" "$PASTA_ORIGINAIS" "$(dirname "$MAPA")"

# Mantém as exceções fora do código principal.
# Só cria o arquivo se ele ainda não existir.
if [[ ! -f "$MAPA" ]]; then
  cat > "$MAPA" <<'EOF'
# arquivo_origem.png|slug-do-artigo
#
# Use apenas quando a descoberta automática por data/nome não for suficiente.
blogcapa-310826.png|o-que-e-streamlit
EOF
  ajustar_permissao "$MAPA"
fi

log "1. ARQUIVANDO CAPAS-FONTE"

shopt -s nullglob
for origem in "$PASTA_PRODUCAO"/*.png; do
  nome="$(basename "$origem")"
  destino="${PASTA_ORIGINAIS}/${nome}"

  if [[ ! -f "$destino" || "$origem" -nt "$destino" ]]; then
    cp -p "$origem" "$destino"
    ajustar_permissao "$destino"
    sucesso "Arquivado: $nome"
  fi
done
shopt -u nullglob

TOTAL_ORIGINAIS="$(find "$PASTA_ORIGINAIS" -maxdepth 1 -type f -iname '*.png' | wc -l | tr -d ' ')"
[[ "$TOTAL_ORIGINAIS" -gt 0 ]] || erro "Nenhum PNG de capa foi encontrado para processar."

log "2. DESCOBRINDO E PROCESSANDO CAPAS"

python3 - \
  "$PROJETO" \
  "$PASTA_ORIGINAIS" \
  "$PASTA_PUBLICA" \
  "$PASTA_ARTIGOS" \
  "$ARQUIVO_TESTE" \
  "$MAPA" \
  "$FORCAR" <<'PY'
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import subprocess
import sys

USE_COLOR = sys.stdout.isatty()
RESET = "\033[0m" if USE_COLOR else ""
AZUL = "\033[1;34m" if USE_COLOR else ""
CIANO = "\033[1;36m" if USE_COLOR else ""
VERDE = "\033[1;32m" if USE_COLOR else ""
AMARELO = "\033[1;33m" if USE_COLOR else ""
VERMELHO = "\033[1;31m" if USE_COLOR else ""
CINZA = "\033[0;90m" if USE_COLOR else ""

def p_info(msg: str):
    print(f"{AZUL}{msg}{RESET}")

def p_ok(msg: str):
    print(f"{VERDE}{msg}{RESET}")

def p_warn(msg: str):
    print(f"{AMARELO}{msg}{RESET}")

def p_error(msg: str):
    print(f"{VERMELHO}{msg}{RESET}")

def p_label(label: str, value: str):
    print(f"{CIANO}{label:<8}{RESET}{value}")
import unicodedata

projeto = Path(sys.argv[1])
pasta_originais = Path(sys.argv[2])
pasta_publica = Path(sys.argv[3])
pasta_artigos = Path(sys.argv[4])
arquivo_teste = Path(sys.argv[5])
arquivo_mapa = Path(sys.argv[6])
forcar = sys.argv[7].lower() == "true"

STOPWORDS = {
    "a", "as", "ao", "aos", "da", "das", "de", "do", "dos",
    "e", "em", "na", "nas", "no", "nos", "o", "os", "para",
    "por", "que", "um", "uma"
}

def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")

def tokens(texto: str) -> set[str]:
    return {
        t for t in normalizar(texto).split("-")
        if t and t not in STOPWORDS and len(t) > 1
    }

def ler_front_matter(caminho: Path) -> dict[str, str]:
    texto = caminho.read_text(encoding="utf-8")
    if not texto.startswith("---"):
        return {}

    partes = texto.split("---", 2)
    if len(partes) < 3:
        return {}

    dados: dict[str, str] = {}
    for linha in partes[1].splitlines():
        if ":" not in linha:
            continue
        chave, valor = linha.split(":", 1)
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")
        if chave in {"title", "slug", "publish_date", "date", "cover", "status"}:
            dados[chave] = valor
    return dados

artigos = []
for md in sorted(pasta_artigos.glob("*.md")):
    meta = ler_front_matter(md)
    slug = meta.get("slug", "").strip()
    if not slug:
        continue

    artigos.append({
        "arquivo": md,
        "slug": slug,
        "titulo": meta.get("title", ""),
        "data": meta.get("publish_date") or meta.get("date") or "",
        "cover": meta.get("cover", ""),
        "status": meta.get("status", ""),
    })

if not artigos:
    raise SystemExit("ERRO: nenhum artigo com slug foi encontrado.")

mapa: dict[str, str] = {}
if arquivo_mapa.exists():
    for linha in arquivo_mapa.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "|" not in linha:
            continue
        origem, slug = linha.split("|", 1)
        mapa[origem.strip()] = slug.strip()

por_slug = {a["slug"]: a for a in artigos}

def artigo_por_data(nome_arquivo: str):
    m = re.fullmatch(r"blogcapa-(\d{2})(\d{2})(\d{2})\.png", nome_arquivo, re.I)
    if not m:
        return None

    dia, mes, ano = m.groups()
    data = f"20{ano}-{mes}-{dia}"

    encontrados = [a for a in artigos if a["data"] == data]
    if len(encontrados) == 1:
        return encontrados[0]
    return None

def artigo_por_nome(nome_arquivo: str):
    base = Path(nome_arquivo).stem
    normal = normalizar(base)

    if normal in por_slug:
        return por_slug[normal]

    candidatos = []
    origem_tokens = tokens(base)
    if not origem_tokens:
        return None

    for artigo in artigos:
        alvo_tokens = tokens(artigo["slug"]) | tokens(artigo["titulo"])
        inter = origem_tokens & alvo_tokens

        if not inter:
            continue

        cobertura_origem = len(inter) / len(origem_tokens)
        cobertura_alvo = len(inter) / max(1, min(len(alvo_tokens), len(origem_tokens) + 3))

        score = (cobertura_origem * 0.75) + (cobertura_alvo * 0.25)
        candidatos.append((score, artigo))

    candidatos.sort(key=lambda x: x[0], reverse=True)

    if not candidatos:
        return None

    melhor_score, melhor = candidatos[0]
    segundo_score = candidatos[1][0] if len(candidatos) > 1 else 0

    # Só aceita fuzzy match quando a origem está quase toda representada
    # e há distância suficiente do segundo candidato.
    if melhor_score >= 0.72 and (melhor_score - segundo_score >= 0.12 or melhor_score >= 0.90):
        return melhor

    return None

def resolver_artigo(origem: Path):
    if origem.name in mapa:
        slug = mapa[origem.name]
        artigo = por_slug.get(slug)
        if artigo:
            return artigo, "mapa"
        p_warn(f"AVISO: {origem.name}: slug do mapa não existe: {slug}")
        return None, None

    artigo = artigo_por_data(origem.name)
    if artigo:
        return artigo, "data"

    artigo = artigo_por_nome(origem.name)
    if artigo:
        return artigo, "nome"

    return None, None

def substituir_cover(artigo: dict, novo_cover: str):
    caminho = artigo["arquivo"]
    texto = caminho.read_text(encoding="utf-8")
    linhas = texto.splitlines()

    for i, linha in enumerate(linhas):
        if linha.startswith("cover:"):
            linhas[i] = f"cover: {novo_cover}"
            caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
            return
    raise RuntimeError(f"campo cover: não encontrado em {caminho}")

def atualizar_testes(valor_antigo: str, valor_novo: str):
    if not arquivo_teste.exists() or not valor_antigo:
        return

    texto = arquivo_teste.read_text(encoding="utf-8")

    antigo_nome = Path(valor_antigo).name
    novo_nome = Path(valor_novo).name

    novo_texto = texto.replace(valor_antigo, valor_novo)
    novo_texto = novo_texto.replace(antigo_nome, novo_nome)

    if novo_texto != texto:
        arquivo_teste.write_text(novo_texto, encoding="utf-8")

def cover_ainda_usado(cover: str) -> bool:
    if not cover:
        return False

    for artigo in artigos:
        meta = ler_front_matter(artigo["arquivo"])
        if meta.get("cover") == cover:
            return True
    return False

processadas = []
ignoradas = []

for origem in sorted(pasta_originais.glob("*.png")):
    artigo, metodo = resolver_artigo(origem)

    if not artigo:
        ignoradas.append(origem.name)
        p_warn(f"IGNORADA: {origem.name} — não foi possível associar com segurança a um artigo.")
        continue

    slug = artigo["slug"]
    destino = pasta_publica / f"{slug}.webp"
    novo_cover = f"/assets/images/blog/{slug}.webp"
    cover_anterior = artigo["cover"]

    precisa_converter = (
        forcar
        or not destino.exists()
        or origem.stat().st_mtime > destino.stat().st_mtime
    )

    print()
    p_label("Origem:", origem.name)
    p_label("Artigo:", artigo["titulo"] or slug)
    p_label("Slug:", slug)
    p_label("Método:", metodo)
    p_label("Destino:", destino.name)

    if precisa_converter:
        subprocess.run(
            ["cwebp", "-quiet", "-q", "85", str(origem), "-o", str(destino)],
            check=True,
        )
        destino.chmod(0o644)
        p_ok("Ação    convertido")
    else:
        p_info("Ação    WebP já atualizado; conversão ignorada")

    if cover_anterior != novo_cover:
        substituir_cover(artigo, novo_cover)
        atualizar_testes(cover_anterior, novo_cover)
        artigo["cover"] = novo_cover
        p_ok(f"Cover   {cover_anterior or '(vazio)'} -> {novo_cover}")
    else:
        p_ok(f"Cover   já correto ({novo_cover})")

    # Remove a capa antiga do projeto somente se não for mais referenciada.
    if cover_anterior and cover_anterior != novo_cover and cover_anterior.startswith("/assets/images/blog/"):
        antigo = pasta_publica / Path(cover_anterior).name
        if antigo.exists() and not cover_ainda_usado(cover_anterior):
            antigo.unlink()
            p_warn(f"Limpeza removido arquivo órfão {antigo.name}")

    processadas.append((origem.name, slug, destino.name))

print()
p_info("RESUMO")
p_ok(f"Processadas: {len(processadas)}")
p_warn(f"Ignoradas  : {len(ignoradas)}") if ignoradas else p_ok("Ignoradas  : 0")

for origem, slug, destino in processadas:
    p_ok(f"  OK  {origem} -> {slug} -> {destino}")

for origem in ignoradas:
    p_warn(f"  ?   {origem}")

if not processadas:
    raise SystemExit("ERRO: nenhuma capa pôde ser processada com segurança.")
PY

# Ajusta dono apenas quando o script estiver rodando como root.
if [[ "$(id -u)" -eq 0 ]] && id kodda >/dev/null 2>&1; then
  chown -R kodda:kodda "$PASTA_PUBLICA" "$PASTA_ORIGINAIS"
  [[ -f "$ARQUIVO_TESTE" ]] && chown kodda:kodda "$ARQUIVO_TESTE"
  find "$PASTA_ARTIGOS" -maxdepth 1 -type f -name '*.md' -exec chown kodda:kodda {} +
fi

log "3. VALIDANDO TODAS AS CAPAS DOS ARTIGOS"

python3 - "$PROJETO" "$PASTA_ARTIGOS" <<'PY'
from pathlib import Path
import re
import sys

USE_COLOR = sys.stdout.isatty()
RESET = "\033[0m" if USE_COLOR else ""
VERDE = "\033[1;32m" if USE_COLOR else ""
VERMELHO = "\033[1;31m" if USE_COLOR else ""

def p_ok(msg: str):
    print(f"{VERDE}{msg}{RESET}")

def p_error(msg: str):
    print(f"{VERMELHO}{msg}{RESET}")

projeto = Path(sys.argv[1])
artigos = Path(sys.argv[2])

erros = []

for md in sorted(artigos.glob("*.md")):
    texto = md.read_text(encoding="utf-8")

    m_slug = re.search(r"^slug:\s*[\"']?([^\"'\n]+)", texto, re.M)
    m_cover = re.search(r"^cover:\s*[\"']?([^\"'\n]+)", texto, re.M)

    if not m_slug:
        continue

    slug = m_slug.group(1).strip()

    if not m_cover:
        erros.append(f"{md.name}: sem cover")
        continue

    cover = m_cover.group(1).strip()

    if cover.startswith("/"):
        arquivo = projeto / "public" / cover.lstrip("/")
        if not arquivo.exists():
            erros.append(f"{md.name}: capa inexistente: {cover}")

if erros:
    p_error("\n".join(f"ERRO: {e}" for e in erros))
    raise SystemExit(1)

p_ok("OK: todas as capas locais referenciadas pelos artigos existem.")
PY

log "4. TESTES DO BLOG"

cd "$PROJETO"
python3 -m unittest discover -s tests -p 'test_blog.py' -v

log "5. BUILD"

python3 scripts/build.py

log "6. VALIDAÇÃO DO BUILD"

python3 - "$PROJETO" "$DIST" "$PASTA_ARTIGOS" <<'PY'
from pathlib import Path
import re
import sys

USE_COLOR = sys.stdout.isatty()
RESET = "\033[0m" if USE_COLOR else ""
VERDE = "\033[1;32m" if USE_COLOR else ""
VERMELHO = "\033[1;31m" if USE_COLOR else ""

def p_ok(msg: str):
    print(f"{VERDE}{msg}{RESET}")

def p_error(msg: str):
    print(f"{VERMELHO}{msg}{RESET}")

projeto = Path(sys.argv[1])
dist = Path(sys.argv[2])
artigos = Path(sys.argv[3])

erros = []

for md in sorted(artigos.glob("*.md")):
    texto = md.read_text(encoding="utf-8")
    m_slug = re.search(r"^slug:\s*[\"']?([^\"'\n]+)", texto, re.M)
    m_cover = re.search(r"^cover:\s*[\"']?([^\"'\n]+)", texto, re.M)

    if not m_slug or not m_cover:
        continue

    slug = m_slug.group(1).strip()
    cover = m_cover.group(1).strip()

    if cover.startswith("/assets/images/blog/"):
        capa_dist = dist / cover.lstrip("/")
        html = dist / "blog" / slug / "index.html"

        if not capa_dist.exists():
            erros.append(f"{slug}: capa ausente no dist: {cover}")

        if not html.exists():
            erros.append(f"{slug}: HTML não gerado")
        elif cover not in html.read_text(encoding="utf-8"):
            erros.append(f"{slug}: HTML não referencia {cover}")

if erros:
    p_error("\n".join(f"ERRO: {e}" for e in erros))
    raise SystemExit(1)

p_ok("OK: capas e HTMLs validados no dist.")
PY

log "7. VERIFICANDO REFERÊNCIAS A BLOGCAPA PNG NO DIST"

if grep -RniE 'assets/images/blog/blogcapa-[0-9]{6}\.png' "$DIST"; then
  erro "O build ainda contém referência a uma blogcapa PNG."
else
  sucesso "Nenhuma blogcapa PNG referenciada no dist."
fi

log "8. RSYNC DRY-RUN"

rsync -avhn --delete \
  "${DIST}/" \
  "${PRODUCAO}/"

if [[ "$PUBLICAR" == true ]]; then
  log "9. PUBLICAÇÃO"

  rsync -avh --delete \
    "${DIST}/" \
    "${PRODUCAO}/"

  log "10. VALIDAÇÃO PÓS-PUBLICAÇÃO"

  python3 - "$PROJETO" "$PRODUCAO" "$PASTA_ARTIGOS" <<'PY'
from pathlib import Path
import re
import sys

USE_COLOR = sys.stdout.isatty()
RESET = "\033[0m" if USE_COLOR else ""
VERDE = "\033[1;32m" if USE_COLOR else ""
VERMELHO = "\033[1;31m" if USE_COLOR else ""

def p_ok(msg: str):
    print(f"{VERDE}{msg}{RESET}")

def p_error(msg: str):
    print(f"{VERMELHO}{msg}{RESET}")

projeto = Path(sys.argv[1])
producao = Path(sys.argv[2])
artigos = Path(sys.argv[3])

erros = []

for md in sorted(artigos.glob("*.md")):
    texto = md.read_text(encoding="utf-8")
    m_slug = re.search(r"^slug:\s*[\"']?([^\"'\n]+)", texto, re.M)
    m_cover = re.search(r"^cover:\s*[\"']?([^\"'\n]+)", texto, re.M)

    if not m_slug or not m_cover:
        continue

    slug = m_slug.group(1).strip()
    cover = m_cover.group(1).strip()

    if not cover.startswith("/assets/images/blog/"):
        continue

    capa = producao / cover.lstrip("/")
    html = producao / "blog" / slug / "index.html"

    if not capa.exists():
        erros.append(f"{slug}: capa ausente em produção: {cover}")
    if not html.exists():
        erros.append(f"{slug}: HTML ausente em produção")
    elif cover not in html.read_text(encoding="utf-8"):
        erros.append(f"{slug}: HTML de produção não referencia a capa correta")

if erros:
    p_error("\n".join(f"ERRO: {e}" for e in erros))
    raise SystemExit(1)

p_ok("OK: publicação validada.")
PY

  echo
  sucesso "PUBLICAÇÃO CONCLUÍDA."
else
  echo
  sucesso "DRY-RUN CONCLUÍDO — PRODUÇÃO NÃO FOI ALTERADA."
  echo
  echo "Se a lista acima estiver correta, publique com:"
  echo "  ./scripts/atualizar_capas_blog.sh --publicar"
fi
