---
layout: about
title: home
permalink: /
---

<!-- 1.1 Lab Introduction Image Section -->
<section id="about-lab" class="my-5 text-center">
<img src="/assets/img/mainpage.png" alt="Lab Introduction Image" class="img-fluid rounded shadow-sm">
</section>

<hr>

<!-- 1.2 Research Highlights Section -->
<section id="research-highlights" class="my-5 text-center">
  <h2>Research Highlights</h2>
  <div class="container mt-4 d-flex flex-column align-items-center">

    <!-- Robotics Card -->
    <div class="card shadow-sm border-0 mb-4" style="max-width: 800px; width: 100%; padding: 20px;">
      <div class="d-flex flex-row align-items-center flex-wrap" style="min-height: 280px;">

        <!-- Image Area -->
        <div class="img-container d-flex justify-content-center align-items-center" 
             style="width: 45%; height: 100%; padding: 15px;">
          <img src="{{ '/assets/img/projects/robot.png' | relative_url }}" 
               alt="Robotics Research Image"
               class="img-fluid rounded shadow-sm"
               style="max-width: 100%; max-height: 240px; object-fit: contain;">
        </div>

        <!-- Text Area -->
        <div class="card-body text-left" style="width: 55%;">
          <h5 class="card-title">Robotics</h5>
          <p class="card-text">
            Our research focuses on intelligent control, human–robot collaboration, and the development of industrial and service robot technologies.
          </p>
        </div>
      </div>
    </div>

    <!-- Autonomous Vehicle Card -->
    <div class="card shadow-sm border-0 mb-4" style="max-width: 800px; width: 100%; padding: 20px;">
      <div class="d-flex flex-row align-items-center flex-wrap" style="min-height: 280px;">

        <!-- Image Area -->
        <div class="img-container d-flex justify-content-center align-items-center" 
             style="width: 45%; height: 100%; padding: 15px;">
          <img src="{{ '/assets/img/projects/autonomous_nav_bg.png' | relative_url }}" 
               alt="Autonomous Vehicle Research Image"
               class="img-fluid rounded shadow-sm"
               style="max-width: 100%; max-height: 240px; object-fit: contain;">
        </div>

        <!-- Text Area -->
        <div class="card-body text-left" style="width: 55%;">
          <h5 class="card-title">Autonomous Vehicles</h5>
          <p class="card-text">
            We study perception, decision-making, and control algorithms for autonomous driving and advanced driver-assistance systems (ADAS).
          </p>
        </div>
      </div>
    </div>

  </div>
</section>

<hr>

<section id="news" class="my-5">
  <div class="container" style="max-width: 800px;">
    <h2 class="text-center">News</h2>
    <div class="mt-4">
      {% include news.liquid limit=5 %}
    </div>
  </div>
</section>

<hr>

<!-- 1.3 Contact Section -->
<section id="contact" class="my-5 text-center">
  <h2>Address & Contact</h2>
  <p class="mt-3">
    <strong>Address:</strong> Room 616, High-Tech Center, Inha University, Yonghyeon Campus<br>
    <strong>Email:</strong> <a href="mailto:lab_contact@example.com">lab_contact@example.com</a><br>
    <strong>Phone:</strong> +82-2-123-4567
  </p>
<a href="https://www.google.com/maps/search/?api=1&query=인하대학교+하이테크센터+616호" 
   target="_blank" 
   class="btn btn-outline-primary mt-2">
  <i class="ti ti-map-pin"></i> View Map
</a>

</section>
