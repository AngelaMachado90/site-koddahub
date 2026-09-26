# KoddaHub Design System

**Versão:** 1.0
**Status:** Ativo
**Projeto:** Site Institucional KoddaHub
**Escopo:** Site, Blog, Landing Pages e interfaces públicas da KoddaHub

---

## 1. Objetivo

Este documento define o Design System oficial da KoddaHub.

Seu objetivo é garantir consistência visual, acessibilidade, clareza e reutilização de componentes em todas as páginas públicas da marca.

Qualquer nova página, componente ou alteração visual deve respeitar este documento.

O Design System é a fonte de verdade para:

- identidade visual;
- cores;
- tipografia;
- espaçamento;
- bordas;
- sombras;
- botões;
- formulários;
- cards;
- navegação;
- estados;
- responsividade;
- acessibilidade;
- uso da marca;
- imagens;
- direção visual;
- comportamento de componentes.

---

## 2. Princípios da marca

A KoddaHub deve transmitir:

**Tecnologia + Clareza + Criatividade + Proximidade + Profissionalismo**

A experiência deve ser moderna sem parecer excessivamente técnica.

A interface deve facilitar a compreensão de tecnologia por pessoas com diferentes níveis de conhecimento.

### Regra visual principal

> Roxo conduz. Amarelo destaca. Neutros organizam.

O roxo é a principal cor institucional.

O amarelo é uma cor de apoio e destaque.

Cores semânticas devem ser utilizadas apenas para comunicar estados.

---

## 3. Identidade da marca

### 3.1 Logo

A assinatura institucional utiliza:

- **Kodda** → roxo;
- **Hub** → amarelo.

O logo oficial não deve ser redesenhado, distorcido, recolorido ou alterado.

Sempre utilizar os arquivos oficiais disponíveis em:

```text
/public/assets/images/logo/
```

### 3.2 Área de proteção

Manter espaço livre ao redor do logo.

Nenhum texto, botão, borda ou elemento visual deve ficar encostado ao logo.

Como regra mínima, utilizar uma área de respiro equivalente à altura aproximada da letra **K** da marca.

### 3.3 Aplicações recomendadas

Preferir:

- fundo branco;
- fundo muito claro;
- fundo escuro institucional quando existir versão compatível do logo.

Evitar:

- fundos visualmente poluídos;
- contraste insuficiente;
- distorção de proporção;
- sombras aplicadas diretamente ao logo;
- efeitos de brilho;
- alterações de cor;
- recortes que removam parte da marca.

---

## 4. Paleta institucional

### 4.1 Primary — Kodda Purple

```text
Primary:       #7C3AED
Primary Hover: #6D28D9
Primary Light: #A78BFA
Primary Soft:  #F3E8FF
```

Uso:

- CTAs principais;
- links;
- ícones institucionais;
- destaques;
- elementos ativos;
- indicadores de navegação;
- elementos relacionados à marca.

### 4.2 Accent — Kodda Yellow

```text
Accent:       #FACC15
Accent Hover: #EAB308
Accent Soft:  #FEF9C3
```

Uso:

- destaque visual;
- pequenos detalhes da marca;
- badges;
- ícones;
- palavras-chave;
- elementos promocionais pontuais.

O amarelo não deve competir visualmente com o roxo.

### 4.3 Regra de contraste

Não utilizar texto branco sobre `#FACC15`.

Preferir:

```text
Texto escuro: #111827
```

---

## 5. Cores neutras

```text
Neutral 950: #111827
Neutral 900: #171717
Neutral 800: #1F2937
Neutral 700: #374151
Neutral 600: #4B5563
Neutral 500: #6B7280
Neutral 400: #9CA3AF
Neutral 300: #D1D5DB
Neutral 200: #E5E7EB
Neutral 100: #F3F4F6
Neutral 50:  #F8FAFC
White:       #FFFFFF
```

### 5.1 Hierarquia de texto

```text
Texto principal:    #111827
Texto secundário:   #4B5563
Texto auxiliar:     #6B7280
Texto desabilitado: #9CA3AF
```

Nunca depender exclusivamente de uma cor herdada para textos importantes.

---

## 6. Cores semânticas

```text
Success: #16A34A
Info:    #2563EB
Warning: #F59E0B
Danger:  #DC2626
```

Essas cores representam estados.

Não utilizá-las como cores institucionais.

Exemplos:

- **Success** → operação concluída;
- **Info** → informação adicional;
- **Warning** → atenção necessária;
- **Danger** → erro ou ação destrutiva.

