const test = require('node:test');
const assert = require('node:assert/strict');
const { reply } = require('../public/assets/js/chat-fallback.js');

test('indica o guia de n8n para a pergunta que falhava no chat', () => {
  const answer = reply('Dúvidas de n8n');
  assert.match(answer.text, /entrada, as regras/);
  assert.equal(answer.link.href, '/blog/n8n-na-pratica-quando-faz-sentido-automatizar-um-processo-com-a-ferramenta/');
});

test('reconhece assunto com ou sem acento e oferece saída humana para tema desconhecido', () => {
  assert.match(reply('automação de processos').link.href, /n8n-na-pratica/);
  assert.match(reply('Site no celular').link.href, /site-responsivo/);
  assert.match(reply('assunto fora do blog').text, /WhatsApp/);
});
