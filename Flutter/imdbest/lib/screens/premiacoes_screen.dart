import 'package:flutter/material.dart';

class PremiacoesScreen extends StatelessWidget {
  const PremiacoesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Exemplo de lista de premiações mock
    final premiacoes = [
      {'premio': 'Oscar', 'ano': '2023'},
      {'premio': 'Globo de Ouro', 'ano': '2023'},
    ];

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: premiacoes.length,
      itemBuilder: (context, index) {
        final premio = premiacoes[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: Icon(Icons.emoji_events),
            title: Text(premio['premio']!),
            subtitle: Text('Ano: ${premio['ano']}'),
            onTap: () {
              // Navegar para detalhes da premiação
            },
          ),
        );
      },
    );
  }
}