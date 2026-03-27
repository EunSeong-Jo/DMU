package ch.sec09;

public class ButtonEX {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Button bttnOk = new Button();
		
		class OkListener implements Button.CL{
			@Override
			public void onClick() {
				System.out.println("click ok button.");
			}
		}
		
		bttnOk.setCL(new OkListener());
		
		bttnOk.click();
		
		Button bttnCancel = new Button();
		
		class CCL implements Button.CL{
			@Override
			public void onClick() {
				System.out.println("click cancel button.");
			}
		}
		
		bttnCancel.setCL(new CCL());
		
		bttnCancel.click();
	}
}
