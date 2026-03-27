package proj_nt;

import java.io.IOException;

public class NTmain2 {

   public static void main(String[] args) {
	   
	   // 1. 객체를 try 괄호 안에서 선언
	   // 2. AutoCloseable을 구현 (NoteTaking.java)
      try (NoteTaking nt = new NoteTaking("notes.txt")) {
          nt.writeNT("This is the first writing in this notes");
      } catch (IOException e) {
          e.printStackTrace();
      }
      // try 구문이 끝나면 close() 구문이 없어도 자동해제
   }
}
