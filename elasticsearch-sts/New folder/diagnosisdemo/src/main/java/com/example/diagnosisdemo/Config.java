package com.example.diagnosisdemo;

import java.net.InetAddress;
import java.net.UnknownHostException;

import org.elasticsearch.client.Client;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.TransportAddress;
import org.elasticsearch.transport.client.PreBuiltTransportClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.ElasticsearchTemplate;

@Configuration
public class Config {

	@Value("${elasticsearch.home:/usr/share/elasticsearch}")
	private String elasticsearchHome;

	/*
	 * @Value("${elasticsearch.cluster.name:elasticsearch}") private String
	 * clusterName;---used if cluster name is not elasticsearch
	 */

	@Bean
	public Client client() throws UnknownHostException {
		Settings elasticsearchSettings = Settings.builder().put("client.transport.sniff", true)
				.put("path.home", elasticsearchHome).build();
		TransportClient client = new PreBuiltTransportClient(elasticsearchSettings);
		client.addTransportAddresses(new TransportAddress(InetAddress.getByName("192.168.1.109"), 9300));
		return client;
	}

	@Bean
	public ElasticsearchOperations elasticsearchTemplate() throws UnknownHostException {
		return new ElasticsearchTemplate(client());
	}

}
