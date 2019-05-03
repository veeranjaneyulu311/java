package com.example.elasticsearchindex;

import java.io.IOException;
import java.util.List;
import org.elasticsearch.client.Request;
import org.elasticsearch.client.Response;
import org.elasticsearch.client.RestClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class ElasticSearchIndex {

	@Autowired
	ElasticSearchIndex ela;

	/*
	 * @Autowired RestHighLevelClient client;
	 */

	@Autowired
	RestClient client;

	@Autowired
	DiagnosisData diagnosisData;

	// created with high rest client
	/*
	 * private void createIndex(List<String> diagnosis) throws IOException {
	 * 
	 * IndexRequest request = new IndexRequest("diagnosis", "diagnose", "1")
	 * .source("diagnosis_suggest", diagnosis);
	 * 
	 * IndexResponse indexResponse = client.index(request, RequestOptions.DEFAULT);
	 * 
	 * 
	 * }
	 */

	private void createIndex() throws IOException {
        
		
		String indexSettings="{\"settings\":{\"analysis\":{\"filter\":{\"diagnosis_filter\":{\"type\":\"ngram\",\"min_gram\":3,\"max_gram\":3}},\"analyzer\":{\"diagnosis_trigram\":{\"type\":\"custom\",\"tokenizer\":\"standard\",\"filter\":[\"lowercase\",\"diagnosis_filter\"]}}}},\"mappings\":{\"diagnosis_type\":{\"properties\":{\"specificDiagnosis\":{\"type\":\"text\",\"analyzer\":\"diagnosis_trigram\"}}}}}";
		
		Request request = new Request("PUT", "/diagnosis");
		
		request.setJsonEntity(indexSettings);
		
		Response response = client.performRequest(request);

	}
	
private void indexData(String data) throws IOException {
        
		
				
		Request request = new Request("POST", "/diagnosis/diagnosis_type/_bulk");
		
		request.setJsonEntity(data);
		
		Response response = client.performRequest(request);

	}

	

	public void getDiagnosis() throws IOException {
		
		
		List<Diagnosis> diagnosis = diagnosisData.fetchDiagnosis();
		StringBuilder sb=new StringBuilder();
		
		//java object to json conversion jakson
		ObjectMapper mapper = new ObjectMapper();
		
		for (Diagnosis diag : diagnosis) {
			sb.append("{ \"index\" : {}}\n");		
			sb.append(mapper.writeValueAsString(diag));
		    sb.append("\n");
		}
		
		//sb.deleteCharAt(sb.length()-1);
		System.out.println(sb);
		
		ela.createIndex();
		ela.indexData(sb.toString());
	}
	
	
	

}