---

## 7. Tipografia

### 7.1 Fonte de títulos

**Poppins**

Uso:

- Hero;
- H1;
- H2;
- H3;
- chamadas;
- números em destaque;
- CTAs estratégicos.

Pesos recomendados:

```text
600 — Semibold
700 — Bold
800 — Extra Bold
```

### 7.2 Fonte de interface e conteúdo

**Inter**

Uso:

- parágrafos;
- blog;
- navegação;
- formulários;
- cards;
- tabelas;
- labels;
- textos auxiliares.

Pesos recomendados:

```text
400 — Regular
500 — Medium
600 — Semibold
700 — Bold
```

---

## 8. Escala tipográfica

### 8.1 Desktop

```text
Display:     56px / 1.10
H1:          44px / 1.15
H2:          36px / 1.20
H3:          28px / 1.30
H4:          22px / 1.35
Body Large:  18px / 1.60
Body:        16px / 1.60
Small:       14px / 1.50
Caption:     12px / 1.40
```

### 8.2 Mobile

```text
Display:     40px
H1:          36px
H2:          30px
H3:          24px
H4:          20px
Body Large:  18px
Body:        16px
Small:       14px
Caption:     12px
```

Evitar textos de conteúdo abaixo de `14px`.

---

## 9. Espaçamento

A escala base utiliza múltiplos de `4px`.

```text
space-1:   4px
space-2:   8px
space-3:  12px
space-4:  16px
space-5:  20px
space-6:  24px
space-8:  32px
space-10: 40px
space-12: 48px
space-16: 64px
space-20: 80px
space-24: 96px
```

### 9.1 Seções

Desktop:

```text
64px a 96px
```

Mobile:

```text
40px a 64px
```

Evitar espaçamentos arbitrários quando já existir um token adequado.

---

## 10. Layout e container

### 10.1 Container padrão

Largura máxima recomendada:

```text
1200px
```

### 10.2 Conteúdo editorial e blog

```text
720px a 800px
```

### 10.3 Padding lateral

```text
Desktop: 24px
Tablet:  24px
Mobile:  20px
```

### 10.4 Grid

Preferir grids responsivos baseados em CSS Grid ou Bootstrap quando o projeto estiver usando Bootstrap.

Regras:

- evitar largura fixa em componentes de conteúdo;
- evitar `position: absolute` para layout estrutural;
- preservar ritmo vertical;
- manter alinhamento consistente entre seções.

---

## 11. Border Radius

```text
radius-sm:   6px
radius-md:  10px
radius-lg:  16px
radius-xl:  24px
radius-pill: 999px
```

Uso recomendado:

```text
Inputs:                 10px
Botões:                 10px
Cards:                  16px
Containers especiais:  24px
Badges:                 999px
```

---

## 12. Bordas

Borda padrão:

```text
1px solid #E5E7EB
```

Borda de campos:

```text
1px solid #D1D5DB
```

Borda de foco:

```text
#7C3AED
```

Evitar bordas escuras e pesadas sem necessidade funcional.

---

## 13. Sombras

### 13.1 Small

```css
box-shadow: 0 2px 8px rgba(17, 24, 39, 0.05);
```

### 13.2 Medium

```css
box-shadow: 0 4px 16px rgba(17, 24, 39, 0.08);
```

### 13.3 Large

```css
box-shadow: 0 12px 32px rgba(17, 24, 39, 0.12);
```

Sombras devem criar profundidade de forma discreta.

Evitar sombras muito escuras ou exageradas.

---

## 14. Botões

### 14.1 Primary

Uso: ação principal de uma área.

```text
Background: #7C3AED
Texto:      #FFFFFF
Hover:      #6D28D9
Radius:     10px
Altura:     44px a 48px
```

Exemplos:

- Solicitar orçamento;
- Conhecer soluções;
- Falar com a KoddaHub;
- Começar agora.

### 14.2 Secondary

```text
Background: #FFFFFF
Texto:      #7C3AED
Borda:      #7C3AED
Hover:      #F3E8FF
```

### 14.3 Accent

Utilização pontual.

```text
Background: #FACC15
Texto:      #111827
Hover:      #EAB308
```

Não utilizar amarelo como CTA dominante em todas as páginas.

### 14.4 Danger

Apenas ações destrutivas.

```text
Background: #DC2626
Texto:      #FFFFFF
```

### 14.5 Grupo de ações

Dentro do mesmo grupo:

