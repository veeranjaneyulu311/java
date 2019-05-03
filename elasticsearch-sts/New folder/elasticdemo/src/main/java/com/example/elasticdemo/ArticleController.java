package com.example.elasticdemo;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ArticleController {

	@Autowired
	ArticleService articleService;

	@PostMapping("/save")
	public Article save(@RequestBody Article article) {
		return articleService.save(article);
	}

	@GetMapping("/fetchOne/{id}")
	public Optional<Article> findOne(@PathVariable String id) {
		return articleService.findOne(id);
	}

	@GetMapping("/fetchAll")
	public Iterable<Article> findAll() {
		return articleService.findAll();
	}

	/*
	 * public Page<Article> findByAuthorName(String name, Pageable pageable) {
	 * return articleService.findByAuthorsName(name, pageable); }
	 * 
	 * public Page<Article> findByAuthorNameUsingCustomQuery(String name, Pageable
	 * pageable) { return articleService.findByAuthorsNameUsingCustomQuery(name,
	 * pageable); }
	 */

	@PostMapping("/findByTag/{tag}")
	public Page<Article> findByFilteredTagQuery(@PathVariable String tag, Pageable pageable) {
		return articleService.findByFilteredTagQuery(tag, pageable);
	}
	
	@PostMapping("/findByNameAndTag/{name}/{tag}")
	public Page<Article> findByAuthorsNameAndFilteredTagQuery(@PathVariable String name,@PathVariable String tag, Pageable pageable) {
		return articleService.findByAuthorsNameAndFilteredTagQuery(name, tag, pageable);
	}

	@GetMapping("/count")
	public long count() {
		return articleService.count();
	}

	@PostMapping("/delete")
	public void delete(@RequestBody Article article) {
		articleService.delete(article);
	}

}
