import pandas as pd
import requests
import json
import openai

# API ViaCEP - Para buscar as informações de endereço

cep_api_url = 'https://viacep.com.br'

#Chat GPT API

openai_api_key = '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'
openai.api_key = openai_api_key

# Configuração Local

input_csv_filename = 'enderecos.csv'
output_csv_filename = 'slogans.csv'

# Variáveis Globais

enderecos = []

# Funções da fase de Extração

def formata_CEP(cep:str): 
    cep = cep.replace('-','')
    return cep

def formata_endereco(*,endereco,numero=None):
    endereco_obj = {
        'logradouro': endereco['logradouro'],
        'numero' : numero,
        'bairro' : endereco['bairro'],
        'cidade' : endereco['localidade'],
        'estado' : endereco['uf'],
        'slogan' : []
    }
    return endereco_obj

def get_address(cep):
    response = requests.get(f'{cep_api_url}/ws/{cep}/json/')
    return response.json() if response.status_code == 200 else None

def le_csv_saida(filename):
    df = pd.read_csv(output_csv_filename)
    logradouros = df['logradouro']
    numeros = df['numero']
    bairros = df['bairro']
    cidades = df['cidade']
    estados = df['estado']
    slogans = df['slogan']

    for index,cidade in enumerate(cidades):
        print("\n----------------------------------------")
        print(f"Cidade: {cidade}/{estados[index]}")
        print(f"Slogan: {slogans[index]}")
        if pd.isna(numeros[index]) is False:
            print(f"Endereço da Prefeitura: {logradouros[index]}, {int(numeros[index])} - Bairro {bairros[index]}")
        print("----------------------------------------")
    
def extraction(*,filename):  
    df = pd.read_csv(filename)
    ceps = df['CEP'].tolist()
    numeros = df['numero'].tolist()
    ceps = [cep_return:=formata_CEP(cep) for cep in ceps]
    enderecos = [endereco := get_address(cep) for cep in ceps]
    enderecos = [endereco_return := formata_endereco(endereco=endereco,numero=numeros[enderecos.index(endereco)]) for endereco in enderecos]
    return enderecos

# Funções da fase de Transformação

def generate_ai_message(cidade):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
      {
          "role": "system",
          "content": "você é um promotor de turismo da cidade"
      },
      {
          "role": "user",
          "content": f"Crie um slogan para a cidade {cidade} sem mencionar o nome da cidade.(maximo de 200 caracteres para cada cidade e sem emoji)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')
  
def transformation(*,enderecos,index):
    slogan = generate_ai_message(enderecos[index]['cidade'])
    enderecos[index]['slogan'].append(slogan)
    return enderecos[index]

# Funções da fase de Carregamento (Load)

def load(*,endereco,filename):
    dados = pd.DataFrame(endereco)
    dados.to_csv(filename,header=False,sep=',',index=False,mode='a')

# MAIN

def main(enderecos):
    print("\n========================================")
    print("\nBEM VINDA(O)!")
    while True:
        print("\n========================================")
        print("\nEscolha a ação desejada para gerar o slogan da cidade.\n")
        print("1) Digitar o CEP.")
        print("2) Selecionar CEP do arquivo csv.")
        print("3) Ver slogans gerados.")
        print("x) Sair\n")
        opcao = input("Digite opção desejada: ")

        if opcao == '1':
            input_cep = input("Digite o cep desejado: ")
            endereco = get_address(input_cep)
            enderecos = []
            enderecos.append(formata_endereco(endereco=endereco))
            endereco = transformation(enderecos=enderecos,index=0)
            load(endereco=endereco,filename=output_csv_filename)

        elif opcao == '2':
            enderecos = extraction(filename=input_csv_filename)
            print("\nLISTA DE CIDADES:")
            for index,end in enumerate(enderecos):
                print(f"{index+1}) {end['cidade']}.") 
            escolha = input("\nDigite a opção desejada: ")
            endereco = transformation(enderecos=enderecos,index=int(escolha)-1)
            load(endereco=endereco,filename=output_csv_filename)
        elif opcao == '3':
            le_csv_saida(filename=output_csv_filename)
        elif opcao == 'x':
            break


if __name__ == "__main__":
    main(enderecos)