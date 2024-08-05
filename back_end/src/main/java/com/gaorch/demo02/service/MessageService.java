package com.gaorch.demo02.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.gaorch.demo02.entity.*;
import com.gaorch.demo02.mapper.ConversationMapper;
import com.gaorch.demo02.mapper.LibMapper;
import com.gaorch.demo02.mapper.MessageMapper;
import com.gaorch.demo02.mapper.RobotMapper;
import com.gaorch.demo02.utils.JwtUtils;
import com.gaorch.demo02.utils.Result;
import jakarta.annotation.PostConstruct;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.client.WebSocketClient;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.io.StringReader;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import com.fasterxml.jackson.databind.ObjectMapper;

@Service
public class MessageService
{

    @Autowired
    private MessageMapper messageMapper;

    @Autowired
    private ConversationMapper conversationMapper;

    @Autowired
    private LibMapper libMapper;

    @Autowired
    private RobotMapper robotMapper;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    public Result list(Integer conversationId)
    {
        // 从Redis缓存中获取消息
        List<Object> messages = redisTemplate.opsForList().range(conversationId.toString(), 0, -1);
        if (messages != null && !messages.isEmpty()) {
            System.out.println("调用redis");
            return Result.ok(messages);
        }

        List<Message> messagess = messageMapper.selectByConversationId(conversationId);
        return Result.ok(messagess);
    }

    // 存储 WebSocketSession 对象的映射，键是 conversationId
    private final ConcurrentHashMap<Integer, WebSocketSession> sessions = new ConcurrentHashMap<>();

    // 存储每个 conversationId 最后一次收到消息的时间
    private final ConcurrentHashMap<Integer, Long> lastMessageTime = new ConcurrentHashMap<>();

    // 定时任务的调度器，用于定期检查并关闭不活跃的 WebSocket 连接
    private ScheduledExecutorService scheduler;

    // 初始化方法，在服务启动时执行
    @PostConstruct
    public void init() {
        // 创建一个定时任务调度器，每分钟检查一次不活跃的 WebSocket 连接
        scheduler = Executors.newScheduledThreadPool(1);
        scheduler.scheduleAtFixedRate(this::checkAndCloseInactiveSessions, 1, 1, TimeUnit.MINUTES);
    }

    /**
     * 发送消息到对应的 WebSocket 连接
     */

    public Result file(MultipartHttpServletRequest request) throws IOException {
        MultipartFile file = request.getFile("file");
        String question = String.valueOf(request.getParameter("question"));
        Integer conversationId = Integer.valueOf(request.getParameter("conversationId"));
        String file_name = file.getOriginalFilename();
        file_name = URLDecoder.decode(file_name, "UTF-8");

        java.io.File folder=new java.io.File("/root/shixun/" + "conversation" + conversationId + "/");
        if(!folder.exists())
            folder.mkdirs();
        file.transferTo(new java.io.File(folder, file_name));

        WebSocketSession session = sessions.get(conversationId);
        if (session == null) {
            // 如果没有现有的 session，创建一个新的
            session = createWebSocketSession(conversationId);
            sessions.put(conversationId, session);

            PreData preData = new PreData();
            preData.setRobotId(6);

            ObjectMapper objectMapper = new ObjectMapper();
            String preJson = objectMapper.writeValueAsString(preData);
            session.sendMessage(new TextMessage(preJson));
        }

        Message message = new Message();
        message.setConversationId(conversationId);
        message.setContent(question);
        message.setIsPerson(1);
        messageMapper.insert(message);

        String key = conversationId.toString();
        redisTemplate.opsForList().rightPush(key, message);
        redisTemplate.expire(key, 1, TimeUnit.DAYS);  // 设置过期时间为1天

        // 发送消息
        question = file_name + "\n" + question;
        message.setContent(question);

        ObjectMapper objectMapper = new ObjectMapper();
        String json = objectMapper.writeValueAsString(message);
        session.sendMessage(new TextMessage(json));

        // 更新最后一次收到消息的时间
        lastMessageTime.put(conversationId, System.currentTimeMillis());

        return Result.ok();

    }

