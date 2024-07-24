package com.gaorch.demo02.mapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaorch.demo02.entity.Conversation;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ConversationMapper extends BaseMapper<Conversation>
{
    @Select("select * from conversation where userId = #{userId}")
    public List<Conversation> selectByUserId(Integer userId);

    @Options(useGeneratedKeys = true, keyProperty = "id")
    @Insert("insert into conversation (userId, name, ifUseLib, libId) values (#{userId},#{name},#{ifUseLib},#{libId})")
    public int insert(Conversation conversation);

    @Select("select * from conversation where id = #{id}")
    public Conversation selectById(Integer id);
}
