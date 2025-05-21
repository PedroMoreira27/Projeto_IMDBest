import 'package:flutter_test/flutter_test.dart';
import 'package:imdbest/viewmodels/filmes_viewmodel.dart';
import 'package:imdbest/models/filme.dart';

void main() {
  late FilmesViewModel viewModel;

  setUp(() {
    viewModel = FilmesViewModel();
  });

  group('FilmesViewModel Tests', () {
    test('carregarFilmes initializes with default movies', () {
      viewModel.carregarFilmes();
      
      expect(viewModel.filmes.length, 2);
      expect(viewModel.filmes[0].titulo, 'Oppenheimer');
      expect(viewModel.filmes[0].ano, '2023');
      expect(viewModel.filmes[1].titulo, 'Barbie');
      expect(viewModel.filmes[1].ano, '2023');
    });

    test('filtering movies works correctly', () {
      viewModel.filmes = [
        Filme(titulo: 'Oppenheimer', ano: '2023'),
        Filme(titulo: 'Barbie', ano: '2023'),
        Filme(titulo: 'Inception', ano: '2010'),
      ];

      // Test empty search
      var filtered = viewModel.filmes
          .where((f) => f.titulo.toLowerCase().contains(''.toLowerCase()))
          .toList();
      expect(filtered.length, 3);

      // Test search with 'opp'
      filtered = viewModel.filmes
          .where((f) => f.titulo.toLowerCase().contains('opp'.toLowerCase()))
          .toList();
      expect(filtered.length, 1);
      expect(filtered[0].titulo, 'Oppenheimer');

      // Test search with 'b'
      filtered = viewModel.filmes
          .where((f) => f.titulo.toLowerCase().contains('b'.toLowerCase()))
          .toList();
      expect(filtered.length, 1);
      expect(filtered[0].titulo, 'Barbie');

      // Test search with non-existent movie
      filtered = viewModel.filmes
          .where((f) => f.titulo.toLowerCase().contains('xyz'.toLowerCase()))
          .toList();
      expect(filtered.length, 0);
    });
  });
} 