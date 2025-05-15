import 'package:flutter/material.dart';
import '../models/filme.dart';
import '../services/api_service.dart';

class DetalhesScreen extends StatefulWidget {
  @override
  State<DetalhesScreen> createState() => _DetalhesScreenState();
}

class _DetalhesScreenState extends State<DetalhesScreen> {
  Filme? detalhes;
  bool carregando = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final Filme filme = ModalRoute.of(context)!.settings.arguments as Filme;
    _carregarDetalhes(filme);
  }

  Future<void> _carregarDetalhes(Filme filme) async {
    if (filme.imdbId != null) {
      final api = ApiService();
      final detalhesOmdb = await api.buscarFilmeOmdb(filme.imdbId!);
      setState(() {
        detalhes = detalhesOmdb;
        carregando = false;
      });
    } else {
      setState(() {
        detalhes = filme;
        carregando = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (carregando || detalhes == null) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    final filme = detalhes!;
    return Scaffold(
      appBar: AppBar(
        title: Text(filme.titulo),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
        elevation: 2,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Card(
              elevation: 6,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: filme.posterUrl != null
                    ? Image.network(filme.posterUrl!, height: 350, fit: BoxFit.cover)
                    : Container(
                        height: 350,
                        color: Colors.grey[300],
                        child: const Icon(Icons.movie, size: 100),
                      ),
              ),
            ),
            const SizedBox(height: 20),
            Text(
              filme.titulo,
              style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Chip(
                  label: Text('Ano: ${filme.ano}'),
                  backgroundColor: Colors.deepPurple.shade50,
                ),
                const SizedBox(width: 8),
                Chip(
                  avatar: const Icon(Icons.star, color: Colors.amber, size: 18),
                  label: Text('IMDB: ${filme.notaImdb ?? "N/A"}'),
                  backgroundColor: Colors.yellow.shade50,
                ),
                const SizedBox(width: 8),
                if (filme.rottenTomatoes != null)
                  Chip(
                    avatar: CircleAvatar(
                      backgroundColor: Colors.transparent,
                      child: Image.asset(
                        'assets/images/rotten_tomatoes.png',
                        width: 18,
                        height: 18,
                        fit: BoxFit.contain,
                      ),
                    ),
                    label: Text('Rotten: ${filme.rottenTomatoes}'),
                    backgroundColor: Colors.green.shade50,
                  ),
              ],
            ),
            const SizedBox(height: 16),
            Divider(thickness: 1.2),
            if (filme.genero != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  children: [
                    const Icon(Icons.category, color: Colors.deepPurple),
                    const SizedBox(width: 8),
                    Expanded(child: Text('Gênero: ${filme.genero}', style: TextStyle(fontSize: 16))),
                  ],
                ),
              ),
            if (filme.diretor != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  children: [
                    const Icon(Icons.person, color: Colors.deepPurple),
                    const SizedBox(width: 8),
                    Expanded(child: Text('Diretor: ${filme.diretor}', style: TextStyle(fontSize: 16))),
                  ],
                ),
              ),
            if (filme.elenco != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.people, color: Colors.deepPurple),
                    const SizedBox(width: 8),
                    Expanded(child: Text('Elenco: ${filme.elenco}', style: TextStyle(fontSize: 16))),
                  ],
                ),
              ),
            const SizedBox(height: 16),
            Divider(thickness: 1.2),
            if (filme.sinopse != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Text(
                  filme.sinopse!,
                  style: const TextStyle(fontSize: 16, fontStyle: FontStyle.italic),
                  textAlign: TextAlign.justify,
                ),
              ),
          ],
        ),
      ),
    );
  }
}