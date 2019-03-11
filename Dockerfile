FROM php:7.2.15-apache
EXPOSE 80
COPY web/ /var/www/html
RUN a2enmod rewrite
RUN a2enmod headers
