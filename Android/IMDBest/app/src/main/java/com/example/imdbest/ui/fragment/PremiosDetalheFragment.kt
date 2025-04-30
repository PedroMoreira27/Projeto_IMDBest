package com.example.imdbest.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.imdbest.databinding.FragmentPremiosDetalheBinding

class PremiosDetalheFragment : Fragment() {

    private var _binding: FragmentPremiosDetalheBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentPremiosDetalheBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val args = PremiosDetalheFragmentArgs.fromBundle(requireArguments())
        binding.txtTitulo.text = args.titulo
        binding.txtPremios.text = args.premios
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
