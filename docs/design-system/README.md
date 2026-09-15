# Koddahub Design System

**Documento:** KDH-DS-001

**Versão:** 1.0

**Status:** Ativo

**Última atualização:** 15/09/2026

**Responsável:** Koddahub

**Classificação:** Uso interno

## 1. Fonte de verdade

Os valores em
[`public/assets/css/koddahub-tokens.css`](../../public/assets/css/koddahub-tokens.css)
são a fonte de verdade visual da interface. Componentes novos não devem repetir
hexadecimais quando existir um token equivalente.

O sistema complementa o Bootstrap 5.3 presente no projeto. Utilities e
componentes do framework continuam preferenciais; tokens Koddahub definem marca,
tema e variações funcionais sem criar um framework paralelo.

## 2. Identidade da marca

O nome visual oficial é **KoddaHub**:

- **Kodda = roxo**;
- **Hub = amarelo**.

Nunca inverta as cores. Azul não é cor oficial de “Hub”. A regra vale para o
wordmark textual estilizado em header, footer, créditos e componentes futuros.
Menções corridas e metadados podem permanecer em texto comum.

### Uso correto

```html
<span class="kdh-brand-wordmark" aria-label="KoddaHub">
  <span class="kdh-brand-kodda" aria-hidden="true">Kodda</span><span class="kdh-brand-hub" aria-hidden="true">Hub</span>
</span>
```

Em fundo escuro, acrescente `kdh-brand-wordmark-on-dark`. O componente usa
`white-space: nowrap` para impedir a quebra entre Kodda e Hub.

Para “desenvolvido por KoddaHub”:

```html
<span class="kdh-credit">
  desenvolvido por
  <span class="kdh-brand-wordmark" aria-label="KoddaHub">
    <span class="kdh-brand-kodda" aria-hidden="true">Kodda</span><span class="kdh-brand-hub" aria-hidden="true">Hub</span>
  </span>
</span>
```

### Uso incorreto

- Kodda preto e Hub azul;
- Kodda e Hub azuis;
- Kodda roxo e Hub azul;
- Kodda amarelo e Hub roxo.

Os assets gráficos atuais usam uma paleta multicolorida e não representam
literalmente o novo wordmark roxo/amarelo. Eles foram preservados nesta etapa,
pois símbolo, geometria, tipografia e arquivos oficiais exigem revisão de marca
separada antes de qualquer alteração.

## 3. Cores

### Marca e uso funcional

| Token | Nome | Hex/RGB | Uso |
| --- | --- | --- | --- |
| `--kdh-brand-kodda` | Kodda Purple | `#7C3AED` / `124, 58, 237` | “Kodda” no wordmark e identidade principal |
| `--kdh-brand-hub` | Hub Yellow | `#FACC15` / `250, 204, 21` | “Hub” no wordmark e acentos |
| `--kdh-brand-kodda-on-dark` | Kodda Purple on Dark | `#A78BFA` / `167, 139, 250` | Wordmark sobre fundo escuro |
| `--kdh-brand-hub-on-dark` | Hub Yellow on Dark | `#FDE047` / `253, 224, 71` | Wordmark sobre fundo escuro |
| `--kdh-primary` | Primary | `#6D28D9` / `109, 40, 217` | Ações, links e estados funcionais |
| `--kdh-primary-hover` | Primary Hover | `#5B21B6` / `91, 33, 182` | Hover de ação primária |
| `--kdh-primary-active` | Primary Active | `#4C1D95` / `76, 29, 149` | Estado ativo |
| `--kdh-accent` | Accent | `#FACC15` / `250, 204, 21` | Destaques controlados e superfícies escuras |
| `--kdh-text-accent-yellow` | Accessible Yellow Text | `#854D0E` / `133, 77, 14` | Texto funcional em fundo claro |
| `--kdh-focus-ring` | Focus Ring | `rgba(124, 58, 237, .38)` | Indicação de foco por teclado |

O amarelo oficial não deve ser usado como texto pequeno essencial em fundo
branco. Para texto funcional, use `--kdh-text-accent-yellow`. A identidade do
wordmark preserva o amarelo oficial e fornece o nome completo por semântica
acessível.

### Neutros e feedback

| Papel | Token | Valor |
| --- | --- | --- |
| Background | `--kdh-bg` | `#F8FAFC` |
| Background sutil | `--kdh-bg-subtle` | `#F1F5F9` |
| Surface | `--kdh-surface` | `#FFFFFF` |
| Text primary | `--kdh-text-primary` | `#0F172A` |
| Text secondary | `--kdh-text-secondary` | `#334155` |
| Text muted | `--kdh-text-muted` | `#64748B` |
| Border | `--kdh-border` | `#CBD5E1` |
| Border sutil | `--kdh-border-subtle` | `#E2E8F0` |
| Success | `--kdh-success` | `#15803D` |
| Warning | `--kdh-warning` | `#A16207` |
| Danger | `--kdh-danger` | `#B91C1C` |
| Info | `--kdh-info` | `#0369A1` |

Feedback não deve ser substituído por roxo ou amarelo. A composição geral
usa aproximadamente 70–80% de neutros, 15–25% de roxo e 5–10% de amarelo como
orientação, não como regra matemática.

## 4. Fundos e contraste

- Em branco ou neutro claro, use os tokens oficiais do wordmark.
- Em fundo escuro, use `kdh-brand-wordmark-on-dark`.
- Em cards, mantenha superfície neutra e reserve amarelo para acentos.
- Não dependa apenas da cor para comunicar estado, erro ou seleção.

Contrastes medidos:

