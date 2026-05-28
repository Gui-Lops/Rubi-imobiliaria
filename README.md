# Rubi-imobiliaria

Um projeto Django para gestão e exibição de imóveis com upload de imagens múltiplas, tipos de imóvel e painel administrativo.

## Requisitos

- Python 3.14+
- pip
- Virtualenv (recomendado)

## Instalação

1. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute as migrações:

```bash
cd imobiliaria
python manage.py migrate
```

4. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

5. Acesse o site em:

```text
http://127.0.0.1:8000/
```

## Configurações de mídia

Durante o desenvolvimento, arquivos de imagem enviados serão salvos na pasta `media/`.

## Funcionalidades

- Cadastro de imóveis com campos de título, localização, preço, tipo, descrição e status de publicação
- Upload múltiplo de imagens para cada imóvel
- Visualização detalhada do imóvel com galeria de imagens
- Painel administrativo para listar, editar e excluir imóveis

## Observações

- Se precisar criar um usuário administrador, use:

```bash
python manage.py createsuperuser
```

- Garanta que o diretório `media/` exista e tenha permissão de escrita durante o desenvolvimento.
