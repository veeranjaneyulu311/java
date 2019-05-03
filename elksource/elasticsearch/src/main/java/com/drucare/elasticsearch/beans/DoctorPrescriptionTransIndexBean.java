package com.drucare.elasticsearch.beans;

public class DoctorPrescriptionTransIndexBean {

	private int drug_brand_id;
	private int drug_id;
	private long created_usr_id;

	public DoctorPrescriptionTransIndexBean() {

	}
	
	public DoctorPrescriptionTransIndexBean(int drug_brand_id, int drug_id, long created_usr_id) {
		super();
		this.drug_brand_id = drug_brand_id;
		this.drug_id = drug_id;
		this.created_usr_id = created_usr_id;
	}

	public int getDrug_brand_id() {
		return drug_brand_id;
	}

	public void setDrug_brand_id(int drug_brand_id) {
		this.drug_brand_id = drug_brand_id;
	}

	public int getDrug_id() {
		return drug_id;
	}

	public void setDrug_id(int drug_id) {
		this.drug_id = drug_id;
	}

	public long getCreated_usr_id() {
		return created_usr_id;
	}

	public void setCreated_usr_id(long created_usr_id) {
		this.created_usr_id = created_usr_id;
	}

	
}
