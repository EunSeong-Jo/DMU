package com.example.hw2_8;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Step1 + Step2
        EditText et1 = findViewById(R.id.ET1);

        // Step3
        et1.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                // 텍스트가 입력되기 전에는 아무 동작이 없음
            }

            @Override
            // 실시간 처리
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                // 텍스트가 입력되면 해당 텍스트 정보를 input 변수에 저장
                String input = s.toString();
                // input 변수가 비어있지 않는다면 (변수 내에 값이 있다면) 해당 값을 Toast 메세지로 보여줌
                if (!input.isEmpty()) {
                    Toast.makeText(getApplicationContext(), input, Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void afterTextChanged(Editable s) {
                // 텍스트 입력이 끝난 뒤에도 아무 동작이 없음
            }
        });
    }
}