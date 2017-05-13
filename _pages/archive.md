---
layout: default
title: Archive
permalink: /archive/
order: 3
robots_index: False
paginate:
  limit: false
  per_page: 9
---

<div class="home">

  <h1 class="page-heading">Archive{% if paginator %} - Page {{ paginator.page }} of {{ paginator.total_pages }}{% endif %}</h1>

    <!-- BEGIN BLOG -->
    <div class="row">
        {% for post in paginator.posts %}
        <article class="col-md-4 col-sm-6 post-thumb">
            <a href="{{ post.url }}">
                <figure class="blog-thumb">
<!--                <img src="{% if post.carousel %}{{ post.carousel }}{% else %}/img/carousel/fullimage1.jpg{% endif %}" alt="{{ post.description }}" {% if post.description %}title="{{ post.description }}"{% endif %}>
    -->
 <img src="{% if post.carousel %}{{ post.carousel }}{% else %}/img/carousel/fullimage1.jpg{% endif %}" alt="{% if post.blurb %}{{ post.blurb }}{% else %}{{  post.description }}{% endif %}" title="{% if post.blurb %}{{ post.blurb }}{% else %}{{ post.description }}{% endif %}">
            </figure>
            </a>
            <div class="post-area">
                <a href="{{ post.url }}">
                    <h4>{{ post.title }}</h4>
                </a>
                <p class="post-info"><span class="glyphicon glyphicon-time"></span> {{ post.date | date: "%b %-d, %Y" }} | <a href="{{ site.url }}{{ post.url }}#comments">Comments <span class="badge"><fb:comments-count href="{{ site.url }}{{ post.url }}"></fb:comments-count></span></a><!--{% if post.rating %} | <i>{{ post.rating}}/100</i>{% endif %}--><br />
                <!--{{post.content|strip_html|truncate:110}}-->{% if post.blurb %}{{ post.blurb }}{% else %}{{post.content|strip_html|truncate:110}}{% endif %}</p>
                
                <div class="bottom-right"><a class="btn btn-primary btn-xs" href="{{ post.url }}">Read More</a></div>
            </div>
        </article>
        {% endfor %}
    </div>
    <!-- END BLOG -->
    <!-- BLOG NAVIGATION -->
    <div class="row row-centered">
        <div class="col-md-4 col-sm-6 col-centered">
            <div class="btn-group btn-group-justified">
                {% if paginator.previous_page %}<a href="{{ paginator.previous_page_path }}" class="btn btn-primary">< Newer Posts</a>{% endif %}
                <a href="/" class="btn btn-primary">Home</a>
                {% if paginator.next_page %}<a href="{{ paginator.next_page_path }}" class="btn btn-primary">Older Posts ></a>{% endif %}
            </div>
        </div>
    </div>
    <!-- BLOG NAVIGATION -->

  <p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>

</div>