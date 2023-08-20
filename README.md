# Desafio DIO - Santander Bootcamp 2023 - Explorando IA Generativa em um Pipeline de ETL com Python

Código para certificação DIO Santander Bootcamp 2023 - Ciência de Dados com Python. Módulo: Explorando IA Generativa em um Pipeline de ETL com Python

## Desafio
Desenvolver uma aplicação em Python utilizando o método de Pipeline ETL, definido por sua estrutura por etapas. São eleas: Extraction(Extração), Transformation (Transformação) e Load (Carregamento).

Basicamente, os dados são extraídos de várias fontes, como arquivos, API's, banco de dados, etc; em seguida são transformados em novas informações que serão salvos em algum arquivo, banco de dados ou qualquer outra estrutura de armazenamento.

## Ferramentas
* [Python](https://www.python.org)
* API [ChatGPT (OpenAI)](https://platform.openai.com/docs/api-reference)
* API [Via CEP](https://viacep.com.br)
* [GitHub](https://github.com)

## Objetivo da Aplicação

A aplicação visa gerar slogans para cidades a partir de um CEP usando o [ChatGPT (OpenAI)](https://platform.openai.com/docs/api-reference) para gerar os slogans e depois salvar em um arquivo CSV.

## Funcionamento da Aplicação

O usuário precisa selecionar a opção de inserção de CEP tendo como opção ler de um arquivo CSV `enderecos.csv` ou digitar o CEP desejado. 

O arquivo `enderecos.csv` tem como estrutura dois campos: *CEP* e *numero*. Neste arquivo estão salvos os CEP's e números dos endereços das prefeituras das capitais dos estados do Brasil. 

O CEP digitado pode ser qualquer CEP existente, mas não é possível registrar números, pois o mesmo só é possível para o método via arquivo CSV. Esta regra foi estabelecida para que o arquivo CSV simule uma base de dados governamental que possui todos os endereços de prefeituras.

Após selecionar/inserir o CEP, a aplicação enviará o CEP e número, o segundo se houver, via request á API [Via CEP](https://viacep.com.br) e retornará o endereço completo no formato `JSON` da seguinte maneira:

Exemplo de retorno da API:

    {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "complemento": "lado ímpar",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
        "ibge": "3550308",
        "gia": "1004",
        "ddd": "11",
        "siafi": "7107"
    }

Após esta extração de dados, a aplicação ira filtrá-los para atender aos objetivos da etapa de transformação, utilizando as informações: `"logradouro"`,`"bairro"`, `"localidade"` e `"uf"`. O campo slogan é adicionado ao contexto de endereço como demostrado abaixo.

Exemplo de objeto endereco: 

    {
        "logradouro": "Praça da Sé",
        "numero" : "23",
        "bairro" : "Sé",
        "cidade" : "São Paulo",
        "estado" : "SP",
        "slogan" : []
    }

Na etapa de transformação, os dados de endereço são enviados para o chatGPT para gerar o slogan. A API tem regras próprias para geração de requisições que podem ser consultadas na [Documentação da API ChatGPT (OpenAI)](https://platform.openai.com/docs/api-reference). O que é relevante salientar é a configuração referente ao comando à Inteligencia Artificial. Para tal, é necessário informar ao chatGPT a sua função, para esta aplicação, ele deve agir como um promotor de turismo de cidades. Também é necessário informá-lo o que ele deve fazer, criar um slogan para a cidade.

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

A API retornará um response com várias informações, dentre elas a mensagem na opção `choices[]`.

    "message": {
        "role": "assistant",
        "content": "Oásis moderno e acolhedor no coração do Brasil, onde natureza exuberante encontra uma cidade vibrante."
    }

Então, na Etapa de Carregamento, a informação é salva no arquivo `slogans.csv`. Nesta etapa a informação pode ser salva de maneiras diferentes de acordo como foi selecionado o modo de inserção do CEP, como foi explicado anteriormente, podendo ter o endereço da prefeitura caso o CEP tenha sido selecionado do arquivo `enderecos.csv`.

Exemplo dos formatos possíveis:

    CEP Digitado: 
        ----------------------------------------
        Cidade: Sorocaba/SP
        Slogan: Sinta o encanto do interior: diversão, cultura e natureza, tudo em um só lugar!
        ----------------------------------------
    
    CEP Selecionado:

        ----------------------------------------
        Cidade: Palmas/TO
        Slogan: Oásis moderno e acolhedor no coração do Brasil, onde natureza exuberante encontra uma cidade vibrante.
        Endereço da Prefeitura: Praça Girassóis, 28 - Bairro Plano Diretor Norte
        ----------------------------------------

A ferramenta possibilita a leitura do arquivo `slogans.csv` e finaliza assim que o usuário decide finalizá-la no menu.
