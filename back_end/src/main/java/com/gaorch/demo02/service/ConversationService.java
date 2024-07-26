package com.gaorch.demo02.service;

import com.gaorch.demo02.entity.Conversation;
import com.gaorch.demo02.entity.Lib;
import com.gaorch.demo02.entity.Message;
import com.gaorch.demo02.mapper.ConversationMapper;
import com.gaorch.demo02.mapper.MessageMapper;
import com.gaorch.demo02.utils.JwtUtils;
import com.gaorch.demo02.utils.Result;
import jakarta.servlet.http.HttpServletRequest;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ConversationService
{
    @Autowired
    private MessageMapper messageMapper;

    @Autowired
    private ConversationMapper conversationMapper;

    @Autowired
    private HttpServletRequest request;

    public Result list()
    {
        Integer userId = JwtUtils.getId(request);
        List<Conversation> conversations = conversationMapper.selectByUserId(userId);
        for (Conversation conversation : conversations)
        {
            conversation.setLastMessage(messageMapper.selectLastByConversationId(conversation.getId()));
        }
        return Result.ok(conversations);
    }

    public Result create(Conversation conversation)
    {
        Integer userId = JwtUtils.getId(request);
        conversation.setUserId(userId);
        conversation.setName("新建会话");
        conversation.setId(0);
        conversationMapper.insert(conversation);
        return Result.ok(conversation.getId());
    }

    public Result delete(Integer id)
    {
        messageMapper.deleteByConversationId(id);
        conversationMapper.deleteById(id);
        return Result.ok();
    }

    public void deleteByUserId(Integer userId)
    {
        List<Conversation> conversations = conversationMapper.selectByUserId(userId);
        for(Conversation conversation: conversations)
        {
            delete(conversation.getId());
        }
    }

    public void name(String name, Integer id)
    {
        conversationMapper.updateNameById(name, id);
    }

    public Result getName(Integer id)
    {
        String name = conversationMapper.getNameById(id);
        return Result.ok(name);
    }
}










