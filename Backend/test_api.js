const axios = require('axios');

const BASE_URL = 'http://127.0.0.1:8000';

async function testPredict() {
  console.log('\nTestando endpoint /predict:');
  try {
    const data = {
      title: 'Mickey 17',
      year: 2025,
      categorias: [
        'oscar_nominated',
        'oscar_winner',
        'globe_nominated',
        'globe_winner',
      ],
    };

    const response = await axios.post(`${BASE_URL}/predict`, data);
    console.log('Status:', response.status);
    console.log('Resposta:');
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error(
      'Erro ao testar /predict:',
      error.response?.data || error.message,
    );
  }
}

async function testTop10() {
  console.log('\nTestando endpoint /top10 para cada categoria:');
  const categorias = [
    'oscar_nominated',
    'oscar_winner',
    'globe_nominated',
    'globe_winner',
  ];

  for (const categoria of categorias) {
    console.log(`\nTop 10 para ${categoria}:`);
    try {
      const response = await axios.get(
        `${BASE_URL}/top10?categoria=${categoria}`,
      );
      console.log('Status:', response.status);
      console.log('Resposta:');
      console.log(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error(
        `Erro ao testar /top10 para ${categoria}:`,
        error.response?.data || error.message,
      );
    }
  }
}

async function runTests() {
  console.log('Iniciando testes da API...');
  await testPredict();
  await testTop10();
}

runTests().catch(console.error);
