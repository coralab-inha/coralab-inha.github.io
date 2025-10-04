---
layout: about
title: home
permalink: /
---

<!-- 1.1 연구실 소개 이미지 섹션 -->
<section id="about-lab" class="my-5 text-center">
  <img src="{{ '/assets/img/mainpage.png' | relative_url }}" alt="연구실 소개 이미지" class="img-fluid rounded shadow-sm mt-3" style="max-width: 80%;">
</section>

<hr>

<!-- 1.2 대표 연구 분야 섹션 -->
<section id="research-highlights" class="my-5 text-center">
  <h2>Research Highlights</h2>
  <div class="container mt-4 d-flex flex-column align-items-center">

    <!-- 로보틱스 카드 -->
    <div class="card shadow-sm border-0 mb-4" style="max-width: 800px; width: 100%; padding: 20px;">
      <div class="d-flex flex-row align-items-center" style="min-height: 280px;">
        
        <!-- 이미지 영역 -->
        <div class="img-container d-flex justify-content-center align-items-center" 
             style="width: 45%; height: 100%; padding: 15px;">
          <img src="{{ '/assets/img/prof_pic_color.png' | relative_url }}" 
               alt="로보틱스 연구 이미지"
               class="img-fluid rounded"
               style="height: 70%; width: auto; object-fit: contain;">
        </div>

        <!-- 텍스트 영역 -->
        <div class="card-body text-left" style="width: 55%;">
          <h5 class="card-title">로보틱스 (Robotics)</h5>
          <p class="card-text">지능형 제어 및 협동 로봇을 중심으로 산업 및 서비스 로봇 기술을 연구합니다.</p>
        </div>
      </div>
    </div>

    <!-- 차량 카드 -->
    <div class="card shadow-sm border-0 mb-4" style="max-width: 800px; width: 100%; padding: 20px;">
      <div class="d-flex flex-row align-items-center" style="min-height: 280px;">
        
        <!-- 이미지 영역 -->
        <div class="img-container d-flex justify-content-center align-items-center" 
             style="width: 45%; height: 100%; padding: 15px;">
          <img src="{{ '/assets/img/prof_pic_color.png' | relative_url }}" 
               alt="자율주행 차량 연구 이미지"
               class="img-fluid rounded"
               style="height: 70%; width: auto; object-fit: contain;">
        </div>

        <!-- 텍스트 영역 -->
        <div class="card-body text-left" style="width: 55%;">
          <h5 class="card-title">자율주행 차량 (Autonomous Vehicles)</h5>
          <p class="card-text">지능형 운전 보조, 자율주행 인식 및 판단 알고리즘을 연구합니다.</p>
        </div>
      </div>
    </div>

  </div>
</section>

<hr>

<!-- 1.3 Contact 섹션 -->
<section id="contact" class="my-5 text-center">
  <h2>Address & Contact</h2>
  <p class="mt-3">
    <strong>주소:</strong> 인하대학교 용현캠퍼스 하이테크센터 616호<br>
    <strong>이메일:</strong> <a href="mailto:lab_contact@example.com">lab_contact@example.com</a><br>
    <strong>전화:</strong> 02-123-4567
  </p>
  <a href="https://maps.google.com" target="_blank" class="btn btn-outline-primary mt-2">
    <i class="ti ti-map-pin"></i> 지도 보기
  </a>
</section>
