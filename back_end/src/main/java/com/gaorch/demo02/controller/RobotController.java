package com.gaorch.demo02.controller;

import com.gaorch.demo02.entity.Robot;
import com.gaorch.demo02.service.RobotService;
import com.gaorch.demo02.utils.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/robot")
public class RobotController
{
    @Autowired
    private RobotService robotService;

    @PostMapping("")
    public Result create(@RequestBody Robot robot)
    {
        return robotService.create(robot);
    }

    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id)
    {
        return robotService.delete(id);
    }

    @GetMapping("/list")
    public Result list()
    {
        return robotService.list();
    }

    @GetMapping("/{id}")
    public Result get(@PathVariable Integer id)
    {
        return robotService.get(id);
    }
}
