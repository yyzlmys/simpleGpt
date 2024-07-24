package com.gaorch.demo02.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaorch.demo02.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface UserMapper extends BaseMapper<User> {
    @Select("SELECT * FROM user WHERE username = #{username}")
    public User selectByUsername(String username);

    @Select("SELECT id FROM user WHERE username = #{username}")
    public Integer getIdByUsername(String username);

    @Select("SELECT username FROM user WHERE id = #{id}")
    public String getUsernameById(Integer id);

    @Update("update user set username = #{username} where id = #{id}")
    public int updateUsernameById(String username, Integer id);
}