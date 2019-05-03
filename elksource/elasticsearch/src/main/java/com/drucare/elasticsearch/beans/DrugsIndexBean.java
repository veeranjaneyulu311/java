package com.drucare.elasticsearch.beans;

public class DrugsIndexBean {
	private String comb_drugnm;
	private int drug_id;
	private int drug_brand_id;
	
	public DrugsIndexBean() {
		
	}

	public DrugsIndexBean(String comb_drugnm, int drug_id, int drug_brand_id) {
		super();
		this.comb_drugnm = comb_drugnm;
		this.drug_id = drug_id;
		this.drug_brand_id = drug_brand_id;
	}

	public String getComb_drugnm() {
		return comb_drugnm;
	}

	public void setComb_drugnm(String comb_drugnm) {
		this.comb_drugnm = comb_drugnm;
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
	
	
	
}
