package com.example.diagnosisdemo;

import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Mapping;

@Document(indexName="diagonise",type="sample")
@Mapping(mappingPath="mapping-sample.json")
public class Diagonise {
    
	
	String diag;
	String diagSuggest;
	

	public String getDiagSuggest() {
		return diagSuggest;
	}

	public void setDiagSuggest(String diagSuggest) {
		this.diagSuggest = diagSuggest;
	}
}
