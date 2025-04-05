package kr.ac.dongyang.webproject.day0404;

public class HtmlUtils {

    public  static String selectBox(int start, int end, String name) {

        StringBuilder sb = new StringBuilder();
        sb.append("<select name=\"%s\">".formatted(name));
        sb.append("<option>선택</option>");

        for (int i = start; i <= end; i++) {
            sb.append("<option value=" + i + ">" + i + "</option>");
        }

        sb.append("</select>");

        return sb.toString();
    }

    public static String itemList(String[] items) {
        StringBuilder sb = new StringBuilder();
        sb.append("<ul>");
        for (String item : items) {
            sb.append("<li>" + item + "</li>");
        }
        sb.append("</ul>");

        return sb.toString();
    }

}
