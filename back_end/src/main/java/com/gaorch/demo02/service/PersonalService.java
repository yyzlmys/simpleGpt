package com.gaorch.demo02.service;

import com.gaorch.demo02.entity.Lib;
import com.gaorch.demo02.entity.User;
import com.gaorch.demo02.mapper.LibMapper;
import com.gaorch.demo02.mapper.UserMapper;
import com.gaorch.demo02.utils.JwtUtils;
import com.gaorch.demo02.utils.PasswordUtils;
import com.gaorch.demo02.utils.Result;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PersonalService
{
    @Autowired
    private UserMapper userMapper;

    @Autowired
    private HttpServletRequest request;     //用于解析请求头中的token

    @Autowired
    private ConversationService conversationService;

    @Autowired
    private LibService libService;

    public Result getInfo()
    {
        String username = JwtUtils.getUserName(request);
        User user = userMapper.selectByUsername(username);
        return Result.ok(user);
    }

    public Result changePassword(User user)
    {
        String username = JwtUtils.getUserName(request);
        String password = user.getPassword();
        User selectUser = userMapper.selectByUsername(username);
        selectUser.setSalt(PasswordUtils.generateSalt());
        selectUser.setPassword(PasswordUtils.hashPassword(password, selectUser.getSalt()));
        userMapper.updateById(selectUser);
        return Result.ok();
    }

    public Result updateUsername(String username)
    {
        Integer id = JwtUtils.getId(request);
        userMapper.updateUsernameById(username, id);
        return Result.ok();
    }

    public Result delete()
    {
        Integer id = JwtUtils.getId(request);
        userMapper.deleteById(id);
        libService.deleteByUserId(id);
        conversationService.deleteByUserId(id);
        return Result.ok();
    }

}
