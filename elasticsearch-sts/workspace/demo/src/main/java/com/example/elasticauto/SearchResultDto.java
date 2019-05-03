package com.example.elasticauto;

import java.util.ArrayList;
import java.util.List;

public class SearchResultDto {
	private List<String> suggestedAddresses=new ArrayList<String>();

	public List<String> getSuggestedAddresses() {
		return suggestedAddresses;
	}

	public void setSuggestedAddresses(List<String> suggestedAddresses) {
		this.suggestedAddresses = suggestedAddresses;
	}

	public void add(String string) {
		suggestedAddresses.add(string);
		
	}

}
