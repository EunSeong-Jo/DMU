package ch.sec09;

public class Button {
	public static interface CL{
		void onClick();
	}
	
	private CL clickListener;
	
	public void setCL(CL clickListener) {
		this.clickListener = clickListener;
	}
	
	public void click() {
		this.clickListener.onClick();
	}
}
