package com.example.drugindex.bean;

public class Drug {
	
	private String comb_drugnm;
	private String drugid;
	private String brandId;
	
	
	public String getDrugid() {
		return drugid;
	}

	public void setDrugid(String drugid) {
		this.drugid = drugid;
	}

	public String getBrandId() {
		return brandId;
	}

	public void setBrandId(String brandId) {
		this.brandId = brandId;
	}

	public Drug() {
	}

	

	public Drug(String comb_drugnm, String drugid, String brandId) {
		super();
		this.comb_drugnm = comb_drugnm;
		this.drugid = drugid;
		this.brandId = brandId;
	}

	public String getComb_drugnm() {
		return comb_drugnm;
	}

	public void setComb_drugnm(String comb_drugnm) {
		this.comb_drugnm = comb_drugnm;
	}
	
	
}
