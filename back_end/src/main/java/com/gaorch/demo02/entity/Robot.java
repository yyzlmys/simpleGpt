package com.gaorch.demo02.entity;

import lombok.Data;

@Data
public class Robot
{
    private Integer id;
    private Integer userId;
    private String name;
    private String prompt;
    private String intro;
}
