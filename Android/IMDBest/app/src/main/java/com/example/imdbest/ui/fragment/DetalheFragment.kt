package com.example.imdbest.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.imdbest.databinding.FragmentDetalheBinding

class DetalheFragment : Fragment() {

    private var _binding: FragmentDetalheBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentDetalheBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val args = DetalheFragmentArgs.fromBundle(requireArguments())
        binding.tvTitulo.text = args.titulo
        binding.tvAno.text = args.ano
        binding.tvDescricao.text = args.descricao

        Glide.with(this)
            .load(args.poster)
            .into(binding.ivPoster)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
