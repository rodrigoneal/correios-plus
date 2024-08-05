from typing import Literal


class Campo:
    UF: Literal["uf"] = "uf"
    BAIRRO: Literal["bairro"] = "bairro"
    LOGRADOURO: Literal["logradouro"] = "logradouro"
    LOCALIDADE: Literal["localidade"] = "localidade"
    CEP: Literal["cep"] = "cep"


class Tipo:
    TUDO: Literal["ALL"] = "ALL"
    LOCALIDADE: Literal["LOG"] = "LOG"
    LOGRADOURO: Literal["LOG"] = "LOG"
    CEP_PROMOCIONAL: Literal["PRO"] = "PRO"
    CAIXA_POSTAL_COMUNITARIA: Literal["CPC"] = "CPC"
    GRANDE_USUARIO: Literal["GRU"] = "GRU"
    UNIDADE_OPERACIONAL: Literal["UOP"] = "UOP"


class UF:
    AC: Literal["AC"] = "AC"
    AL: Literal["AL"] = "AL"
    AP: Literal["AP"] = "AP"
    AM: Literal["AM"] = "AM"
    BA: Literal["BA"] = "BA"
    CE: Literal["CE"] = "CE"
    DF: Literal["DF"] = "DF"
    ES: Literal["ES"] = "ES"
    GO: Literal["GO"] = "GO"
    MA: Literal["MA"] = "MA"
    MT: Literal["MT"] = "MT"
    MS: Literal["MS"] = "MS"
    MG: Literal["MG"] = "MG"
    PA: Literal["PA"] = "PA"
    PB: Literal["PB"] = "PB"
    PR: Literal["PR"] = "PR"
    PE: Literal["PE"] = "PE"
    PI: Literal["PI"] = "PI"
    RJ: Literal["RJ"] = "RJ"
    RN: Literal["RN"] = "RN"
    RS: Literal["RS"] = "RS"
    RO: Literal["RO"] = "RO"
    RR: Literal["RR"] = "RR"
    SC: Literal["SC"] = "SC"
    SP: Literal["SP"] = "SP"
    SE: Literal["SE"] = "SE"
    TO: Literal["TO"] = "TO"


class Localidade:
    DEFAULT: Literal[""] = ""
    AEROPORTO: Literal["Aeroporto"] = "Aeroporto"
    ALAMEDA: Literal["Alameda"] = "Alameda"
    ÁREA: Literal["Área"] = "Área"
    AVENIDA: Literal["Avenida"] = "Avenida"
    CAMPO: Literal["Campo"] = "Campo"
    CHÁCARA: Literal["Chácara"] = "Chácara"
    COLÔNIA: Literal["Colônia"] = "Colônia"
    CONDOMÍNIO: Literal["Condomínio"] = "Condomínio"
    CONJUNTO: Literal["Conjunto"] = "Conjunto"
    DISTRITO: Literal["Distrito"] = "Distrito"
    ESPLANADA: Literal["Esplanada"] = "Esplanada"
    ESTAÇÃO: Literal["Estação"] = "Estação"
    ESTRADA: Literal["Estrada"] = "Estrada"
    FAVELA: Literal["Favela"] = "Favela"
    FAZENDA: Literal["Fazenda"] = "Fazenda"
    FEIRA: Literal["Feira"] = "Feira"
    JARDIM: Literal["Jardim"] = "Jardim"
    LADEIRA: Literal["Ladeira"] = "Ladeira"
    LAGO: Literal["Lago"] = "Lago"
    LAGOA: Literal["Lagoa"] = "Lagoa"
    LARGO: Literal["Largo"] = "Largo"
    LOTEAMENTO: Literal["Loteamento"] = "Loteamento"
    MORRO: Literal["Morro"] = "Morro"
    NÚCLEO: Literal["Núcleo"] = "Núcleo"
    PARQUE: Literal["Parque"] = "Parque"
    PASSARELA: Literal["Passarela"] = "Passarela"
    PÁTIO: Literal["Pátio"] = "Pátio"
    PRAÇA: Literal["Praça"] = "Praça"
    QUADRA: Literal["Quadra"] = "Quadra"
    RECANTO: Literal["Recanto"] = "Recanto"
    RESIDENCIAL: Literal["Residencial"] = "Residencial"
    RODOVIA: Literal["Rodovia"] = "Rodovia"
    RUA: Literal["Rua"] = "Rua"
    SETOR: Literal["Setor"] = "Setor"
    SÍTIO: Literal["Sítio"] = "Sítio"
    TRAVESSA: Literal["Travessa"] = "Travessa"
    TRECHO: Literal["Trecho"] = "Trecho"
    TREVO: Literal["Trevo"] = "Trevo"
    VALE: Literal["Vale"] = "Vale"
    VEREDA: Literal["Vereda"] = "Vereda"
    VIA: Literal["Via"] = "Via"
    VIADUTO: Literal["Viaduto"] = "Viaduto"
    VIELA: Literal["Viela"] = "Viela"
    VILA: Literal["Vila"] = "Vila"


TipoType = Literal["ALL", "LOG", "PRO", "CPC", "GRU", "UOP"]
CampoType = Literal["uf", "bairro", "logradouro", "localidade", "cep"]
UFType = Literal[
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]
LocalidadeType = Literal[
    "",
    "Aeroporto",
    "Alameda",
    "Área",
    "Avenida",
    "Campo",
    "Chácara",
    "Colônia",
    "Condomínio",
    "Conjunto",
    "Distrito",
    "Esplanada",
    "Estação",
    "Estrada",
    "Favela",
    "Fazenda",
    "Feira",
    "Jardim",
    "Ladeira",
    "Lago",
    "Lagoa",
    "Largo",
    "Loteamento",
    "Morro",
    "Núcleo",
    "Parque",
    "Passarela",
    "Pátio",
    "Praça",
    "Quadra",
    "Recanto",
    "Residencial",
    "Rodovia",
    "Rua",
    "Setor",
    "Sítio",
    "Travessa",
    "Trecho",
    "Trevo",
    "Vale",
    "Vereda",
    "Via",
    "Viaduto",
    "Viela",
    "Vila",
]
