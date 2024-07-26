package com.gaorch.demo02.config;

import com.gaorch.demo02.interceptor.AuthenticationInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry)
    {
        registry.addInterceptor(new AuthenticationInterceptor())
                .excludePathPatterns("/login", "/signup", "/conversation/name")
                .addPathPatterns("/**");
    }
}
