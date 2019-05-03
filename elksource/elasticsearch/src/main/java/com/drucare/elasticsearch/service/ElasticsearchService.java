package com.drucare.elasticsearch.service;

import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

import org.json.simple.parser.ParseException;

import com.drucare.elasticsearch.beans.DoctorFavouriteDrugsSearchBean;
import com.drucare.elasticsearch.beans.DrugsFoundResponseBean;
import com.drucare.elasticsearch.beans.Favourites;
import com.drucare.elasticsearch.beans.DrugSearchBean;

public interface ElasticsearchService {

	public void indexDrugsInfo() throws IOException;

	public void indexDoctorPrescriptionTransInfo() throws IOException;
	
	public void indexDoctorFavouritesInfo() throws IOException;
	
	public List<DrugsFoundResponseBean> fetchDrugsInfo(DrugSearchBean drugSearchBean)
			throws IOException, ParseException;

	public List<DrugsFoundResponseBean> fetchDoctorFavDrugsInfo(
			DoctorFavouriteDrugsSearchBean doctorFavouriteDrugsSearchBean) throws ParseException, IOException;

	public List<DrugsFoundResponseBean> fetchFavouritesInfo(Favourites fav) throws IOException, ParseException;

	public void getData() throws SQLException;

	public void indexDeseasesInfo() throws IOException;
}
