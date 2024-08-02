package com.gaorch.demo02.entity;

import lombok.Data;

@Data
public class Message
{
    private Integer id;
    private Integer conversationId;
    private Integer isPerson;
    private String content;
}
