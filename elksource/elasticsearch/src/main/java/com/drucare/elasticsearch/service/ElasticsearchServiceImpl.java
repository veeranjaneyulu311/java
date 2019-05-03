package com.drucare.elasticsearch.service;

import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

import org.json.simple.parser.ParseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.drucare.elasticsearch.beans.DrugsFoundResponseBean;
import com.drucare.elasticsearch.beans.Favourites;
import com.drucare.elasticsearch.beans.DoctorFavouriteDrugsSearchBean;
import com.drucare.elasticsearch.beans.DrugSearchBean;
import com.drucare.elasticsearch.dao.ElasticsearchDao;

@Service
public class ElasticsearchServiceImpl implements ElasticsearchService {

	@Autowired
	ElasticsearchDao elasticSearchDao;

	@Override
	public void indexDrugsInfo() throws IOException {
		elasticSearchDao.indexDrugsInfo();
	}

	@Override
	public void indexDoctorPrescriptionTransInfo() throws IOException {
		elasticSearchDao.indexDoctorPrescriptionTransInfo();	
	}
	
	@Override
	public void indexDoctorFavouritesInfo() throws IOException {
		elasticSearchDao.indexDoctorFavouritesInfo();
	}

	@Override
	public List<DrugsFoundResponseBean> fetchDrugsInfo(DrugSearchBean drugSearchBean)
			throws IOException, ParseException {

		return elasticSearchDao.fetchDrugsInfo(drugSearchBean);
	}

	@Override
	public List<DrugsFoundResponseBean> fetchDoctorFavDrugsInfo(
			DoctorFavouriteDrugsSearchBean doctorFavouriteDrugsSearchBean) throws ParseException, IOException {

		return elasticSearchDao.fetchDoctorFavDrugsInfo(doctorFavouriteDrugsSearchBean);
	}

	@Override
	public List<DrugsFoundResponseBean> fetchFavouritesInfo(Favourites fav) throws IOException, ParseException {
		
		return elasticSearchDao.fetchFavouritesInfo(fav);
	}
	
	@Override
	public void getData() throws SQLException{
		
		elasticSearchDao.getData();
	}

	@Override
	public void indexDeseasesInfo() throws IOException {
		elasticSearchDao.indexDeseasesInfo();
		
	}

	
}