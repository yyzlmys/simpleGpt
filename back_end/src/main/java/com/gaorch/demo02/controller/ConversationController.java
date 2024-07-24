package com.gaorch.demo02.controller;

import com.gaorch.demo02.entity.Conversation;
import com.gaorch.demo02.service.ConversationService;
import com.gaorch.demo02.utils.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/conversation")
public class ConversationController
{
    @Autowired
    private ConversationService conversationService;

    @GetMapping("/list")
    public Result list()
    {
        return conversationService.list();
    }

    @PostMapping("")
    public Result create(@RequestBody Conversation conversation)
    {
        return conversationService.create(conversation);
    }

    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id)
    {
        return conversationService.delete(id);
    }
}
