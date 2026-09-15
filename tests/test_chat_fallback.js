const test = require('node:test');
const assert = require('node:assert/strict');
const { reply, createConversation } = require('../public/assets/js/chat-fallback.js');

const context = {
  page_type: 'blog',
  article_slug: 'dado-metrica-e-kpi-diferencas-que-ajudam-a-decidir-melhor',
  glossary: [
    { term: 'Dado', aliases: ['dados'], definition: 'Informação registrada.', example: '30 pedidos.', application: 'Serve para analisar.', related: ['Métrica', 'KPI'] },
    { term: 'Dado quantitativo', aliases: ['quantitativo'], definition: 'Informação representada por quantidade.', example: 'R$ 1.200 em vendas.', application: 'Pode ser calculado.', related: ['Dado'] },
    { term: 'Dado qualitativo', aliases: ['qualitativo'], definition: 'Informação que descreve uma categoria.', example: 'Canal WhatsApp.', application: 'Serve para agrupar.', related: ['Dado'] },
    { term: 'Métrica', aliases: ['metrica'], definition: 'Medida criada a partir de dados.', example: 'Pedidos na semana.', application: 'Serve para acompanhar.', related: ['Dado', 'KPI'] },
    { term: 'KPI', aliases: [], definition: 'Métrica ligada a um objetivo.', example: 'Taxa de conversão.', application: 'Serve para acompanhar um objetivo.', related: ['Dado', 'Métrica'] }
  ]
};

test('indica o guia de n8n para a pergunta que falhava no chat', () => {
  const answer = reply('Dúvidas de n8n');
  assert.match(answer.text, /entrada, as regras/);
  assert.equal(answer.link.href, '/blog/n8n-na-pratica-quando-faz-sentido-automatizar-um-processo-com-a-ferramenta/');
});

test('coleta contato em etapas e só prepara o envio pelo WhatsApp', () => {
  const chat = createConversation();
  chat.reply('Dúvidas de n8n');
  assert.match(chat.reply('quero implementar isto na minha empresa').text, /Qual é seu nome/);
  assert.match(chat.reply('Ana Silva').text, /telefone com DDD/);
  assert.match(chat.reply('123').text, /10 ou 11 dígitos/);
  assert.match(chat.reply('(41) 99999-9999').text, /e-mail/);
  assert.match(chat.reply('email inválido').text, /Confira o e-mail/);
  const answer = chat.reply('ana@empresa.com.br');
  assert.equal(answer.lead, true);
  assert.match(answer.link.href, /^https:\/\/wa\.me\/5541992272854\?text=/);
  const message = decodeURIComponent(answer.link.href.split('text=')[1]);
  assert.match(message, /n8n/);
  assert.match(message, /Ana Silva/);
  assert.match(message, /41999999999/);
  assert.match(message, /ana@empresa.com.br/);
});

test('reconhece assunto com ou sem acento e oferece saída humana para tema desconhecido', () => {
  assert.match(reply('automação de processos').link.href, /n8n-na-pratica/);
  assert.match(reply('Site no celular').link.href, /site-responsivo/);
  assert.match(reply('assunto fora do blog').text, /Não encontrei/);
});

test('explica termos do glossário do artigo antes de sugerir conteúdo', () => {
  for (const [question, term] of [['Dado', 'Dado'], ['O que é dado quantitativo?', 'Dado quantitativo'], ['Dado qualitativo', 'Dado qualitativo'], ['Métrica', 'Métrica'], ['KPI', 'KPI']]) {
    const answer = createConversation(context).reply(question);
    assert.equal(answer.kind, 'glossary');
    assert.equal(answer.intent, 'GLOSSARY');
    assert.equal(answer.term, term);
    assert.ok(answer.text.length < 180);
    assert.ok(answer.example);
    assert.ok(answer.application);
  }
});

test('compara conceitos, aprofunda sob demanda e usa fallback contextual seguro', () => {
  const chat = createConversation(context);
  assert.equal(chat.reply('Qual a diferença entre dado e métrica?').intent, 'ARTICLE_QUESTION');
  assert.equal(chat.reply('Qual a diferença entre métrica e KPI?').kind, 'comparison');
  assert.match(chat.reply('Zero é dado ausente?').text, /Não/);
  chat.reply('KPI');
  assert.equal(chat.reply('Explique mais').expanded, true);
  assert.match(chat.reply('kindly').text, /conteúdo que você está lendo/);
});

test('intenção comercial vem depois do contexto e prepara CTA com consentimento', () => {
  const chat = createConversation(context);
  chat.reply('KPI');
  const answer = chat.reply('Quero usar isso na minha empresa');
  assert.equal(answer.lead, true);
  assert.equal(answer.intent, 'COMMERCIAL_INTENT');
  assert.match(answer.text, /nome, telefone e e-mail/);
  assert.match(answer.text, /Qual é seu nome/);
});
