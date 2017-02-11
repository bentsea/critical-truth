---
layout: default
permalink: /
---

<div class="home">

  <h1 class="page-heading">Latest Reviews</h1>

  <div id="home-slider" class="owl-carousel">
    {% for post in site.posts limit:10 %}
    <div class="item" {% if forloop.first %}style="display:block; background: url('{{ post.carousel }}');"{% endif %}>
      <a href="{{ post.url }}">
        <div class="slide-text">
          <h2><span>{{ post.title }}</span></h2>
          <span class="slide-blurb"><span>{{ post.blurb }}</span></span>
        </div>
        <div class="slide-image">
          <img {% unless forloop.first %}class="lazyOwl" data-src="{{ post.carousel }}"{% endunless %}{% if forloop.first %}src="{{ post.carousel }}"{% endif %} alt="{{ post.title }}">
        </div>
      </a>
    </div>
    {% endfor %}
  </div>

  <!--
  {% assign this_years_posts = site.array %}
  {% for post in site.categories.reviews %}
    {% capture this_year %}{{ post.date | date: "%Y" }}{% endcapture %}
    {% if this_year == '2016' %}
      {% assign this_years_posts = this_years_posts | push: post %}
    {% endif %}
  {% endfor %}
  {% assign sorted = this_years_posts | sort: 'rating' | reverse %}
  {% for item in sorted limit: 10 %}
    <p><a href="{{ item.url }}">{{ item.title }}</a></p>
  {% endfor %}
  -->
  <p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>

</div>
