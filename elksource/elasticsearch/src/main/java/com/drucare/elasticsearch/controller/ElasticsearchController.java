package com.drucare.elasticsearch.controller;

import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

import org.json.simple.parser.ParseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.drucare.elasticsearch.beans.DoctorFavouriteDrugsSearchBean;
import com.drucare.elasticsearch.beans.DrugsFoundResponseBean;
import com.drucare.elasticsearch.beans.Favourites;
import com.drucare.elasticsearch.beans.DrugSearchBean;
import com.drucare.elasticsearch.service.ElasticsearchService;

@RestController
public class ElasticsearchController {

	@Autowired
	ElasticsearchService elaticsearchService;
	
	
	@GetMapping("/indexDeseases")
	public void indexDeseasesInfo() throws IOException {
		elaticsearchService.indexDeseasesInfo();
	}
	

	@GetMapping("/indexDrugs")
	public void indexDrugsInfo() throws IOException {
		elaticsearchService.indexDrugsInfo();
	}

	@Scheduled(cron = "0 0 0 ? * 1")
	public void indexDrugsInfoSchedule() throws IOException {
		elaticsearchService.indexDrugsInfo();
	}

	@GetMapping("/indexDoctorPrescriptionTrans")
	public void indexDoctorPrescriptionTransInfo() throws IOException {
		elaticsearchService.indexDoctorPrescriptionTransInfo();
	}

	@Scheduled(cron = "0 0 0 * * ?")
	public void indexDoctorPrescriptionTransInfoSchedule() throws IOException {
		elaticsearchService.indexDoctorPrescriptionTransInfo();
	}

	@GetMapping("/indexDoctorFavourites")
	public void indexDoctorFavouritesInfo() throws IOException {
		elaticsearchService.indexDoctorFavouritesInfo();
	}

	@Scheduled(cron = "0 0 0 * * ?")
	public void indexDoctorFavouritesInfoSchedule() throws IOException {
		elaticsearchService.indexDoctorFavouritesInfo();
	}

	@PostMapping("/fetchDrugs")
	public List<DrugsFoundResponseBean> fetchDrugsInfo(@RequestBody DrugSearchBean drugSearchBean)
			throws IOException, ParseException {
		return elaticsearchService.fetchDrugsInfo(drugSearchBean);
	}

	@PostMapping("/fetchDoctorFavDrugs")
	public List<DrugsFoundResponseBean> fetchDoctorFavDrugsInfo(
			@RequestBody DoctorFavouriteDrugsSearchBean doctorFavouriteDrugsSearchBean)
			throws IOException, ParseException {
		return elaticsearchService.fetchDoctorFavDrugsInfo(doctorFavouriteDrugsSearchBean);
	}

	@PostMapping("/fetchFavs")
	public List<DrugsFoundResponseBean> fetchFavouritesInfo(@RequestBody Favourites fav) throws IOException, ParseException {

		return elaticsearchService.fetchFavouritesInfo(fav);
	}
	
	@GetMapping("/copydata")
	public void copydata() throws SQLException {
		elaticsearchService.getData();
	}
}
