package com.practice;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

public class FourthFilter implements Filter{

	FilterConfig config;

	public void init(FilterConfig config) throws ServletException {
		this.config = config;
	}

	public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain)
			throws IOException, ServletException {

		PrintWriter out = resp.getWriter();

		String s = config.getInitParameter("fourthFilter");
		out.println("Filter4 is working...................." + s);
		
		if (s.equals("no")) {
			out.println("This Filter4 is under construction");
		} else {
			chain.doFilter(req, resp);// sends request to next resource
		}
		out.println("after-four");
		
	}
	
	
	public void destroy() {
	}

}
