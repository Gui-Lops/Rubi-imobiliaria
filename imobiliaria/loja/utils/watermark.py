from PIL import Image
from django.conf import settings
import os


def aplicar_marca_dagua(image_path):
    """
    Aplica a logo RubiHaus centralizada na imagem.
    """

    logo_path = os.path.join(
        settings.MEDIA_ROOT,
        "watermark",
        "rubihaus.png"
    )

    print("\n=== MARCA D'ÁGUA ===")
    print("Imagem:", image_path)
    print("Logo:", logo_path)
    print("Logo existe?", os.path.exists(logo_path))

    if not os.path.exists(logo_path):
        print("ERRO: Logo não encontrada!")
        return

    try:
        foto = Image.open(image_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")

        # Logo ocupa 45% da largura da imagem
        largura_logo = int(foto.width * 0.45)

        proporcao = largura_logo / logo.width

        altura_logo = int(
            logo.height * proporcao
        )

        logo = logo.resize(
            (largura_logo, altura_logo),
            Image.LANCZOS
        )

        # Transparência da marca
        alpha = logo.getchannel("A")
        alpha = alpha.point(
            lambda p: int(p * 0.90)
        )

        logo.putalpha(alpha)

        # Centraliza
        pos_x = (foto.width - logo.width) // 2
        pos_y = (foto.height - logo.height) // 2

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

        print("Marca d'água aplicada com sucesso!")

    except Exception as e:
        print("ERRO AO APLICAR MARCA D'ÁGUA:")
        print(str(e))