    public Result web(Message message) throws IOException
    {
        Integer conversationId = message.getConversationId();
        WebSocketSession session = sessions.get(conversationId);
        if (session == null) {
            // 如果没有现有的 session，创建一个新的
            session = createWebSocketSession(conversationId);
            sessions.put(conversationId, session);

            PreData preData = new PreData();
            preData.setRobotId(5);

            ObjectMapper objectMapper = new ObjectMapper();
            String preJson = objectMapper.writeValueAsString(preData);
            session.sendMessage(new TextMessage(preJson));
        }

        message.setIsPerson(1);
        messageMapper.insert(message);

        String key = conversationId.toString();
        redisTemplate.opsForList().rightPush(key, message);
        redisTemplate.expire(key, 1, TimeUnit.DAYS);  // 设置过期时间为1天

        // 发送消息
        ObjectMapper objectMapper = new ObjectMapper();
        String json = objectMapper.writeValueAsString(message);
        session.sendMessage(new TextMessage(json));

        // 更新最后一次收到消息的时间
        lastMessageTime.put(conversationId, System.currentTimeMillis());

        return Result.ok();
    }

    public Result vedio(Message message) throws IOException {
        Integer conversationId = message.getConversationId();
        WebSocketSession session = sessions.get(conversationId);
        if (session == null) {
            // 如果没有现有的 session，创建一个新的
            session = createWebSocketSession(conversationId);
            sessions.put(conversationId, session);

            PreData preData = new PreData();
            preData.setRobotId(4);

            // 从Redis缓存中获取消息
            List<Object> messages = redisTemplate.opsForList().range(conversationId.toString(), 0, -1);
            if (messages != null && !messages.isEmpty()) {
                System.out.println("调用redis");
                List<Message> msgs = messages.stream()
                        .map(obj -> (Message) obj)
                        .collect(Collectors.toList());

                List<Message> newMsgs = new ArrayList<>();
                int begin = 0;
                for(int i = 0; i < msgs.size(); i++)
                {
                    if(msgs.get(i).getContent().equals("您发的网址有问题，请重新发一下吧~"))
                    {
                        begin = i;
                    }
                }
                for(int i = begin + 1; i < msgs.size(); i++)
                {
                    newMsgs.add(msgs.get(i));
                }

                preData.setLastMessages(newMsgs);
            } else {
                List<Message> messagess = messageMapper.selectByConversationId(conversationId);

                List<Message> newMsgs = new ArrayList<>();
                int begin = 0;
                for(int i = 0; i < messagess.size(); i++)
                {
                    if(messagess.get(i).getContent().equals("您发的网址有问题，请重新发一下吧~"))
                    {
                        begin = i;
                    }
                }
                for(int i = begin + 1; i < messagess.size(); i++)
                {
                    newMsgs.add(messagess.get(i));
                }

                preData.setLastMessages(newMsgs);
            }

            ObjectMapper objectMapper = new ObjectMapper();
            String preJson = objectMapper.writeValueAsString(preData);
            session.sendMessage(new TextMessage(preJson));
        }

        message.setIsPerson(1);
        messageMapper.insert(message);

        String key = conversationId.toString();
        redisTemplate.opsForList().rightPush(key, message);
        redisTemplate.expire(key, 1, TimeUnit.DAYS);  // 设置过期时间为1天

        // 发送消息
        ObjectMapper objectMapper = new ObjectMapper();
        String json = objectMapper.writeValueAsString(message);
        session.sendMessage(new TextMessage(json));

        // 更新最后一次收到消息的时间
        lastMessageTime.put(conversationId, System.currentTimeMillis());

        return Result.ok();
    }

