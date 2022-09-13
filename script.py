from bs4 import BeautifulSoup
import requests
import json
import os

pesquisa = input('DIGITE A PESQUISA: ')
pesquisa = pesquisa.replace(' ', '-')

r = requests.get(f'https://br.shein.com/pdsearch/{pesquisa}/')

soup = BeautifulSoup(r.text, 'lxml')
for a in soup.find_all('a', href=True)[30:][:50]:

    r = requests.get('https://br.shein.com/' + a['href'])

    soup = BeautifulSoup(r.text, 'lxml')
    codigo = soup.find('script',{'data-id':'criteo-productDetail'}).text.split('\n')
    codigo = codigo[4].replace("item: '", '')
    codigo = codigo.replace("        ", '')
    codigo = codigo[1:][:12]

    response = requests.get(f'https://br.shein.com/goods_detail_nsw/getCommentInfoByAbc?_lang=pt-br&_ver=1.1.8&goods_id=&is_picture=&limit=20&offset=0&page=1&rule_id=recsrch_sort%3AA&shop_id=&size=&sort=&spu={codigo}&tag_id=')

    response = json.loads(response.text)
    contador = 1
    for i in response['info']['commentInfo']:
        for y in (range(len(i['comment_image']))):
            imagem = i['comment_image'][y]

            imageURL = 'https://img.shein.com/' + imagem['member_image_original']

            if not os.path.exists(pesquisa):
                os.makedirs(pesquisa)
            
            img_data = requests.get(imageURL).content
            with open(pesquisa + '/' + imagem['member_image_original'][20:], 'wb') as handler:
                handler.write(img_data)
            
            print('BAIXANDO IMAGEM: ', contador)
            contador += 1
    
    print('===========PROXIMO PRODUTO==========')

