from bs4 import BeautifulSoup
import requests
import json
import os

#QUANTIDADE DE PAGINAS POR PRODUTO (RECOMENDO 5 OU MENOS)
QUANTIDADE_PAGINAS = 5

#QUANTIDADE DE PRODUTOS A BUSCAR (MAXIMO 260)
QUANTIDADE_PRODUTOS = 200

pesquisa = input('DIGITE A PESQUISA: ')
pesquisa = pesquisa.replace(' ', '-')

r = requests.get(f'https://br.shein.com/pdsearch/{pesquisa}/')
produto = 1
soup = BeautifulSoup(r.text, 'lxml')
for a in soup.find_all('a', href=True)[30:][:30+QUANTIDADE_PRODUTOS]:

    r = requests.get('https://br.shein.com/' + a['href'])

    soup = BeautifulSoup(r.text, 'lxml')
    codigo = soup.find('script',{'data-id':'criteo-productDetail'}).text.split('\n')
    codigo = codigo[4].replace("item: '", '')
    codigo = codigo.replace("        ", '')
    codigo = codigo[1:][:12]
    offset = 20
    for page in range(1, QUANTIDADE_PAGINAS+1):
        
        print(f'=======PRODUTO {produto} - PAGINA {page}==========')
        
        response = requests.get(f'https://br.shein.com/goods_detail_nsw/getCommentInfoByAbc?_lang=pt-br&_ver=1.1.8&goods_id=&is_picture=&limit=20&offset={offset}&page=1&rule_id=recsrch_sort%3AA&shop_id=&size=&sort=&spu={codigo}&tag_id=')

        offset += 20

        response = json.loads(response.text)
        if response['info']['commentInfoTotal'] == 0:
            print('NENHUMA IMAGEM')
        else:
            
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
    produto += 1        
