package com.example.diagnosissearch;

import java.io.IOException;

import org.apache.http.HttpHost;
import org.apache.http.util.EntityUtils;
import org.elasticsearch.client.Request;
import org.elasticsearch.client.Response;
import org.elasticsearch.client.RestClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RestClientConfig {
    
	@Autowired
	RestClientConfig restClientConfig;
	
	//This method returns the query to be searched in elasticsearch
	private String getSearchQuery(String find) {
		
		StringBuilder query=new StringBuilder();
		
		query.append("{\"query\":{\"match\":{\"specificDiagnosis\":{\"query\":\"");
		query.append(find);
		query.append("\",\"operator\":\"and\"}}}}");
		
		return query.toString();
		
	}
	
	
	public String fetchFromElasticSearch(String find) throws IOException {
		
		//connect to elasticsearch using restclient
		RestClient restClient = RestClient.builder(new HttpHost("192.168.1.109", 9200, "http")).build();
		
		//configure request method and url
		Request request = new Request("GET","/diagnosis/diagnosis_type/_search");
				
		String query=restClientConfig.getSearchQuery(find);
		
		request.setJsonEntity(query);	
		
		Response response = restClient.performRequest(request);
		return EntityUtils.toString(response.getEntity()); 
		
	}
}
