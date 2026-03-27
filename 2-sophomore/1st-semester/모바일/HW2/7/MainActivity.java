package com.example.hw2_7;

import android.os.Bundle;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {
    // Step1
    TextView title1;
    CheckBox chkEn, chkClick, chk45;
    Button btn1;

    @Override
    // onCreate : 화면 표시를 위해 앱 실행시 제일 먼저 호출 되는 함수
    protected void onCreate(Bundle savedInstanceState) {
        // Bundle : 키와 값을 쌍으로 담을 수 있는 객체 (딕셔너리)
        // savedInstanceState : UI의 상태 정보를 담고 있는 Bundle 객체 (전원, 회전 등의 외부 영향으로 부터 앱의 지속성을 유지)
        super.onCreate(savedInstanceState);
        // setContentView : 출력될 XML파일(뷰) 지정
        setContentView(R.layout.activity_main);

        // Step2
        // R : Resource(리소스)
        // findViewById : 해당 id 값을 가지고 있는 객체를 가져옴
        title1 = (TextView) findViewById(R.id.Title1);
        chkEn = (CheckBox) findViewById(R.id.ChkEn);
        chkClick = (CheckBox) findViewById(R.id.ChkClick);
        chk45 = (CheckBox) findViewById(R.id.Chk45);
        btn1 = (Button) findViewById(R.id.Btn1);

        // Step3
        chkEn.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // 체크 상태로 바뀌면 버튼의 활성화 여부를 현재의 체크 상태(True)로 변경
                btn1.setEnabled(isChecked);
            }
        });

        chkClick.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // 체크 상태로 바뀌면 버튼의 클릭 여부를 현재의 체크 상태(True)로 변경
                btn1.setClickable(isChecked);
            }
        });

        chk45.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // 체크 상태로 바뀌면 버튼의 회전 상태를 45도로 변경
                if (chk45.isChecked()){
                    btn1.setRotation(45);
                }
                // 체크 상태가 풀리면 버튼의 회전 상태를 0도로 변경
                else {
                    btn1.setRotation(0);
                }
            }
        });
    }
}