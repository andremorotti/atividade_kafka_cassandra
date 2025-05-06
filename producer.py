from kafka import KafkaProducer
from faker import Faker
import json
from datetime import datetime
import random
import time

kafka_bootstrap_servers = 'localhost:9092'
topic_name = 'vendas-ecommerce'

fake = Faker('pt_BR')

magic_cartas = [
    "Dragão Ancião Nicol Bolas",
    "Anjo Exarca da Paz",
    "Demônio da Ruína Cósmica",
    "Hidra Primordial",
    "Esfinge Enigmática",
    "Guerreiro Felino Selvagem",
    "Elfo da Floresta Sombria",
    "Mago da Centelha Novata",
    "Clérigo da Luz Radiante",
    "Ladino das Sombras Silenciosas",
    "Golem de Ferro Forjado",
    "Elemental da Tempestade Furiosa",
    "Zumbi Errante Faminto",
    "Vampiro Aristocrata Sanguinário",
    "Lobisomem da Lua Crescente",
    "Ave de Rapina Veloz",
    "Serpente Marinha Gigante",
    "Aranha da Teia Venenosa",
    "Troll da Ponte Rústica",
    "Ciclope de Um Olho Só",
    "Fênix das Cinzas Eternas",
    "Basilisco de Olhar Petrificante",
    "Quimera de Três Cabeças",
    "Grifo Real Majestoso",
    "Minotauro Furioso Batedor",
    "Centauro Arqueiro Habilidoso",
    "Sátiro Flautista Travesso",
    "Ninfa da Fonte Serena",
    "Dríade da Árvore Antiga",
    "Ent da Floresta Guardiã"
]

def gerar_venda():
    pedido_id = fake.uuid4()
    cpf_cliente = fake.cpf()
    qtd_produtos = random.randint(1, 5)
    produtos_comprados = []
    valor_total = 0.0

    for _ in range(qtd_produtos):
        nome_carta = random.choice(magic_cartas)
        quantidade = random.randint(1, 3)
        preco = round(random.uniform(5.0, 50.0), 2)
        produtos_comprados.append({"nome": nome_carta, "quantidade": quantidade, "preco_unitario": preco})
        valor_total += quantidade * preco

    venda_data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return {
        "id_ordem": pedido_id,
        "documento_cliente": cpf_cliente,
        "produtos_comprados": produtos_comprados,
        "valor_total_venda": round(valor_total, 2),
        "data_hora_venda": venda_data
    }

def msg_dados_venda(producer):
    dados_venda = gerar_venda()
    try:
        producer.send(topic_name, json.dumps(dados_venda).encode('utf-8'))
        print(f"Mensagem enviada: {dados_venda}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
    try:
        for _ in range(10):
            msg_dados_venda(producer)
            time.sleep(2)
    finally:
        producer.close()