package com.gaorch.demo02.entity;

import lombok.Data;

@Data
public class Conversation
{
    private Integer id;
    private Integer userId;
    private String name;
    private Integer ifUseLib;
    private Integer LibId;
    private String date;

    private Message lastMessage;
}
