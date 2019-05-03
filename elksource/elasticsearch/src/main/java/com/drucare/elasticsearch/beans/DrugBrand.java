package com.drucare.elasticsearch.beans;

public class DrugBrand {
	int drug_brand_id;
	int drug_type_id;
	int drug_id;
	int dose_id;
	String drug_brand_nm;
	String dose_nm;
	String drug_type_nm;
	String drug_nm;

	public DrugBrand() {
	}

	
	
	public DrugBrand(int drug_id, String drug_nm) {
		super();
		this.drug_id = drug_id;
		this.drug_nm = drug_nm;
	}



	public DrugBrand(int drug_brand_id, int drug_type_id, int drug_id, int dose_id, String drug_brand_nm,
			String dose_nm, String drug_type_nm) {
		super();
		this.drug_brand_id = drug_brand_id;
		this.drug_type_id = drug_type_id;
		this.drug_id = drug_id;
		this.dose_id = dose_id;
		this.drug_brand_nm = drug_brand_nm;
		this.dose_nm = dose_nm;
		this.drug_type_nm = drug_type_nm;
	}

	public String getDrug_nm() {
		return drug_nm;
	}

	public void setDrug_nm(String drug_nm) {
		this.drug_nm = drug_nm;
	}

	public int getDrug_brand_id() {
		return drug_brand_id;
	}

	public void setDrug_brand_id(int drug_brand_id) {
		this.drug_brand_id = drug_brand_id;
	}

	public int getDrug_type_id() {
		return drug_type_id;
	}

	public void setDrug_type_id(int drug_type_id) {
		this.drug_type_id = drug_type_id;
	}

	public int getDrug_id() {
		return drug_id;
	}

	public void setDrug_id(int drug_id) {
		this.drug_id = drug_id;
	}

	public int getDose_id() {
		return dose_id;
	}

	public void setDose_id(int dose_id) {
		this.dose_id = dose_id;
	}

	public String getDrug_brand_nm() {
		return drug_brand_nm;
	}

	public void setDrug_brand_nm(String drug_brand_nm) {
		this.drug_brand_nm = drug_brand_nm;
	}

	public String getDose_nm() {
		return dose_nm;
	}

	public void setDose_nm(String dose_nm) {
		this.dose_nm = dose_nm;
	}

	public String getDrug_type_nm() {
		return drug_type_nm;
	}

	public void setDrug_type_nm(String drug_type_nm) {
		this.drug_type_nm = drug_type_nm;
	}

}
