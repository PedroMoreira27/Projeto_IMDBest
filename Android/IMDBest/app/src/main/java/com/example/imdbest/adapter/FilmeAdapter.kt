package com.example.imdbest.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.imdbest.R
import com.example.imdbest.model.FilmeTmdb

class FilmeAdapter(
    private val onItemClick: (FilmeTmdb) -> Unit
) : RecyclerView.Adapter<FilmeAdapter.FilmeViewHolder>() {

    private var filmes: List<FilmeTmdb> = emptyList()

    fun submitList(lista: List<FilmeTmdb>) {
        filmes = lista
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): FilmeViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_filme, parent, false)
        return FilmeViewHolder(view)
    }

    override fun onBindViewHolder(holder: FilmeViewHolder, position: Int) {
        holder.bind(filmes[position])
        holder.itemView.setOnClickListener {
            onItemClick(filmes[position])
        }
    }

    override fun getItemCount() = filmes.size

    class FilmeViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val titulo: TextView = itemView.findViewById(R.id.tvTitulo)
        private val ano: TextView = itemView.findViewById(R.id.tvAno)
        private val poster: ImageView = itemView.findViewById(R.id.ivPoster)

        fun bind(filme: FilmeTmdb) {
            titulo.text = filme.title
            ano.text = filme.release_date ?: "Ano não informado"

            val posterUrl = filme.poster_path?.let {
                "https://image.tmdb.org/t/p/w500$it"
            }

            if (posterUrl != null) {
                Glide.with(itemView.context)
                    .load(posterUrl)
                    .into(poster)
            } else {
                poster.setImageResource(R.drawable.ic_no_image) // Imagem padrão se não tiver poster
            }
        }
    }
}
