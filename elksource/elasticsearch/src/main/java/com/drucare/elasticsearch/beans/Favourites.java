package com.drucare.elasticsearch.beans;

public class Favourites {

	private long created_usr_id;
	private String pattern;

	public long getCreated_usr_id() {
		return created_usr_id;
	}

	public void setCreated_usr_id(long created_usr_id) {
		this.created_usr_id = created_usr_id;
	}

	public String getPattern() {
		return pattern;
	}

	public void setPattern(String pattern) {
		this.pattern = pattern;
	}
}
