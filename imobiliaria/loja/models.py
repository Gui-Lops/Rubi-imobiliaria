from django.db import models


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('APARTAMENTO', 'Apartamento'),
        ('CASA', 'Casa'),
        ('COBERTURA', 'Cobertura'),
        ('TERRENO', 'Terreno'),
        ('COMERCIAL', 'Comercial'),
    ]

    title = models.CharField(max_length=220)
    location = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='APARTAMENTO')
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def main_image_url(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return self.image_url or ''


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem de {self.property.title}"