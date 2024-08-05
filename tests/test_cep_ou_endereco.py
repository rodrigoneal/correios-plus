from correios_plus.buscadores.endereco_ou_cep import EnderecoOuCep
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
    segunda_pagina = primeira_pagina.proximar_pagina()
    terceira_pagina = segunda_pagina.proximar_pagina()
    assert (
        primeira_pagina.enderecos[0]
        != segunda_pagina.enderecos[0]
        != terceira_pagina.enderecos[0]
    )


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
