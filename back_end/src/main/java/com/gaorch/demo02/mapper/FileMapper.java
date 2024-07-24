package com.gaorch.demo02.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaorch.demo02.entity.File;
import org.apache.ibatis.annotations.*;
import org.springframework.web.bind.annotation.DeleteMapping;

import java.util.List;

@Mapper
public interface FileMapper extends BaseMapper<File> {

    @Options(useGeneratedKeys = true, keyProperty = "id")
    @Insert("insert into file (libId, fileName, size, type) values (#{libId},#{fileName},#{size},#{type})")
    public int insert(File myFile);

    @Select("select id, libId, fileName from file where id = #{id}")
    public File getById(Integer id);

    @Select("select * from file where libId = #{libId} ORDER BY date ASC")
    public List<File> getByLibId(Integer libId);

    @Delete("delete from file where libId = #{libId}")
    public int deleteByLibId(Integer libId);

}
