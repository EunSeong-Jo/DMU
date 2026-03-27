package proj_nt;

import java.io.IOException;

public class NoteTaking implements AutoCloseable {

   public NoteTaking (String fPath) throws IOException {
      System.out.println("글을 작성하기 위해, " + fPath + " 파일을 열니다");
   }

   public void writeNT(String note) throws IOException {
      System.out.println(note + "를 파일에 기록(저장) 합니다");
   }
   
   public void close() throws IOException {
      System.out.println("파일을 닫아서 글 작성을 마칩니다.");
   }
   
}