package com.gaorch.demo02.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaorch.demo02.entity.Robot;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface RobotMapper extends BaseMapper<Robot>
{
    @Insert("insert into robot (userId, name, prompt, intro) values (#{userId}, #{name}, #{prompt}, #{intro})")
    public int insert(Robot robot);

    @Select("select * from robot where userId = #{userId} or userId = 1")
    public List<Robot> selectByUserId(Integer userId);

    @Select("select * from robot where id = #{id}")
    public Robot selectById(Integer id);

    @Delete("delete from robot where userId = #{userId}")
    public int deleteByUserId(Integer userId);
}