| Combinação | Razão aproximada | Decisão |
| --- | ---: | --- |
| Kodda Purple `#7C3AED` sobre branco | 5,70:1 | Aprovado para texto normal |
| Hub Yellow `#FACC15` sobre branco | 1,53:1 | Restrito ao wordmark/acento não essencial |
| Accessible Yellow `#854D0E` sobre branco | 6,85:1 | Aprovado para texto funcional |
| Kodda Purple on Dark `#A78BFA` sobre `#0F172A` | 6,56:1 | Aprovado para texto normal |
| Hub Yellow on Dark `#FDE047` sobre `#0F172A` | 13,54:1 | Aprovado para texto normal |

## 5. Tipografia

A família atual foi preservada: `Inter, ui-sans-serif, system-ui, -apple-system,
"Segoe UI", sans-serif`. Pesos adotados: 400, 500, 600, 700 e 800.

| Papel | Diretriz |
| --- | --- |
| Display/H1 | `clamp(3rem, 4.45vw, 4.75rem)`, peso 800 |
| H2 | `clamp(2.2rem, 4.2vw, 4.2rem)`, peso 800 |
| H3 | 1,28–2rem conforme o componente, peso 800 |
| Body | 1rem, peso 400, line-height mínimo recomendado de 1,5 |
| Small | 0,82–0,9rem conforme o contexto |
| Caption | 0,72–0,78rem, com contraste adequado |
| Label | 0,72–0,88rem, peso 700 ou 800 |

## 6. Espaçamento, raios e sombras

A escala de espaçamento usa base de 4 px: 4, 8, 12, 16, 24, 32, 48 e 64 px,
exposta nos tokens `--kdh-space-*`. Ela orienta componentes novos sem exigir
reescrita mecânica dos existentes.

Use `--kdh-radius-sm`, `md`, `lg`, `xl` e `pill`. Para elevação, use
`--kdh-shadow-sm`, `md` e `lg`; sombras devem permanecer suaves.

## 7. Componentes

| Componente | Padrão |
| --- | --- |
| Brand Wordmark | Classes `kdh-brand-wordmark`, `kdh-brand-kodda` e `kdh-brand-hub`; nome acessível e sem quebra |
| Button Primary | Bootstrap `.btn` + `.btn-brand`; roxo funcional, texto branco e estados hover/focus |
| Button Secondary | Bootstrap `.btn-outline-*`; contraste e foco preservados |
| Button Accent | Amarelo sobre texto escuro, reservado a destaque em superfície escura |
| Card | Superfície neutra, borda sutil, raio `lg` e sombra apenas quando necessária |
| Badge | Não comunicar estado somente por cor; manter texto descritivo |
| Input | Bootstrap `.form-control`, borda neutra e focus ring roxo |
| Navbar | Bootstrap responsivo; wordmark oficial no nome textual |
| Footer | Neutro; wordmark oficial e links com contraste |
| Alert | Semântica Bootstrap e tokens de feedback, independentes da marca |
| Link | Roxo funcional, sublinhado quando o contexto exigir distinção |
| Focus State | Contorno e anel visíveis; nunca remover sem alternativa |

### Launcher do chatbot

O launcher anterior em formato horizontal foi substituído por um botão circular
fixado no canto inferior direito. O componente preserva a classe
`kodda-chat-trigger` consumida pelo JavaScript existente.

| Propriedade | Desktop | Mobile |
| --- | --- | --- |
| Dimensão | 64 × 64 px | 56 × 56 px |
| Distância inferior | 24 px | 16 px |
| Distância direita | 24 px | 16 px |
| Conteúdo | Ícone de chat amarelo sobre roxo | Mesmo ícone, sem tooltip permanente |

O texto “Tire suas dúvidas” é apresentado em um balão lateral discreto no
`hover` e no `focus-visible`. O botão usa elemento `button`,
`aria-label="Tire suas dúvidas"`, `aria-controls` e `aria-expanded`. Hover eleva
o componente e reforça suavemente a sombra; foco por teclado acrescenta
contorno e anel visíveis. Ao abrir o painel, a lógica JavaScript existente
oculta o launcher; ao fechar, restaura o botão e devolve o foco.

### Tabelas comparativas editoriais

Use tabela semântica no desktop quando a comparação entre colunas for a ideia
principal. Preserve `thead`, `tbody`, `scope="col"` e `scope="row"`. Adote
`table-layout: auto`, reserve espaço suficiente para a coluna de conceitos e
impeça quebra arbitrária de termos curtos. Descrições podem quebrar
naturalmente entre palavras.

Abaixo de 768 px, transforme visualmente cada linha em card quando três ou mais
colunas comprimirem a leitura. O conteúdo e a tabela permanecem únicos no HTML;
os rótulos auxiliares vêm de `data-label`. Título e badge usam flex com wrap: o
badge muda de linha antes de apertar o título. A legenda fica fora da tabela,
com cor secundária e espaçamento que preserve sua função de explicação.

## 8. Governança

- Reutilize tokens antes de adicionar cores ou valores paralelos.
- Diferencie cor de marca, cor funcional, feedback e cores pertencentes a
  clientes ou visualizações de dados.
- Não aplique estes tokens à identidade da Ouça Mais ou de outros clientes.
- Valide componentes em mobile, tablet e desktop, além de teclado, foco e
  contraste.
- O projeto ainda não possui dark mode global. Os tokens `on-dark` atendem
  componentes sobre superfícies escuras sem declarar um tema inexistente.
- Alterar símbolo, logo, favicon ou geometria exige uma revisão de branding
  separada.
