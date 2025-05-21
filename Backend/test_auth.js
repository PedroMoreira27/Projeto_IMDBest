const axios = require('axios');

const BASE_URL = 'http://127.0.0.1:5000'; // Porta correta do servidor

// Função para gerar email único
function gerarEmailUnico() {
  const timestamp = new Date().getTime();
  return `teste${timestamp}@exemplo.com`;
}

// Credenciais de teste
const TEST_USER = {
  nome: 'Teste Usuario',
  email: gerarEmailUnico(),
  senha: 'senha123',
  confirmarSenha: 'senha123',
};

// Função para esperar um tempo
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function testRegistro() {
  console.log('\nTestando endpoint /registrar:');
  try {
    console.log('Dados do registro:', { ...TEST_USER, senha: '******' });
    const response = await axios.post(`${BASE_URL}/auth/registrar`, TEST_USER);
    console.log('Status:', response.status);
    console.log('Resposta:');
    console.log(JSON.stringify(response.data, null, 2));
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Erro ao testar /registrar:', error.response.data);
    } else {
      console.error('Erro ao testar /registrar:', error.message);
    }
    return null;
  }
}

async function testLogin() {
  console.log('\nTestando endpoint /login:');
  try {
    const data = {
      email: TEST_USER.email,
      senha: TEST_USER.senha,
    };

    console.log('Dados do login:', { ...data, senha: '******' });
    const response = await axios.post(`${BASE_URL}/auth/login`, data);
    console.log('Status:', response.status);
    console.log('Resposta:');
    console.log(JSON.stringify(response.data, null, 2));
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Erro ao testar /login:', error.response.data);
    } else {
      console.error('Erro ao testar /login:', error.message);
    }
    return null;
  }
}

async function testLoginInvalido() {
  console.log('\nTestando login com credenciais inválidas:');
  try {
    const data = {
      email: TEST_USER.email,
      senha: 'senha_errada',
    };

    console.log('Dados do login inválido:', { ...data, senha: '******' });
    const response = await axios.post(`${BASE_URL}/auth/login`, data);
    console.log('Status:', response.status);
    console.log('Resposta:');
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    if (error.response) {
      console.error('Erro ao testar login inválido:', error.response.data);
    } else {
      console.error('Erro ao testar login inválido:', error.message);
    }
  }
}

async function runTests() {
  console.log('Iniciando testes de autenticação...');

  // Testa registro
  const registroResult = await testRegistro();

  if (registroResult) {
    // Testa login
    await testLogin();
  }

  // Testa login com credenciais inválidas
  await testLoginInvalido();
}

runTests().catch(console.error);
