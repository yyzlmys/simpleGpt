package com.gaorch.demo02.mapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaorch.demo02.entity.Message;
import com.gaorch.demo02.utils.PasswordUtils;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface MessageMapper extends BaseMapper<Message>
{
    @Select("SELECT * from message WHERE conversationId = #{conversationId} ORDER BY date DESC LIMIT 1;")
    public Message selectLastByConversationId(Integer conversationId);

    @Insert("insert into message (conversationId, isPerson, content) values (#{conversationId},#{isPerson},#{content})")
    public int insert(Message message);

    @Delete("delete from message where conversationId = #{conversationId}")
    public int deleteByConversationId(Integer conversationId);

    @Select("select * from message where conversationId = #{conversationId} ORDER BY date ASC")
    public List<Message> selectByConversationId(Integer conversationId);

    @Select("select * FROM ( SELECT * FROM message where conversationId = #{conversationId} ORDER BY date DESC LIMIT #{num} ) AS subquery ORDER BY date ASC;")
    public List<Message> selectLastMessagesByConversationId(Integer conversationId, Integer num);
}
