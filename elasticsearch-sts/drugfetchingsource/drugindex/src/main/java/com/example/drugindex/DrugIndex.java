package com.example.drugindex;

import java.io.IOException;
import java.util.List;

import org.elasticsearch.client.Request;
import org.elasticsearch.client.Response;
import org.elasticsearch.client.RestClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.example.drugindex.bean.Drug;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class DrugIndex {

	@Autowired
	DrugIndex drugIndex;

	@Autowired
	RestClient client;

	@Autowired
	DrugDao drugDao;

	private void createIndex() throws IOException {

		String indexMappings = "{ \"settings\": { \"analysis\": { \"normalizer\": { \"drugs_keyword_normalizer\": { \"type\": \"custom\", \"filter\": [ \"lowercase\" ] } } } }, \"mappings\": { \"drugs_type\": { \"properties\": { \"comb_drugnm\": { \"type\": \"keyword\",\"normalizer\": \"drugs_keyword_normalizer\" } } } } } ";

		Request request = new Request("PUT", "/drugsinfo");

		request.setJsonEntity(indexMappings);

		Response response = client.performRequest(request);

	}

	private void indexData(String data) throws IOException {

		Request request = new Request("POST", "/drugsinfo/drugs_type/_bulk");

		request.setJsonEntity(data);

		Response response = client.performRequest(request);

	}

	public void getDrugs() throws IOException {

		List<Drug> drugsInfo = drugDao.fetchDrugs();
		StringBuilder sb = new StringBuilder();

		// java object to json conversion jakson
		ObjectMapper mapper = new ObjectMapper();

		for (Drug drug : drugsInfo) {
			sb.append("{ \"index\" : {}}\n");
			sb.append(mapper.writeValueAsString(drug));
			sb.append("\n");
		}

		System.out.println(sb);

		drugIndex.createIndex();
		drugIndex.indexData(sb.toString());
	}

}
