package com.gaorch.demo02.mapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaorch.demo02.entity.Lib;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface LibMapper extends BaseMapper<Lib> {

    @Select("select id, userId, name, size, description from lib where userId = #{userid};")
    public List<Lib> getByUserId(Integer userId);

    @Insert("INSERT INTO lib (userId,name,size,description) values (#{userId},#{name},#{size},#{description})")
    public int insert(Lib lib);

    @Update("update lib set size = #{size} where id = #{id}")
    public int updateSizeById(double size, Integer id);

    @Select("select size from lib where id = #{id}")
    public double selectSizeById(Integer id);

    @Select("select id, userId, name, size, description from lib where id = #{id}")
    public Lib selectById(Integer id);
}
