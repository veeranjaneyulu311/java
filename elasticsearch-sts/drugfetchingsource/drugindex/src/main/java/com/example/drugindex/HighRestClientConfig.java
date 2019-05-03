package com.example.drugindex;

import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HighRestClientConfig {
		
	@Bean
	public RestClient client() {
		return  RestClient.builder(new HttpHost("192.168.1.109", 9200, "http")).build();
	}
//done
}
