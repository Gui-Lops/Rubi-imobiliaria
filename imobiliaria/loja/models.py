from django.db import models
from PIL import Image
from django.conf import settings
import os


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
    property = models.ForeignKey(
        Property,
        related_name='images',
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='property_images/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Imagem de {self.property.title}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        try:
            image_path = self.image.path

            logo_path = os.path.join(
                settings.MEDIA_ROOT,
                'watermark',
                'rubihaus.png'
            )

            if not os.path.exists(logo_path):
                return

            foto = Image.open(image_path).convert("RGBA")
            logo = Image.open(logo_path).convert("RGBA")

            nova_largura = int(foto.width * 0.45)

            proporcao = nova_largura / logo.width

            nova_altura = int(
                logo.height * proporcao
            )

            logo = logo.resize(
                (nova_largura, nova_altura),
                Image.LANCZOS
            )

            alpha = logo.getchannel("A")
            alpha = alpha.point(
                lambda p: int(p * 0.12)
            )

            logo.putalpha(alpha)

            pos_x = (
                foto.width - logo.width
            ) // 2

            pos_y = (
                foto.height - logo.height
            ) // 2

            camada = Image.new(
                "RGBA",
                foto.size,
                (255, 255, 255, 0)
            )

            camada.paste(
                logo,
                (pos_x, pos_y),
                logo
            )

            resultado = Image.alpha_composite(
                foto,
                camada
            )

            resultado.convert("RGB").save(
                image_path,
                quality=95
            )

        except Exception as e:
            print("Erro ao aplicar marca d'água:", e)