package com.gaorch.demo02.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;


@Data
public class File
{
    private Integer id;
    private Integer libId;
    private MultipartFile file;
    private String fileName;
    private double size;
    private String date;
    private String type;
}
