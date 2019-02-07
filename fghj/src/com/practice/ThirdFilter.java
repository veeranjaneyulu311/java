package com.practice;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

public class ThirdFilter implements Filter{

	FilterConfig config;

	public void init(FilterConfig config) throws ServletException {
		this.config = config;
	}

	public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain)
			throws IOException, ServletException {

		PrintWriter out = resp.getWriter();

		String s = config.getInitParameter("thirdFilter");
		out.println("Filter3 is working...................." + s);
		if (s.equals("no")) {
			out.println("This Filter3 is under construction");
		} else {
			chain.doFilter(req, resp);// sends request to next resource
		}
		out.println("after-three");
	}

	public void destroy() {
	}


}
