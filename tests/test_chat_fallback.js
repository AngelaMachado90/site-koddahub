const test = require('node:test');
const assert = require('node:assert/strict');
const { reply, createConversation } = require('../public/assets/js/chat-fallback.js');

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
  assert.match(reply('assunto fora do blog').text, /WhatsApp/);
});
