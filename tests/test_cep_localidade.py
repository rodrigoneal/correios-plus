from correios_plus.buscadores import CEPLocalidade
from correios_plus.filtros.filtro import UF, Campo, Localidade


def test_se_pega_o_endereco_pela_logradoura():
    enderecos = CEPLocalidade(
        UF.RJ, "Rio de Janeiro", tipo=Localidade.ALAMEDA, logradouro="Santa Cruz"
    ).buscar()
    assert "Santa Cruz" in enderecos[0].logradouro


def test_se_filtra_pelo_bairro():
    enderecos = (
        CEPLocalidade(
            UF.RJ, "Rio de Janeiro", tipo=Localidade.AVENIDA, logradouro="Brasil"
        )
        .filtrar(Campo.BAIRRO, "Deodoro")
        .enderecos
    )
    assert len(enderecos) > 1
    assert all(e.bairro == "Deodoro" for e in enderecos)


def test_se_faz_paginacao():
    primeira_pagina = CEPLocalidade(
        UF.RJ, "Rio de Janeiro", tipo=Localidade.RUA, logradouro="Brasil", numero="42"
    ).buscar()
    segunda_pagina = primeira_pagina.proxima()
    assert primeira_pagina[0] != segunda_pagina[0]


def test_se_faz_representacao():
    assert (
        str(
            CEPLocalidade(
                UF.RJ,
                "Rio de Janeiro",
                tipo=Localidade.RUA,
                logradouro="Brasil",
                numero="42",
            )
        )
        == "CEPLocalidade(uf='RJ', localidade='Rio de Janeiro', tipo='Rua', logradouro='Brasil', numero='42')"
    )
