// lib/viewmodels/filmes_viewmodel.dart
import 'package:flutter/material.dart';
import '../models/filme.dart'; // Use apenas este model!
import '../services/api_service.dart';

class FilmesViewModel extends ChangeNotifier {
  List<Filme> filmes = [];

  void carregarFilmes() {
    // Aqui você buscaria da API ou banco local
    filmes = [
      Filme(titulo: 'Oppenheimer', ano: '2023'),
      Filme(titulo: 'Barbie', ano: '2023'),
    ];
    notifyListeners();
  }
}

class FilmesScreen extends StatefulWidget {
  const FilmesScreen({super.key});

  @override
  State<FilmesScreen> createState() => _FilmesScreenState();
}

class _FilmesScreenState extends State<FilmesScreen> {
  List<Filme> filmes = [];
  String busca = '';
  bool carregando = true;

  @override
  void initState() {
    super.initState();
    buscarFilmes();
  }

  Future<void> buscarFilmes() async {
    final api = ApiService();
    final resultado = await api.buscarFilmesTmdb();
    setState(() {
      filmes = resultado;
      carregando = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final filmesFiltrados = filmes
        .where((f) => f.titulo.toLowerCase().contains(busca.toLowerCase()))
        .toList();

    if (carregando) {
      return const Center(child: CircularProgressIndicator());
    }

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: TextField(
            decoration: const InputDecoration(
              labelText: 'Buscar filme...',
              prefixIcon: Icon(Icons.search),
              border: OutlineInputBorder(),
            ),
            onChanged: (valor) {
              setState(() {
                busca = valor;
              });
            },
          ),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: filmesFiltrados.length,
            itemBuilder: (context, index) {
              final filme = filmesFiltrados[index];
              return ListTile(
                leading: filme.posterUrl != null
                    ? Image.network(filme.posterUrl!)
                    : null,
                title: Text(filme.titulo),
                subtitle: Text(filme.ano),
                onTap: () {
                  Navigator.pushNamed(
                    context,
                    '/detalhes',
                    arguments: filme,
                  );
                },
              );
            },
          ),
        ),
      ],
    );
  }
}