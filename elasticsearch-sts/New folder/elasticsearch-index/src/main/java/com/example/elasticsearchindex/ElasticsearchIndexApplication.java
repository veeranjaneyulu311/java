package com.example.elasticsearchindex;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;

@SpringBootApplication
public class ElasticsearchIndexApplication {

	@Autowired
	private DataSource dataSource;
	
	
	
	public static void main(String[] args) {
		SpringApplication.run(ElasticsearchIndexApplication.class, args);
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
