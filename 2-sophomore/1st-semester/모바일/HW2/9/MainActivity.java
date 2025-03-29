package com.example.hw2_9;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;

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
        LinearLayout rotateButton = findViewById(R.id.rotateButton);
        ImageView mainImg = findViewById(R.id.mainImg);

        // Step3
        rotateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            // rotateButton 객체를 클릭 했을 경우
            public void onClick(View v) {
                // getRotation() : float형 메소드, 현재의 회전값을 가져옴
                float Rotate = mainImg.getRotation();
                // 클릭할 때 마다 현재 회전값에 10도씩 더해서 저장
                float newRotate = Rotate + 10;
                // 10도가 더해진 회전값을 mainImg에 적용
                mainImg.animate().rotation(newRotate);
            }
        });

        // 상태바, 네비게이션바까지 화면을 적용할지 여부
        EdgeToEdge.enable(this);
        // 작성한 앱이 시스템 UI와 곂칠 수 있음으로 자체적으로 패딩을 추가해 사전에 방지
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }
}