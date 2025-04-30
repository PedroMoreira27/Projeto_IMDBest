package com.example.imdbest.model

data class FilmeBuscaTmdbResponse(
    val results: List<FilmeTmdb>
)

data class FilmeTmdb(
    val id: Int,
    val title: String,
    val release_date: String?,
    val poster_path: String?
)
