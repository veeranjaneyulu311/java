package com.example.diagnosisdemo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;



@RestController
public class DIagContr {
	
	
	@Autowired
	DiagService diagService;
   
	
	@PostMapping("/createIndex")
	public Diagonise createIndex(@RequestBody Diagonise diagno) {
		return diagService.createIndex(diagno);	
	}
	
	
	@PostMapping("/search")
	public Iterable<Diagonise> searchField(@RequestBody Diagonise diagno) {
		return diagService.searchField();
	}

	
}
