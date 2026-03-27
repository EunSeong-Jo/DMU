package kr.ac.dongyang.website.jspwebsite.utils;

import java.text.SimpleDateFormat;
import java.util.Date;

public class DateUtils {

    /**
     * long 시각을 문자열로 리턴하는 함수
     */
    public static String toDateString(long value) {
        Date date = new Date(value);
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        return formatter.format(date);
    }

}
