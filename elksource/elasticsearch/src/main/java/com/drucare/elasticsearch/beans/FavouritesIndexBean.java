package com.drucare.elasticsearch.beans;

public class FavouritesIndexBean {

	private String drug_nm;
	private String drug_brand_nm;
	private int drug_id;
	private int drug_brand_id;
	private long created_usr_id;
	

	public FavouritesIndexBean() {

	}
	
	public FavouritesIndexBean(int drug_brand_id, String drug_brand_nm, int drug_id, String drug_nm,long created_usr_id) {
		super();
		this.drug_nm = drug_nm;
		this.drug_brand_nm = drug_brand_nm;
		this.drug_id = drug_id;
		this.drug_brand_id = drug_brand_id;
		this.created_usr_id=created_usr_id;
	}

	public String getDrug_nm() {
		return drug_nm;
	}

	public void setDrug_nm(String drug_nm) {
		this.drug_nm = drug_nm;
	}

	public String getDrug_brand_nm() {
		return drug_brand_nm;
	}

	public void setDrug_brand_nm(String drug_brand_nm) {
		this.drug_brand_nm = drug_brand_nm;
	}

	public int getDrug_id() {
		return drug_id;
	}

	public void setDrug_id(int drug_id) {
		this.drug_id = drug_id;
	}

	public int getDrug_brand_id() {
		return drug_brand_id;
	}

	public void setDrug_brand_id(int drug_brand_id) {
		this.drug_brand_id = drug_brand_id;
	}

	public long getCreated_usr_id() {
		return created_usr_id;
	}

	public void setCreated_usr_id(long created_usr_id) {
		this.created_usr_id = created_usr_id;
	}

	
}
