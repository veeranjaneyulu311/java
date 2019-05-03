package com.example.elasticsearchindex;

import java.io.IOException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SmapleControler {
	
	@Autowired
	ElasticSearchIndex esi;
	
	@GetMapping("/sample")
	public void sample() throws IOException {
		esi.getDiagnosis();
	}
}
