package com.example.elasticauto;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AutoController {

	@Autowired
	private AddressSearchService service;

	@GetMapping("/hello")
	public SearchResultDto autocomplete(@RequestParam("search") String search, @RequestParam(defaultValue = "20") int size) {
		return service.autocomplete(search, size);
	}

}
