package com.gaorch.demo02.utils;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.HashMap;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Result
{
    private Integer code;
    private Object data;

    public static Result ok(Object value)
    {
        return new Result(Code.SUCCESS, value);
    }

    public static Result ok()
    {
        return new Result(Code.SUCCESS, null);
    }

    public static Result error()
    {
        return new Result(Code.ERROR, null);
    }

    public static Result error(Object value)
    {
        return new Result(Code.ERROR, value);
    }

    public static Result unAuthorized()
    {
        return new Result(Code.UNAUTHORIZED, null);
    }

    public static Result serious()
    {
        return new Result(Code.SERIOUS_ERROR, null);
    }

}
