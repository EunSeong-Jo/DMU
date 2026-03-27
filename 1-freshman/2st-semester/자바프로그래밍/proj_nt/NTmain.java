package proj_nt;

import java.io.IOException;

public class NTmain {

   public static void main(String[] args) {
	  
	  NoteTaking nt = null;
      
      try {
    	  nt = new NoteTaking("notes.txt");

          nt.writeNT("This is the first wrting in this notes");
      }
      catch (IOException e) {
          e.printStackTrace();
     }
      finally { 
          try {
        	  nt.close();
         }
          catch (IOException e) { 
        	  
         }
      }
   }
}