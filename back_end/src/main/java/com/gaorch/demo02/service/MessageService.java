package com.gaorch.demo02.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.gaorch.demo02.entity.*;
import com.gaorch.demo02.mapper.ConversationMapper;
import com.gaorch.demo02.mapper.LibMapper;
import com.gaorch.demo02.mapper.MessageMapper;
import com.gaorch.demo02.mapper.RobotMapper;
import com.gaorch.demo02.utils.Result;
import jakarta.annotation.PostConstruct;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.client.WebSocketClient;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.io.StringReader;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
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

    public Result insert(Message message)
    {
        message.setId(0);
        messageMapper.insert(message);
        return Result.ok();
    }

    public Result list(Integer conversationId)
    {
        List<Message> messages = messageMapper.selectByConversationId(conversationId);
        return Result.ok(messages);
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

    public Result sendMessage(Message message) throws IOException {
        Integer conversationId = message.getConversationId();
        WebSocketSession session = sessions.get(conversationId);
        if (session == null) {
            // 如果没有现有的 session，创建一个新的
            session = createWebSocketSession(conversationId);
            sessions.put(conversationId, session);

            List<Message> messages = messageMapper.selectLastMessagesByConversationId(conversationId, 10);
            Conversation conversation = conversationMapper.selectById(conversationId);
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
