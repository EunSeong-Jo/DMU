package Day0526;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Scanner;

public class AddrMain {
    
    static Scanner sc = new Scanner(System.in);
    static ArrayList<Addr> addlist = new ArrayList<Addr>();
    
    public static void main(String[] args) {
        while(true) {
            System.out.println("-------------");
            System.out.println("1. 주소록 입력");
            System.out.println("2. 주소록 검색");
            System.out.println("3. 주소록 전체 조회");
            System.out.println("4. 주소록 수정");
            System.out.println("5. 주소록 삭제");
            System.out.println("0. 종료");
            System.out.println("-------------");
            System.out.print("메뉴를 입력하세요: ");
            int in = sc.nextInt(); 
            
            switch (in) {
            case 1:
                addrInput();
                break;
            case 2:
                addrSearch();
                break;
            case 3:
                addrJohoi();
                break;
            case 4:
                addrUpdate();
                break;
            case 5:
                addrDelete();
                break;
            case 0:
                System.out.println("종료");
                sc.close();
                return;
            default:
                System.out.println("잘못된 입력입니다. 다시 입력하세요.");
            }
        }
    }
    
    // 입력
    public static void addrInput() {
        System.out.print("이름을 입력하세요: ");
        String name = sc.next();
        
        System.out.print("전화번호를 입력하세요: ");
        String tel = sc.next();
        
        System.out.print("회사 이름을 입력하세요: ");
        String com = sc.next();
        
        LocalDateTime createDate = LocalDateTime.now();
        
        Addr addr = new Addr(name, tel, com, createDate);
        addlist.add(addr);
    }
    
    // 검색
    static private void addrSearch() {
        System.out.print("검색할 이름을 입력하세요. (like검색): ");
        String name = sc.next();
        
        for (Addr addr : addlist) {
            if (addr.getName().contains(name)) {
                System.out.println(addr);
            }
        }
    }

    // 전체 조회
    static void addrJohoi() {
        for (int i = 0; i < addlist.size(); i++) {
            System.out.println(addlist.get(i));
        }
    }

    // 수정
    static void addrUpdate() {
        System.out.print("수정할 이름을 입력하시오: ");
        String name = sc.next();
        
        for (Addr addr : addlist) {
            if (addr.getName().equals(name)) {
                System.out.print("새 전화번호를 입력하세요: ");
                String tel = sc.next();
                
                System.out.print("새 회사명을 입력하세요: ");
                String com = sc.next();
                
                addr.setTel(tel);
                addr.setCom(com);
                addr.setCreateDate(LocalDateTime.now());
                
                System.out.println("주소록이 수정되었습니다.");
                break;
            }
        }
    }

    // 삭제
    static void addrDelete() {
        System.out.print("삭제할 이름을 입력하시오: ");
        String name = sc.next();

        for (int i = 0; i < addlist.size(); i++) {
            if (addlist.get(i).getName().equals(name)) {
                addlist.remove(i);
                System.out.println("주소록이 삭제되었습니다.");
                break;
            }
        }
    }
    
}