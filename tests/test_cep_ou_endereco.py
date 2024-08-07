from correios_plus.buscadores import EnderecoOuCep
from correios_plus.filtros.filtro import Campo


def test_se_pega_o_endereco_pelo_cep():
    enderecos = EnderecoOuCep("21521020").buscar()
    assert enderecos.enderecos[0].logradouro == "Alameda Santa Cruz"


def test_se_pega_enderecos_pelo_nome():
    enderecos = EnderecoOuCep("Alameda Santa Cruz").buscar()
    assert len(enderecos) > 1


def test_se_filtrar_por_uf():
    enderecos = EnderecoOuCep("Alameda Santa Cruz").filtrar(Campo.UF, "RJ")
    assert all(e.uf == "RJ" for e in enderecos.enderecos)


def test_se_buscar_proxima_pagina():
    primeira_pagina = EnderecoOuCep("Alameda Santa Cruz").buscar()
    segunda_pagina = primeira_pagina.proxima()
    terceira_pagina = segunda_pagina.proxima()
    assert primeira_pagina[0] != segunda_pagina[0] != terceira_pagina[0]


def test_se_retorna_erro_se_dados_nao_encontrados():
    assert EnderecoOuCep("kkll").buscar().enderecos == []


def test_se_consigo_filtrar_antes_de_buscar():
    enderecos = EnderecoOuCep("Alameda Santa Cruz").filtrar(Campo.UF, "RJ")
    assert all(e.uf == "RJ" for e in enderecos.enderecos)


def test_se_reproduz_o_objeto_corretamente():
    assert (
        repr(EnderecoOuCep("Alameda Santa Cruz"))
        == "EnderecoOuCep(endereco_ou_cep='Alameda Santa Cruz', tipo='ALL')"
    )


def test_se_pega_o_endereco_pelo_index():
    enderecos = EnderecoOuCep("Alameda Santa Cruz").filtrar(Campo.UF, "RJ")
    assert "Alameda Santa Cruz" in enderecos[0].logradouro


def test_se_transforma_endereco_em_dict():
    enderecos = EnderecoOuCep("Alameda Santa Cruz").filtrar(Campo.UF, "RJ")
    assert isinstance(enderecos[0].dict(), dict)


def test_se_transforma_cep_ou_endereco_em_dict():
    enderecos = EnderecoOuCep("Alameda Santa Cruz").filtrar(Campo.UF, "RJ")
    assert isinstance(enderecos.to_dict(), dict)
