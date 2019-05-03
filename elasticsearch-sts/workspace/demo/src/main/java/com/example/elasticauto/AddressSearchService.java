package com.example.elasticauto;

public interface AddressSearchService {

	SearchResultDto autocomplete(String search, int size);

}
