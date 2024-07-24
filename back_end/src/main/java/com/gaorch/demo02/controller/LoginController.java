package com.gaorch.demo02.controller;

import com.gaorch.demo02.entity.User;
import com.gaorch.demo02.service.LoginService;
import com.gaorch.demo02.utils.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LoginController {

    @Autowired
    private LoginService loginService;

    @PostMapping("/signup")
    public Result signup(@RequestBody User user)
    {
        return loginService.signup(user);
    }

    @PostMapping("/login")
    public Result login(@RequestBody User user)
    {
        return loginService.login(user);
    }

}
