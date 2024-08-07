# AINDA EM DESENVOLVIMENTO...

# Correios Plus

Este repositório contém classes e métodos para buscar CEPs e localidades através do site dos Correios. Todos os dados são extraídos do [site dos Correios](https://www2.correios.com.br/sistemas/buscacep/).

## Instalação

```bash
pip install correios-plus
```

## Uso

## Busca por CEP

```python
from correios_plus import EnderecoCEP

cep_info = EnderecoCEP("21521020").buscar()
print(cep_info[0].localidade) # Rio de Janeiro
print(cep_info[0].uf) # RJ
```


## Buscando um endereço pelo nome da Rua:

```python
from correios_plus import EnderecoOuCep, Campo

enderecos = EnderecoOuCep("Alameda Santa Cruz").filtrar(Campo.UF, "RJ")
print(enderecos[0].cep)  # '21521020'
```
O método filtrar pode ser utilizado para refinar os resultados com base em diferentes campos, como UF, bairro, logradouro, localidade e CEP. Sempre retorna uma lista de endereços.

## API

### class *EnderecoCEP*:
- Parâmetros:
    - `cep`: str - CEP a ser pesquisado.
    - `enderecos`: list[EnderecoCEP] - Lista de endereços encontrados.

- URL de Referência: [Busca Endereço](https://www2.correios.com.br/sistemas/buscacep/buscaEndereco.cfm)

#### Métodos:
- `buscar()` (EnderecoCEP): Realiza a busca pelo CEP especificado.
    - Retorna a instância do objeto EnderecoCEP. Use o `enderecos` para obter a lista de endereços encontrados.
- `to_dict` (dict): Retorna um dicionário com os endereços.



### class *CEPLocalidade*:

- Parâmetros:
    - `uf` (str) Unidade Federativa a ser pesquisada.
    - `localidade` (str): Nome da localidade a ser pesquisada.
    - `logradouro` (str): Nome do logradouro a ser pesquisado.
    - `tipo` (str): Tipo de localidade a ser pesquisada. (OBS: `RUA`, `ALAMEDA`, `VILA` e `BAIRRO`)
    - `numero`: str - Número do localidade a ser pesquisado.
    - `enderecos`: list[EnderecoCEP] - Lista de endereços encontrados.

- Retorno:
    - `CEPLocalidade`: Objeto CEPLocalidade.
    return: list[CEPLocalidade] - Lista de endereços encontrados.

- URL de Referência: [Busca CEP](https://www2.correios.com.br/sistemas/buscacep/buscaCep.cfm)

#### Métodos:
- `buscar()` (CEPLocalidade): Realiza a busca pelo CEP ou logradouro.
- `filtrar()` (CEPLocalidade): Filtra os resultados obtidos com base em critérios específicos.
  - Parametros:
    - `campo`: str - Campo a ser filtrado. (Ex: `UF`, `BAIRRO`, `LOGRADOURO`, `LOCALIDADE` ou `CEP`)
    - `valor`: str - Valor a ser filtrado. (Ex: `RJ`, `CENTRO`, `SANTA CRUZ`, `RIO DE JANEIRO` ou `21521020`)
- `proxima()` (CEPLocalidade): Obtém os dados da próxima página de resultados.
- `to_dict` (dict): Retorna um dicionário com os endereços.



    