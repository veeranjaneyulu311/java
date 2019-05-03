package com.drucare.elasticsearch.beans;

public class Deseases {
	
	private String diseases_nm;
	
	public Deseases() {
	}

	public Deseases(String diseases_nm) {
		super();
		this.diseases_nm = diseases_nm;
	}

	public String getDiseases_nm() {
		return diseases_nm;
	}

	public void setDiseases_nm(String diseases_nm) {
		this.diseases_nm = diseases_nm;
	}

}
