package com.gaorch.demo02.entity;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Lib
{
    private Integer id;
    private Integer userId;
    private String name;
    private double size;
    private String description;
}
