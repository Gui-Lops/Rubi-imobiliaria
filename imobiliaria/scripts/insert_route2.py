from pathlib import Path
p=Path('loja/urls.py')
s=p.read_text()
if "path('imoveis/'" in s:
    print('already')
else:
    old="    path('propriedades/<int:pk>/', views.property_detail, name='property_detail'),\n]"
    new="    path('imoveis/', views.all_properties, name='all_properties'),\n    path('propriedades/<int:pk>/', views.property_detail, name='property_detail'),\n]"
    if old in s:
        s=s.replace(old,new)
        p.write_text(s)
        print('inserted')
    else:
        print('pattern not found')
