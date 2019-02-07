package com.practice;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.*;

public class FirstFilter implements Filter {
	FilterConfig config;

	public void init(FilterConfig config) throws ServletException {
		this.config = config;
	}

	public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain)
			throws IOException, ServletException {

		PrintWriter out = resp.getWriter();

		String s = config.getInitParameter("construction");
		
		out.println("Filter1 is working...................."+s);
		
		if (s.equals("no")) {
			out.println("This Filter1 is under construction");
		} else {
			chain.doFilter(req, resp);// sends request to next resource
		}
		out.println("after-first");
	}

	public void destroy() {
	}

}
