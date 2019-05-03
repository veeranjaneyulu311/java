package com.drucare.elasticsearch.dao;

import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

import org.json.simple.parser.ParseException;

import com.drucare.elasticsearch.beans.DrugsFoundResponseBean;
import com.drucare.elasticsearch.beans.Favourites;
import com.drucare.elasticsearch.beans.DoctorFavouriteDrugsSearchBean;
import com.drucare.elasticsearch.beans.DrugSearchBean;

public interface ElasticsearchDao {

	void indexDrugsInfo() throws IOException;

	void indexDoctorPrescriptionTransInfo() throws IOException;
	
	void indexDoctorFavouritesInfo() throws IOException;

	List<DrugsFoundResponseBean> fetchDrugsInfo(DrugSearchBean drugSearchBean) throws IOException, ParseException;

	List<DrugsFoundResponseBean> fetchDoctorFavDrugsInfo(DoctorFavouriteDrugsSearchBean doctorFavouriteDrugsSearchBean) throws ParseException, IOException;

	List<DrugsFoundResponseBean> fetchFavouritesInfo(Favourites fav) throws IOException, ParseException;

	void getData() throws SQLException;

	void indexDeseasesInfo() throws IOException;

	
}
