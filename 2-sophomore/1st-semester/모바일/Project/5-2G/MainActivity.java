package com.example.project5_2g;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    EditText edit1, edit2;
    Button btnAdd, btnSub, btnMul, btnDiv;
    TextView textResult;
    Button[] numButtons = new Button[10];
    Integer[] numBtnIDs = {
            R.id.BtnNum0, R.id.BtnNum1, R.id.BtnNum2, R.id.BtnNum3,
            R.id.BtnNum4, R.id.BtnNum5, R.id.BtnNum6, R.id.BtnNum7,
            R.id.BtnNum8, R.id.BtnNum9
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        setTitle("그리드 레이아웃 계산기");

        // 뷰 바인딩
        edit1 = findViewById(R.id.Edit1);
        edit2 = findViewById(R.id.Edit2);

        btnAdd = findViewById(R.id.BtnAdd);
        btnSub = findViewById(R.id.BtnSub);
        btnMul = findViewById(R.id.BtnMul);
        btnDiv = findViewById(R.id.BtnDiv);

        textResult = findViewById(R.id.TextResult);

        // 연산 버튼 이벤트 설정
        btnAdd.setOnClickListener(v -> calculate('+'));
        btnSub.setOnClickListener(v -> calculate('-'));
        btnMul.setOnClickListener(v -> calculate('*'));
        btnDiv.setOnClickListener(v -> calculate('/'));

        // 숫자 버튼 이벤트 설정
        for (int i = 0; i < numBtnIDs.length; i++) {
            final int index = i;
            numButtons[i] = findViewById(numBtnIDs[i]);
            numButtons[i].setOnClickListener(v -> {
                if (edit1.isFocused()) {
                    edit1.append(numButtons[index].getText());
                } else if (edit2.isFocused()) {
                    edit2.append(numButtons[index].getText());
                } else {
                    Toast.makeText(getApplicationContext(), "먼저 입력창을 선택하세요", Toast.LENGTH_SHORT).show();
                }
            });
        }

        // 인셋 처리
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    // 계산 메서드
    private void calculate(char operator) {
        String num1Str = edit1.getText().toString();
        String num2Str = edit2.getText().toString();

        if (num1Str.isEmpty() || num2Str.isEmpty()) {
            Toast.makeText(this, "값을 입력해주세요", Toast.LENGTH_SHORT).show();
            return;
        }

        try {
            int num1 = Integer.parseInt(num1Str);
            int num2 = Integer.parseInt(num2Str);
            int result;

            switch (operator) {
                case '+': result = num1 + num2; break;
                case '-': result = num1 - num2; break;
                case '*': result = num1 * num2; break;
                case '/':
                    if (num2 == 0) {
                        Toast.makeText(this, "0으로 나눌 수 없습니다", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    result = num1 / num2; break;
                default: return;
            }

            textResult.setText("계산 결과 : " + result);
        } catch (NumberFormatException e) {
            Toast.makeText(this, "숫자를 정확히 입력하세요", Toast.LENGTH_SHORT).show();
        }
    }
}
