package com.example.elasticsearchindex;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class DiagnosisData {

	@Autowired
	NamedParameterJdbcTemplate namedParameterjdbcTemplate;

	public List<Diagnosis> fetchDiagnosis() {

		// query="SELECT PATIENT_ID, PATIENT_VISIT_ID, HOS_PATIENT_ID, VISIT_DT,
		// DISEASE_CODE, DISEASES_NM, SPECIFIC_DIAGNOSIS, PLAN_SURGERY_DT,
		// NEXT_REVIEW_DT FROM OPD.PATIENT_VISIT_DISEASES_TRANS";
		String query = "SELECT PATIENT_ID, DISEASES_NM, SPECIFIC_DIAGNOSIS FROM OPD.PATIENT_VISIT_DISEASES_TRANS";

		return namedParameterjdbcTemplate.query(query, new RowMapper<Diagnosis>() {

			@Override
			public Diagnosis mapRow(ResultSet rs, int rowNum) throws SQLException {
				return new Diagnosis(Long.parseLong(rs.getBigDecimal("PATIENT_ID").toString()),
						rs.getString("DISEASES_NM"), rs.getString("SPECIFIC_DIAGNOSIS"));
			}
		});
	}

}
