package com.example.drugindex;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

import com.example.drugindex.bean.Drug;

@Repository
public class DrugDao {
	/*queries.fetchDrugs=SELECT COMB_DRUGNM,COMB_DRUGID FROM  PUBLIC.DRUGS_INFO WHERE COMB_DRUGNM ILIKE :COMB_DRUGNM*/
	
	@Autowired
	NamedParameterJdbcTemplate namedParameterjdbcTemplate;
	
	
	public List<Drug> fetchDrugs() {

		String query = "SELECT COMB_DRUGID,COMB_DRUGNM FROM  PUBLIC.DRUGS_INFO";
		
		/*return namedParameterjdbcTemplate.query(query, new RowMapper<String>() {

			@Override
			public String mapRow(ResultSet rs, int rowNum) throws SQLException {
				return rs.getString("COMB_DRUGNM");
			}
		}
		);*/

		return namedParameterjdbcTemplate.query(query, new RowMapper<Drug>() {

			@Override
			public Drug mapRow(ResultSet rs, int rowNum) throws SQLException {
				
				String comb_drugid=rs.getString("COMB_DRUGID");
				return new Drug(rs.getString("COMB_DRUGNM"),comb_drugid.split("-")[1],comb_drugid.split("-")[0]);
			}
		});
		
		/*if(!drugList.isEmpty()) {
			for (String combDrugName : drugList) {
				drug=new Drug();
				
				drug.setBrandName(combDrugName.split("@@")[0]);
				drug.setDrugName(combDrugName.split("@@")[1]);
				
				drugsNames.add(drug);
			}
			
			return drugsNames;
		}
		
		return null;
		*/
		
	} 

}
