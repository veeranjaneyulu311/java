package com.example.diagnosissearch;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RestClientController {

	@Autowired
	RestClientConfig restClientConfig;
	
	@GetMapping("/fetchSuggestions/{find}")
	public String findSuggestion(@PathVariable String find) throws IOException {
		return restClientConfig.fetchFromElasticSearch(find);
	}
}