    public Result sendMessage(Message message) throws IOException {
        Integer conversationId = message.getConversationId();
        WebSocketSession session = sessions.get(conversationId);
        Conversation conversation = conversationMapper.selectById(conversationId);
        if (session == null) {
            // 如果没有现有的 session，创建一个新的
            session = createWebSocketSession(conversationId);
            sessions.put(conversationId, session);

            List<Message> messages = messageMapper.selectLastMessagesByConversationId(conversationId, 10);
            Robot robot = robotMapper.selectById(conversation.getRobotId());

            PreData preData = new PreData();

            preData.setLastMessages(messages);
            preData.setRobotId(robot.getId());
            preData.setPrompt(robot.getPrompt());

            if(conversation.getIfUseLib() == 1)
            {
                preData.setLibId(conversation.getLibId());
                Lib lib = libMapper.selectById(conversation.getLibId());
                preData.setName(lib.getName());
                preData.setDescription(lib.getDescription());
            }

            // 发送前置消息
            ObjectMapper objectMapper = new ObjectMapper();
            String preJson = objectMapper.writeValueAsString(preData);
            session.sendMessage(new TextMessage(preJson));
        }

        message.setIsPerson(1);
        messageMapper.insert(message);

        String key = conversationId.toString();
        redisTemplate.opsForList().rightPush(key, message);
        redisTemplate.expire(key, 1, TimeUnit.DAYS);  // 设置过期时间为1天

        // 发送消息
        ObjectMapper objectMapper = new ObjectMapper();
        String json = objectMapper.writeValueAsString(message);
        session.sendMessage(new TextMessage(json));

        // 更新最后一次收到消息的时间
        lastMessageTime.put(conversationId, System.currentTimeMillis());

        return Result.ok();
    }

    /**
     * 创建一个新的 WebSocket 连接
     * @param conversationId 会话 ID
     * @return WebSocketSession 对象
     */
    private WebSocketSession createWebSocketSession(Integer conversationId) {
        try {
            WebSocketClient client = new StandardWebSocketClient();
            // 连接到 FastAPI WebSocket 服务器，并返回 WebSocketSession 对象
            return client.doHandshake(new TextWebSocketHandler() {
                @Override
                protected void handleTextMessage(WebSocketSession session, TextMessage message) {
                    // 接收来自 FastAPI 的回答
                    String answer = message.getPayload();
                    System.out.println("Received answer: " + answer);
                    Message reply = new Message();
                    reply.setIsPerson(0);
                    reply.setContent(answer);
                    reply.setConversationId(conversationId);

                    messageMapper.insert(reply);

                    String key = conversationId.toString();
                    redisTemplate.opsForList().rightPush(key, reply);
                    redisTemplate.expire(key, 1, TimeUnit.DAYS);  // 设置过期时间为1天

                    conversationMapper.updateDate(conversationId);
                }

                @Override
                public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
                    // WebSocket 连接关闭后的处理逻辑
                    System.out.println("Connection closed: " + session.getId());
                }
            }, "ws://localhost:8080/ws").get();
        } catch (Exception e) {
            throw new RuntimeException("Failed to create WebSocket session", e);
        }
    }

    /**
     * 检查并关闭超过 5 分钟未活动的 WebSocket 连接
     */
    private void checkAndCloseInactiveSessions() {
        long currentTime = System.currentTimeMillis();
        for (Integer conversationId : sessions.keySet()) {
            Long lastTime = lastMessageTime.get(conversationId);
            if (lastTime != null && currentTime - lastTime > TimeUnit.MINUTES.toMillis(5)) {
                closeSession(conversationId);
            }
        }
    }

    /**
     * 关闭指定的 WebSocket 连接
     * @param conversationId 会话 ID
     */
    private void closeSession(Integer conversationId) {
        WebSocketSession session = sessions.remove(conversationId);
        if (session != null && session.isOpen()) {
            try {
                session.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        lastMessageTime.remove(conversationId);
    }
}
