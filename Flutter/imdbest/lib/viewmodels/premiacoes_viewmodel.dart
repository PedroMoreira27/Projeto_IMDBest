// lib/viewmodels/premiacoes_viewmodel.dart
import 'package:flutter/material.dart';

class Premiacao {
  final String nome;
  final String ano;
  Premiacao({required this.nome, required this.ano});
}

class PremiacoesViewModel extends ChangeNotifier {
  List<Premiacao> premiacoes = [];

  void carregarPremiacoes() {
    premiacoes = [
      Premiacao(nome: 'Oscar', ano: '2023'),
      Premiacao(nome: 'Globo de Ouro', ano: '2023'),
    ];
    notifyListeners();
  }
}