- somente uma ação deve ser visualmente dominante;
- ações secundárias devem ter menor peso;
- evitar vários botões com cores fortes lado a lado.

Exemplo:

```text
[ Salvar ]   [ Cancelar ]
   roxo        neutro
```

---

## 15. Cards

Card padrão:

```text
Background: #FFFFFF
Border:     #E5E7EB
Radius:     16px
Shadow:     Medium
Padding:    24px
```

Hover quando o card for clicável:

```css
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(17, 24, 39, 0.10);
```

Cards não clicáveis não devem receber efeitos que indiquem interação.

---

## 16. Formulários

### 16.1 Input normal

```text
Background: #FFFFFF
Border:     #D1D5DB
Texto:      #111827
Radius:     10px
Altura:     44px
```

### 16.2 Focus

```text
Border: #7C3AED
```

```css
box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12);
```

### 16.3 Placeholder

```text
#9CA3AF
```

### 16.4 Erro

```text
Border: #DC2626
Texto auxiliar: #DC2626
```

Labels devem permanecer visíveis.

Não utilizar placeholder como substituto de label.

---

## 17. Links

```text
Normal: #7C3AED
Hover:  #6D28D9
```

Em textos editoriais, links devem possuir indicação visual suficiente.

Preferencialmente:

```text
cor + underline no hover
```

Links nunca devem depender exclusivamente de uma pequena variação de cor.

---

## 18. Badges

### 18.1 Brand

```text
Background: #F3E8FF
Texto:      #6D28D9
```

### 18.2 Accent

```text
Background: #FEF9C3
Texto:      #854D0E
```

### 18.3 Success

```text
Background: #DCFCE7
Texto:      #166534
```

### 18.4 Danger

```text
Background: #FEE2E2
Texto:      #991B1B
```

---

## 19. Ícones

Padrão recomendado:

**Lucide Icons**

Características:

- outline;
- simples;
- espessura consistente;
- boa legibilidade;
- visual moderno.

Não misturar diferentes bibliotecas de ícones em uma mesma experiência sem necessidade.

Evitar utilizar emojis como substitutos de ícones funcionais.

---

## 20. Fundos

### 20.1 Base

```text
#FFFFFF
```

### 20.2 Alternativo

```text
#F8FAFC
```

### 20.3 Brand Soft

```text
#F3E8FF
```

### 20.4 Dark Institutional

```text
#111827
```

Páginas devem alternar fundos com propósito de criar hierarquia visual.

Evitar excesso de caixas independentes.

---

## 21. Gradiente institucional

Pode ser utilizado em:

- Hero;
- banners;
- CTA institucional;
- elementos promocionais.

Padrão:

```css
background: linear-gradient(
  135deg,
  #7C3AED 0%,
  #9333EA 55%,
  #FACC15 140%
);
```

O amarelo deve funcionar como destaque.

Não utilizar divisões visuais 50% roxo / 50% amarelo.

---

## 22. Imagens

A direção visual da KoddaHub deve priorizar:

- mulheres trabalhando com tecnologia;
- profissionais em situações reais;
- dashboards;
- dados;
- automação;
- programação;
- telas;
- colaboração;
- empresas;
- processos;
- inteligência comercial.

### 22.1 Estilo

Preferir:

```text
moderno
profissional
natural
tecnológico
humano
limpo
editorial
```

Evitar:

```text
hacker com capuz
códigos verdes genéricos
robôs humanoides genéricos
imagens extremamente futuristas
visual artificial excessivo
bancos de imagem muito óbvios
```

Quando houver pessoas em imagens institucionais da KoddaHub, priorizar representação feminina sempre que fizer sentido para o contexto.

---

## 23. Blog

As capas do Blog KoddaHub devem possuir:

```text
Proporção: 16:9
Resolução padrão: 1672 × 941 px
Formato final: WebP
```

A linguagem visual deve ser consistente entre os artigos.

Priorizar:

- mulher como personagem quando houver pessoa;
- contexto relacionado ao tema;
- telas, notebooks ou dashboards quando fizer sentido;
- paleta compatível com KoddaHub;
- composição moderna;
- leitura clara em miniaturas.

Evitar texto excessivo dentro da imagem.

---

## 24. Navbar

A navbar deve:

- utilizar o logo oficial;
- possuir hierarquia simples;
- destacar apenas um CTA;
- manter navegação legível;
- funcionar completamente em mobile;
- manter área de toque adequada;
- oferecer indicação clara de item ativo.

Recomendação visual:

```text
Background: #FFFFFF
Border bottom: #E5E7EB
Altura desktop: 72px a 80px
```

