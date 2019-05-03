package com.example.elasticsearchindex;

import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HighRestClientConfig {
	
	/*@Bean
	public RestHighLevelClient client() {
		return  new RestHighLevelClient(RestClient.builder(new HttpHost("192.168.1.109", 9200, "http")));
	}
	 */
	
	@Bean
	public RestClient client() {
		return  RestClient.builder(new HttpHost("192.168.1.109", 9200, "http")).build();
	}

}
