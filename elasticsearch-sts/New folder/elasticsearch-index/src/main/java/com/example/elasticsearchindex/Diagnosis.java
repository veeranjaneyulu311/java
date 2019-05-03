package com.example.elasticsearchindex;

public class Diagnosis {
	
	long patientID;
	String diseaseName;
	String specificDiagnosis;
	
	public Diagnosis() {
		
	}
	
	
	
	public Diagnosis(long l, String diseaseName, String specificDiagnosis) {
		this.patientID = l;
		this.diseaseName = diseaseName;
		this.specificDiagnosis = specificDiagnosis;
	}



	public long getPatientID() {
		return patientID;
	}
	public void setPatientID(long patientID) {
		this.patientID = patientID;
	}
	public String getDiseaseName() {
		return diseaseName;
	}
	public void setDiseaseName(String diseaseName) {
		this.diseaseName = diseaseName;
	}
	public String getSpecificDiagnosis() {
		return specificDiagnosis;
	}
	public void setSpecificDiagnosis(String specificDiagnosis) {
		this.specificDiagnosis = specificDiagnosis;
	}
	

}