O CTA principal deve utilizar o roxo institucional.

---

## 25. Hero

O Hero deve comunicar rapidamente:

1. o que a KoddaHub faz;
2. para quem;
3. qual problema resolve;
4. qual é a principal ação disponível.

Estrutura recomendada:

```text
Eyebrow opcional
Título principal
Descrição curta
CTA principal
CTA secundário opcional
Imagem ou visual contextual
```

Evitar:

- mais de dois CTAs concorrentes;
- textos longos;
- frases genéricas sem proposta de valor;
- elementos decorativos que prejudiquem a leitura.

---

## 26. Seções de serviços

Cards de serviços devem:

- utilizar ícone consistente;
- ter título curto;
- ter descrição objetiva;
- possuir CTA apenas quando necessário;
- manter alturas visualmente equilibradas.

Quantidade recomendada por linha:

```text
Desktop: 3
Tablet:  2
Mobile:  1
```

---

## 27. CTA institucional

Blocos de CTA devem possuir uma ação principal clara.

Pode utilizar:

- roxo sólido;
- fundo roxo suave;
- gradiente institucional.

Não utilizar vários CTAs diferentes dentro do mesmo bloco.

---

## 28. Footer

O footer deve organizar:

- marca;
- navegação;
- soluções;
- conteúdo;
- contato;
- redes sociais;
- links legais.

Recomendação:

```text
Background: #111827
Texto principal: #FFFFFF
Texto secundário: #D1D5DB
Links hover: #A78BFA
Detalhes: #FACC15
```

Evitar excesso de informações e colunas desnecessárias.

---

## 29. Tabelas

Tabelas devem priorizar legibilidade.

Regras:

- cabeçalho claramente diferenciado;
- linhas com altura confortável;
- alinhamento consistente;
- ações agrupadas;
- responsividade prevista;
- nunca depender apenas de cor para comunicar estado.

Padrão sugerido:

```text
Header background: #F8FAFC
Header text:       #374151
Border:            #E5E7EB
Body text:         #111827
```

Em mobile, avaliar:

- scroll horizontal controlado;
- cards responsivos;
- ocultação apenas de colunas realmente secundárias.

---

## 30. Modais

Usar modal quando a ação:

- for curta;
- tiver poucos campos;
- não exigir fluxo complexo;
- não precisar de URL dedicada.

Padrão:

```text
Background: #FFFFFF
Radius:     16px
Shadow:     Large
Padding:    24px
```

O modal deve conter:

- título;
- descrição opcional;
- conteúdo;
- ação principal;
- ação de cancelamento;
- fechamento acessível.

---

## 31. Feedback e estados

Toda interação relevante deve prever:

- normal;
- hover;
- focus;
- active;
- loading;
- success;
- error;
- disabled;
- empty state.

### 31.1 Loading

Evitar mudanças abruptas de layout.

Preferir:

- skeleton;
- spinner pequeno;
- label de ação em andamento.

### 31.2 Empty State

Deve explicar:

1. o que está vazio;
2. por que isso importa;
3. qual ação pode ser realizada.

### 31.3 Erro

Mensagens de erro devem:

- explicar o problema;
- indicar como corrigir quando possível;
- evitar mensagens técnicas para usuários finais.

---

## 32. Responsividade

Breakpoints de referência:

```text
Mobile:  até 575px
Small:   576px a 767px
Tablet:  768px a 991px
Desktop: 992px a 1199px
Large:   1200px ou mais
```

Esses limites podem acompanhar Bootstrap quando ele fizer parte da página.

### 32.1 Mobile First

Toda nova interface deve funcionar em mobile.

Prioridades:

- legibilidade;
- toque confortável;
- navegação simples;
- conteúdo sem overflow;
- imagens responsivas;
- CTAs visíveis;
- formulários utilizáveis.

---

## 33. Acessibilidade

A acessibilidade é requisito do Design System.

### 33.1 Contraste

Manter contraste compatível com WCAG AA sempre que aplicável.

### 33.2 Foco

Elementos interativos devem apresentar foco visível.

Padrão recomendado:

```css
outline: 2px solid #7C3AED;
outline-offset: 2px;
```

### 33.3 Área mínima de interação

Alvos de toque devem possuir área confortável.

Referência:

```text
mínimo recomendado: 44 × 44 px
```

### 33.4 HTML semântico

Priorizar elementos nativos:

```text
header
nav
main
section
article
aside
footer
button
a
form
label
```

Não substituir `button` por `div` clicável.

