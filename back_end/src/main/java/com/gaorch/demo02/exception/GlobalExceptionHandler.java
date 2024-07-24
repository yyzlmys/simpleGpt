package com.gaorch.demo02.exception;

import com.gaorch.demo02.utils.Result;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class)
    public Result ex(Exception ex)
    {
        ex.printStackTrace();
        return Result.error();
    }
}
