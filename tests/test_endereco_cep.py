from correios_plus.buscadores import EnderecoCEP


def test_se_pega_o_endereco_pelo_cep():
    enderecos = EnderecoCEP("21521020").buscar()
    assert enderecos[0].logradouro == "Alameda Santa Cruz"

def test_se_passar_um_cep_invalido_retorna_vazio():
    enderecos = EnderecoCEP("12345678").buscar()
    assert len(enderecos) == 0