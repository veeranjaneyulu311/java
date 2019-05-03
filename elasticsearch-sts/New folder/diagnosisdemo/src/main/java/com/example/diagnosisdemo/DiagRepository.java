package com.example.diagnosisdemo;

import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DiagRepository extends ElasticsearchRepository<Diagonise, String>{

}
