package com.drucare.elasticsearch;

import javax.sql.DataSource;

import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ElasticsearchApplication {

	@Autowired
	private DataSource dataSource;
	
	public static void main(String[] args) {
		SpringApplication.run(ElasticsearchApplication.class, args);
	}
	
	//elastic search rest client configuration for fetching data
	@Bean
	public RestClient client() {
		return  RestClient.builder(new HttpHost("192.168.1.109", 9200, "http")).build();
	}
	
	@Bean
	public DataSourceTransactionManager transactionManager() {
		DataSourceTransactionManager dsTransactionManager = new DataSourceTransactionManager(dataSource);
		return dsTransactionManager;
	}

	public DataSource getDataSource() {
		return dataSource;
	}

	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
	}

}

