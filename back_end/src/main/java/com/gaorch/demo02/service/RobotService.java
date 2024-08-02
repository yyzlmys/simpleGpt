package com.gaorch.demo02.service;

import com.gaorch.demo02.entity.Robot;
import com.gaorch.demo02.mapper.RobotMapper;
import com.gaorch.demo02.utils.JwtUtils;
import com.gaorch.demo02.utils.Result;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RobotService
{
    @Autowired
    private RobotMapper robotMapper;

    @Autowired
    private HttpServletRequest request;

    public Result create(Robot robot)
    {
        Integer userId = JwtUtils.getId(request);
        robot.setUserId(userId);
        robot.setId(0);
        robotMapper.insert(robot);
        return Result.ok();
    }

    public Result delete(Integer id)
    {
        robotMapper.deleteById(id);
        return Result.ok();
    }

    public Result list()
    {
        Integer userId = JwtUtils.getId(request);
        List<Robot> robots = robotMapper.selectByUserId(userId);
        return Result.ok(robots);
    }
}















