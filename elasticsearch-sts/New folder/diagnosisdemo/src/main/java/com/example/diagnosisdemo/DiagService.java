package com.example.diagnosisdemo;

public interface DiagService {

	Iterable<Diagonise> searchField();

	Diagonise createIndex(Diagonise diagno);

}
