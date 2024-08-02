package com.gaorch.demo02.entity;

import lombok.Data;

import java.util.List;

@Data
public class PreData
{
    private Integer robotId;
    private String prompt;
    private Integer libId;
    private String name;
    private String description;
    private List<Message> lastMessages;
}
