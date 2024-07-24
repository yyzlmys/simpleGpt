package com.gaorch.demo02.controller;

import com.gaorch.demo02.entity.Message;
import com.gaorch.demo02.service.MessageService;
import com.gaorch.demo02.utils.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@RestController
@RequestMapping("/message")
public class MessageController
{
    @Autowired
    private MessageService messageService;

    @GetMapping("/list/{conversationId}")
    public Result list(@PathVariable Integer conversationId)
    {
        return messageService.list(conversationId);
    }


    @PostMapping("/ask")
    public Result ask(@RequestBody Message message) throws IOException {
        return messageService.sendMessage(message);
    }
}







