package com.example.elasticauto;

import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.unit.Fuzziness;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.suggest.Suggest;
import org.elasticsearch.search.suggest.Suggest.Suggestion;
import org.elasticsearch.search.suggest.Suggest.Suggestion.Entry;
import org.elasticsearch.search.suggest.Suggest.Suggestion.Entry.Option;
import org.elasticsearch.search.suggest.SuggestBuilder;
import org.elasticsearch.search.suggest.completion.CompletionSuggestionBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AddressSearchServiceImpl implements AddressSearchService{
	
	@Autowired
	Client client;
	
	@Override
	public SearchResultDto autocomplete(String prefixString, int size) {
	     SearchRequest searchRequest = new SearchRequest("music");
	     CompletionSuggestionBuilder suggestBuilder = new CompletionSuggestionBuilder("name"); // Note 1

	     suggestBuilder.size(size)
	                   .prefix(prefixString, Fuzziness.ONE) // Note 2
	                   .skipDuplicates(true)
	                   .analyzer("standard");
	 
	     SearchSourceBuilder sourceBuilder = new SearchSourceBuilder(); // _search
	     sourceBuilder.suggest(new SuggestBuilder().addSuggestion("name", suggestBuilder));
	     searchRequest.source(sourceBuilder);

	     SearchResponse response;
	     response = (SearchResponse) client.search(searchRequest);
		  return getSuggestions(response); // Note 3
	}
	
	
	
	   private SearchResultDto getSuggestions(SearchResponse response) {
		 SearchResultDto dto = new SearchResultDto();
		 Suggest suggest = response.getSuggest();
		 Suggestion<Entry<Option>> suggestion = suggest.getSuggestion("name");
		 for(Entry<Option> entry: suggestion.getEntries()) {
		       for (Option option: entry.getOptions()) {
		         dto.add(option.getText().toString());
		       }
		 }
		 return dto;
		}


}
