package com.drucare.elasticsearch.beans;

public class DrugSearchBean {
	String drugName;
	String selectCriteria;

	public String getDrugName() {
		return drugName;
	}
	public void setDrugName(String drugName) {
		this.drugName = drugName;
	}
	public String getSelectCriteria() {
		return selectCriteria;
	}
	public void setSelectCriteria(String selectCriteria) {
		this.selectCriteria = selectCriteria;
	}	
}
