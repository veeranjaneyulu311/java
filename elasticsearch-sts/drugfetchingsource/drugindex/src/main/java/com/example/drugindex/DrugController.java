package com.example.drugindex;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DrugController {
	@Autowired
	DrugIndex drugIndex;
	
	@GetMapping("/index")
	public void sample() throws IOException {
		drugIndex.getDrugs();
	}
}