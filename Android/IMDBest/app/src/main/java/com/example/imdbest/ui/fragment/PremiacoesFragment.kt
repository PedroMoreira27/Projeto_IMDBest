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
import com.example.imdbest.api.OmdbApi
import com.example.imdbest.api.TmdbApiService
import com.example.imdbest.databinding.FragmentPremiacoesBinding
import com.example.imdbest.viewmodel.PremiacoesViewModel
import com.example.imdbest.viewmodel.PremiacoesViewModelFactory

class PremiacoesFragment : Fragment() {

    private var _binding: FragmentPremiacoesBinding? = null
    private val binding get() = _binding!!

    private lateinit var adapter: FilmeAdapter

    private val tmdbApi = TmdbApiService.create()
    private val omdbApi = OmdbApi.create()

    private val viewModel: PremiacoesViewModel by viewModels {
        PremiacoesViewModelFactory(tmdbApi, omdbApi)
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentPremiacoesBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        adapter = FilmeAdapter { filmeSelecionado ->
            viewModel.buscarDetalhesFilme(filmeSelecionado.id)
        }

        binding.recyclerFilmes.layoutManager = LinearLayoutManager(requireContext())
        binding.recyclerFilmes.adapter = adapter

        binding.btnBuscar.setOnClickListener {
            val nome = binding.editNomeFilme.text.toString()
            if (nome.isNotBlank()) {
                viewModel.buscarFilmes(nome)
            } else {
                Toast.makeText(requireContext(), "Digite um nome para buscar", Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.filmes.observe(viewLifecycleOwner) { filmes ->
            adapter.submitList(filmes)
        }

        // Correção: pegar imdbID após obter detalhes
        viewModel.filmeDetalhado.observe(viewLifecycleOwner) { event ->
            event.getContentIfNotHandled()?.let { detalhes ->
                detalhes.imdb_id?.let { imdbId ->
                    viewModel.buscarPremios(imdbId)
                } ?: run {
                    Toast.makeText(requireContext(), "IMDb ID não encontrado para esse filme.", Toast.LENGTH_SHORT).show()
                }
            }
        }

        viewModel.premios.observe(viewLifecycleOwner) { premios ->
            val action = PremiacoesFragmentDirections.actionNavPremiacoesToNavPremiosDetalhe(
                titulo = "Premiações",
                premios = premios
            )
            findNavController().navigate(action)
            viewModel.limparPremios() // ✅ LIMPA os prêmios depois de navegar!
        }

    }
}
