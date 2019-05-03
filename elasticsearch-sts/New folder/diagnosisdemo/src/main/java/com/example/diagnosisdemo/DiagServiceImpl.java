package com.example.diagnosisdemo;

import org.elasticsearch.index.query.QueryBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DiagServiceImpl implements DiagService{
	
	@Autowired
	DiagRepository diagRepo;
	
	QueryBuilder query;

	@Override
	public Iterable<Diagonise> searchField() {
		// TODO Auto-generated method stub
		return diagRepo.search(query);
	}

	@Override
	public Diagonise createIndex(Diagonise diagno) {
		// TODO Auto-generated method stub
		return null;
	}

}