### 33.5 Imagens

Imagens informativas devem possuir `alt` significativo.

Imagens puramente decorativas devem utilizar `alt=""`.

---

## 34. Movimento e animação

Animações devem ajudar a compreender a interface.

Duração recomendada:

```text
Fast:   150ms
Normal: 200ms
Slow:   300ms
```

Easing recomendado:

```css
cubic-bezier(0.2, 0, 0, 1)
```

Evitar:

- animações longas;
- movimentos decorativos excessivos;
- elementos pulando continuamente;
- efeitos que prejudiquem leitura.

Respeitar `prefers-reduced-motion`.

---

## 35. Design Tokens CSS

Arquivo recomendado:

```text
/public/assets/css/design-system.css
```

Fonte de verdade dos tokens:

```css
:root {
  /* Brand */
  --kh-purple: #7C3AED;
  --kh-purple-dark: #6D28D9;
  --kh-purple-light: #A78BFA;
  --kh-purple-soft: #F3E8FF;

  --kh-yellow: #FACC15;
  --kh-yellow-dark: #EAB308;
  --kh-yellow-soft: #FEF9C3;

  /* Neutral */
  --kh-neutral-950: #111827;
  --kh-neutral-900: #171717;
  --kh-neutral-800: #1F2937;
  --kh-neutral-700: #374151;
  --kh-neutral-600: #4B5563;
  --kh-neutral-500: #6B7280;
  --kh-neutral-400: #9CA3AF;
  --kh-neutral-300: #D1D5DB;
  --kh-neutral-200: #E5E7EB;
  --kh-neutral-100: #F3F4F6;
  --kh-neutral-50: #F8FAFC;
  --kh-white: #FFFFFF;

  /* Semantic */
  --kh-success: #16A34A;
  --kh-info: #2563EB;
  --kh-warning: #F59E0B;
  --kh-danger: #DC2626;

  /* Typography */
  --kh-font-heading: "Poppins", sans-serif;
  --kh-font-body: "Inter", sans-serif;

  /* Radius */
  --kh-radius-sm: 6px;
  --kh-radius-md: 10px;
  --kh-radius-lg: 16px;
  --kh-radius-xl: 24px;
  --kh-radius-pill: 999px;

  /* Spacing */
  --kh-space-1: 4px;
  --kh-space-2: 8px;
  --kh-space-3: 12px;
  --kh-space-4: 16px;
  --kh-space-5: 20px;
  --kh-space-6: 24px;
  --kh-space-8: 32px;
  --kh-space-10: 40px;
  --kh-space-12: 48px;
  --kh-space-16: 64px;
  --kh-space-20: 80px;
  --kh-space-24: 96px;

  /* Shadows */
  --kh-shadow-sm: 0 2px 8px rgba(17, 24, 39, 0.05);
  --kh-shadow-md: 0 4px 16px rgba(17, 24, 39, 0.08);
  --kh-shadow-lg: 0 12px 32px rgba(17, 24, 39, 0.12);

  /* Layout */
  --kh-container: 1200px;
  --kh-content-width: 800px;

  /* Motion */
  --kh-transition-fast: 150ms;
  --kh-transition-normal: 200ms;
  --kh-transition-slow: 300ms;
}
```

---

## 36. Componentes CSS reutilizáveis

Componentes globais reutilizáveis devem usar prefixo `kh-`.

Exemplos:

```text
.kh-container
.kh-section
.kh-button
.kh-button-primary
.kh-button-secondary
.kh-card
.kh-badge
.kh-input
.kh-modal
.kh-empty-state
```

Evitar classes genéricas que possam conflitar com outras bibliotecas.

Exemplo inadequado:

```text
.card
.button
.title
.container-custom
```

Exemplo adequado:

```text
.kh-card
.kh-button
.kh-section-title
.kh-container
```

---

## 37. Organização dos estilos

Estrutura recomendada:

```text
public/
└── assets/
    └── css/
        ├── design-system.css
        ├── components.css
        └── pages/
```

Responsabilidades:

### `design-system.css`

Somente:

- tokens;
- tipografia base;
- utilitários institucionais;
- primitives reutilizáveis.

### `components.css`

Componentes reutilizados em múltiplas páginas.

### `pages/`

Estilos específicos de páginas.

Não colocar regras específicas de uma única página dentro do Design System.

---

## 38. Regras de implementação

### Deve

- reutilizar tokens;
- reutilizar componentes;
- manter comportamento responsivo;
- utilizar HTML semântico;
- preservar acessibilidade;
- seguir a hierarquia visual;
- manter consistência entre páginas.

