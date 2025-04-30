package com.example.imdbest.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.imdbest.adapter.FilmeAdapter
import com.example.imdbest.api.TmdbApiService
import com.example.imdbest.databinding.FragmentListaFilmesBinding
import com.example.imdbest.viewmodel.FilmesViewModel
import com.example.imdbest.viewmodel.FilmesViewModelFactory

class FilmesFragment : Fragment() {

    private var _binding: FragmentListaFilmesBinding? = null
    private val binding get() = _binding!!

    private lateinit var adapter: FilmeAdapter

    private val tmdbApi = TmdbApiService.create()

    private val viewModel: FilmesViewModel by viewModels {
        FilmesViewModelFactory(tmdbApi)
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentListaFilmesBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        adapter = FilmeAdapter { filmeSelecionado ->
            viewModel.buscarDetalhesFilme(filmeSelecionado.id)
        }

        binding.rvFilmes.layoutManager = LinearLayoutManager(requireContext())
        binding.rvFilmes.adapter = adapter

        binding.searchView.setOnQueryTextListener(object : androidx.appcompat.widget.SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String?): Boolean {
                if (!query.isNullOrBlank()) {
                    viewModel.buscarFilmes(query)
                } else {
                    Toast.makeText(requireContext(), "Digite um nome para buscar", Toast.LENGTH_SHORT).show()
                }
                return true
            }
            override fun onQueryTextChange(newText: String?): Boolean = false
        })

        viewModel.filmes.observe(viewLifecycleOwner) { filmes ->
            adapter.submitList(filmes)
        }

        viewModel.filmeDetalhado.observe(viewLifecycleOwner) { detalhes ->
            detalhes?.let {
                val action = FilmesFragmentDirections.actionFilmesFragmentToDetalheFragment(
                    titulo = it.title,
                    ano = it.release_date ?: "Ano não disponível",
                    poster = it.poster_path?.let { path -> "https://image.tmdb.org/t/p/w500$path" } ?: "",
                    descricao = it.overview ?: "Sem descrição",
                    nota = "", // Pode adicionar rating se desejar
                    genero = "", // Pode adicionar genres se desejar
                    classificacao = "" // Pode buscar release_dates se desejar
                )
                findNavController().navigate(action)
                viewModel.limparFilmeDetalhado()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
