package com.gaorch.demo02.controller;

import com.gaorch.demo02.entity.User;
import com.gaorch.demo02.service.PersonalService;
import com.gaorch.demo02.utils.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.ServletRequestBindingException;
import org.springframework.web.bind.annotation.*;

@RestController
public class PersonalController {

    @Autowired
    private PersonalService personalService;

    @GetMapping("/getInfo")
    public Result getInfo() {
        return personalService.getInfo();
    }

    @PutMapping("/changePassword")
    public Result changePassword(@RequestBody User user) {
        return personalService.changePassword(user);
    }

    @PutMapping("/changeUsername/{username}")
    public Result changeUsername(@PathVariable String username) {
       return personalService.updateUsername(username);
    }

    @DeleteMapping("/user")
    public Result delete()
    {
        return personalService.delete();
    }
}
