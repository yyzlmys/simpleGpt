package com.gaorch.demo02.service;

import com.gaorch.demo02.entity.Lib;
import com.gaorch.demo02.mapper.FileMapper;
import com.gaorch.demo02.mapper.LibMapper;
import com.gaorch.demo02.mapper.UserMapper;
import com.gaorch.demo02.utils.JwtUtils;
import com.gaorch.demo02.utils.Result;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class LibService {
    @Autowired
    private LibMapper libMapper;

    @Autowired
    private FileMapper fileMapper;

    @Autowired
    HttpServletRequest request;

    private void deleteDirectory(java.io.File folder)
    {
        java.io.File[] files = folder.listFiles();
        if (files != null) {
            for (java.io.File file : files) {
                if (file.isDirectory()) {
                    deleteDirectory(file);
                } else {
                    file.delete();
                }
            }
        }
        folder.delete();
    }

    public Result create(Lib lib)
    {
        Integer userId = JwtUtils.getId(request);
        lib.setUserId(userId);
        lib.setId(0);
        lib.setSize(0);
        libMapper.insert(lib);
        return Result.ok();
    }

    public Result delete(Integer id)
    {
        //windows
        //java.io.File folder=new java.io.File("D:\\shixun\\" + "lib" + id + "\\");

        //linux
        java.io.File folder=new java.io.File("/root/shixun/" + "lib" + id + "/");

        deleteDirectory(folder);
        fileMapper.deleteByLibId(id);
        libMapper.deleteById(id);
        return Result.ok();
    }

    public Result list()
    {
        Integer userId = JwtUtils.getId(request);
        List<Lib> libs = libMapper.getByUserId(userId);
        return Result.ok(libs);
    }

    public Result get(Integer id)
    {
        Lib lib = libMapper.selectById(id);
        return Result.ok(lib);
    }

    public void deleteByUserId(Integer userId)
    {
        List<Lib> libs = libMapper.getByUserId(userId);
        for(Lib lib: libs)
        {
            delete(lib.getId());
        }
    }
}