### Não deve

- criar nova tonalidade de roxo sem justificativa;
- criar novo amarelo sem justificativa;
- usar valores arbitrários quando existir token;
- duplicar componentes visualmente equivalentes;
- aplicar estilos inline sem necessidade;
- editar arquivos gerados em `dist/`;
- criar páginas visualmente isoladas do restante do site.

---

## 39. Regra sobre `dist`

A pasta:

```text
/dist/
```

é artefato gerado pelo processo de build.

Não editar arquivos diretamente dentro de `dist/`.

Alterações devem ser realizadas nos arquivos fonte em:

```text
/public/
```

e posteriormente processadas pelo build oficial do projeto.

---

## 40. Hierarquia visual

Toda página deve possuir uma hierarquia reconhecível.

Ordem recomendada:

1. contexto;
2. título;
3. explicação;
4. conteúdo principal;
5. ação;
6. conteúdo complementar.

Evitar:

- muitos elementos com o mesmo peso;
- excesso de títulos grandes;
- múltiplos CTAs dominantes;
- excesso de cores fortes;
- excesso de cards.

---

## 41. Linguagem visual

A KoddaHub deve parecer:

```text
clara
moderna
tecnológica
humana
organizada
profissional
criativa
confiável
```

A KoddaHub não deve parecer:

```text
excessivamente corporativa
fria
genérica
infantil
poluída
futurista em excesso
visualmente agressiva
```

---

## 42. Regra de consistência

Antes de criar um novo padrão visual, verificar se já existe:

- componente;
- token;
- padrão de layout;
- regra de espaçamento;
- estilo equivalente.

Se já existir, reutilizar.

Novo padrão só deve ser introduzido quando resolver uma necessidade que o Design System atual não cobre.

---

## 43. Governança

Toda evolução visual deve seguir:

1. identificar a necessidade;
2. verificar componente existente;
3. aplicar o menor ajuste possível;
4. validar desktop;
5. validar mobile;
6. validar acessibilidade;
7. validar consistência com a marca;
8. atualizar este documento quando houver nova regra global.

Mudanças globais devem ser documentadas antes de serem replicadas em todo o site.

---

## 44. Checklist para novas páginas

Antes de considerar uma página concluída, validar:

- [ ] Logo oficial utilizado corretamente.
- [ ] Paleta oficial respeitada.
- [ ] Poppins nos títulos.
- [ ] Inter em textos e interface.
- [ ] Somente um CTA dominante por contexto.
- [ ] Espaçamento baseado nos tokens.
- [ ] Cards seguem o padrão.
- [ ] Inputs possuem labels.
- [ ] Focus é visível.
- [ ] Contraste foi verificado.
- [ ] Layout funciona em mobile.
- [ ] Não existe overflow horizontal.
- [ ] Imagens possuem `alt`.
- [ ] Links são identificáveis.
- [ ] Estados de hover foram previstos.
- [ ] Estados de loading foram previstos quando necessários.
- [ ] Estados de erro foram previstos.
- [ ] Empty state foi previsto quando necessário.
- [ ] Nenhum arquivo em `dist/` foi editado diretamente.
- [ ] Componentes existentes foram reutilizados sempre que possível.
- [ ] A página parece pertencer ao mesmo produto e à mesma marca.

---

## 45. Resumo oficial da identidade

### Cor líder

```text
Kodda Purple
#7C3AED
```

### Cor de destaque

```text
Kodda Yellow
#FACC15
```

### Fundo principal

```text
#FFFFFF
```

### Texto principal

```text
#111827
```

### Fonte de títulos

```text
Poppins
```

### Fonte de conteúdo

```text
Inter
```

### Radius padrão

```text
10px a 16px
```

### Linguagem

```text
Tecnologia + Clareza + Criatividade + Proximidade + Profissionalismo
```

### Princípio central

> Roxo conduz. Amarelo destaca. Neutros organizam.

---

## 46. Fonte de verdade

Este documento é a referência oficial de Design System do site KoddaHub.

Localização:

```text
/docs/design-system/KODDAHUB_DESIGN_SYSTEM.md
```

Implementação dos tokens:

```text
/public/assets/css/design-system.css
```

Arquivos de logo:

```text
/public/assets/images/logo/
```

Qualquer divergência visual entre páginas deve ser tratada como inconsistência e revisada com base neste documento.

---

**Fim do documento — KoddaHub Design System v1.0**
