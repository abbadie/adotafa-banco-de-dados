"""Ponto de entrada e menus do sistema AdotaFá."""

from datetime import date

from src.conexao.conexao import ErroConexao
from src.controller.controller_adocao import ControllerAdocao
from src.controller.controller_adotante import ControllerAdotante
from src.controller.controller_animal import ControllerAnimal
from src.controller.excecoes import RegistroReferenciado
from src.model.adocao import Adocao
from src.model.adotante import Adotante
from src.model.animal import Animal
from src.reports.relatorios import Relatorios
from src.utils.config import MENU_ENTIDADES, MENU_PRINCIPAL, MENU_RELATORIOS
from src.utils.entrada import (
    confirmar,
    ler_data,
    ler_decimal,
    ler_inteiro,
    ler_opcao,
    ler_texto,
    pausar,
)
from src.utils.splash_screen import exibir_splash
from src.utils.tabela import montar_tabela


controller_adotante = ControllerAdotante()
controller_animal = ControllerAnimal()
controller_adocao = ControllerAdocao()


def titulo(texto: str) -> None:
    print("\n" + "=" * 68)
    print(texto.center(68))
    print("=" * 68)


def ler_enum(mensagem: str, opcoes: set[str], padrao: str | None = None) -> str:
    while True:
        sufixo = f" [{padrao}]" if padrao else ""
        valor = input(f"{mensagem} ({'/'.join(sorted(opcoes))}){sufixo}: ").strip().upper()
        if not valor and padrao is not None:
            return padrao
        if valor in opcoes:
            return valor
        print("Valor inválido. Escolha uma das opções exibidas.")


def exibir_adotantes(somente_ativos: bool = False) -> bool:
    linhas = controller_adotante.listar_resumo(somente_ativos)
    print(montar_tabela(["Código", "Nome", "CPF", "Cidade", "Situação"], linhas))
    return bool(linhas)


def exibir_animais(somente_disponiveis: bool = False) -> bool:
    linhas = controller_animal.listar_resumo(somente_disponiveis)
    print(montar_tabela(["Código", "Nome", "Espécie", "Porte", "Status"], linhas))
    return bool(linhas)


def exibir_adocoes() -> bool:
    linhas = controller_adocao.listar_resumo()
    print(montar_tabela(["Código", "Animal", "Adotante", "Data", "Taxa (R$)"], linhas))
    return bool(linhas)


def ler_adotante(atual: Adotante | None = None) -> Adotante:
    nome = ler_texto("Nome completo", 3, atual.nome if atual else None)
    cpf = ler_texto("CPF (somente números)", 11, atual.cpf if atual else None)
    telefone = ler_texto("Telefone", 8, atual.telefone if atual else None)
    email = ler_texto("E-mail", 5, atual.email if atual else None)
    cidade = ler_texto("Cidade", 2, atual.cidade if atual else None)
    ativo_padrao = "S" if atual is None or atual.ativo else "N"
    ativo = ler_enum("Cadastro ativo?", {"S", "N"}, ativo_padrao) == "S"
    return Adotante(
        id_adotante=atual.id_adotante if atual else None,
        nome=nome,
        cpf=cpf,
        telefone=telefone,
        email=email,
        cidade=cidade,
        ativo=ativo,
    )


def ler_animal(atual: Animal | None = None) -> Animal:
    nome = ler_texto("Nome do animal", 2, atual.nome if atual else None)
    especie = ler_enum(
        "Espécie",
        Animal.ESPECIES,
        atual.especie if atual else None,
    )
    sexo = ler_enum("Sexo", Animal.SEXOS, atual.sexo if atual else None)
    idade = ler_inteiro(
        "Idade aproximada em anos",
        0,
        35,
        atual.idade_aproximada if atual else None,
    )
    porte = ler_enum("Porte", Animal.PORTES, atual.porte if atual else None)
    entrada = ler_data("Data de entrada", atual.data_entrada if atual else None)
    status = atual.status_adocao if atual else "DISPONIVEL"
    if atual:
        print(f"Status preservado automaticamente: {status}")
    return Animal(
        id_animal=atual.id_animal if atual else None,
        nome=nome,
        especie=especie,
        sexo=sexo,
        idade_aproximada=idade,
        porte=porte,
        status_adocao=status,
        data_entrada=entrada,
    )


def ler_adocao(atual: Adocao | None = None) -> Adocao | None:
    print("\nAdotantes ativos:")
    if not exibir_adotantes(somente_ativos=True):
        print("Cadastre um adotante ativo antes de registrar uma adoção.")
        return None
    id_adotante = ler_inteiro(
        "Código do adotante",
        1,
        padrao=atual.adotante.id_adotante if atual else None,
    )
    adotante = controller_adotante.buscar_por_id(id_adotante)
    if not adotante.ativo:
        raise ValueError("O adotante selecionado está inativo.")

    print("\nAnimais:")
    if atual:
        if not exibir_animais():
            return None
        print("Na atualização, selecione o animal atual ou outro com status DISPONIVEL.")
    elif not exibir_animais(somente_disponiveis=True):
        print("Não há animais disponíveis para adoção.")
        return None
    id_animal = ler_inteiro(
        "Código do animal",
        1,
        padrao=atual.animal.id_animal if atual else None,
    )
    animal = controller_animal.buscar_por_id(id_animal)
    if atual is None and animal.status_adocao != "DISPONIVEL":
        raise ValueError("Selecione um animal com status DISPONIVEL.")

    data_adocao = ler_data("Data da adoção", atual.data_adocao if atual else date.today())
    taxa = ler_decimal("Taxa da adoção", atual.taxa if atual else None)
    observacoes = ler_texto(
        "Observações (pode ficar em branco)",
        0,
        atual.observacoes if atual else "",
    )
    return Adocao(
        id_adocao=atual.id_adocao if atual else None,
        adotante=adotante,
        animal=animal,
        data_adocao=data_adocao,
        taxa=taxa,
        observacoes=observacoes,
    )


def selecionar_entidade() -> str:
    print(MENU_ENTIDADES)
    return ler_opcao("Escolha uma opção: ", {"0", "1", "2", "3"})


def menu_inserir() -> None:
    while True:
        titulo("INSERIR REGISTROS")
        entidade = selecionar_entidade()
        if entidade == "0":
            return
        try:
            if entidade == "1":
                registro = ler_adotante()
                codigo = controller_adotante.inserir(registro)
                print(f"Adotante incluído com sucesso. Código: {codigo}.")
            elif entidade == "2":
                registro = ler_animal()
                codigo = controller_animal.inserir(registro)
                print(f"Animal incluído com sucesso. Código: {codigo}.")
            else:
                registro = ler_adocao()
                if registro is None:
                    pausar()
                    continue
                codigo = controller_adocao.inserir(registro)
                print(f"Adoção incluída com sucesso. Código: {codigo}.")
        except (ValueError, ErroConexao) as erro:
            print(f"Não foi possível inserir: {erro}")
        if not confirmar("Deseja inserir mais algum registro?"):
            return


def remover_adotante() -> bool:
    if not exibir_adotantes():
        return False
    codigo = ler_inteiro("Código do adotante que será removido", 1)
    registro = controller_adotante.buscar_por_id(codigo)
    print("Selecionado:", registro.to_string())
    if not confirmar("Confirma a remoção desse adotante?"):
        print("Remoção cancelada.")
        return False
    dependencias = controller_adotante.quantidade_adocoes(codigo)
    remover_dependencias = False
    if dependencias:
        print(f"O adotante é referenciado por {dependencias} adoção(ões).")
        remover_dependencias = confirmar(
            "Deseja remover também as adoções e liberar os respectivos animais?"
        )
        if not remover_dependencias:
            print("O adotante foi preservado para manter a integridade referencial.")
            return False
    controller_adotante.excluir(codigo, remover_dependencias)
    print("Adotante removido com sucesso.")
    return True


def remover_animal() -> bool:
    if not exibir_animais():
        return False
    codigo = ler_inteiro("Código do animal que será removido", 1)
    registro = controller_animal.buscar_por_id(codigo)
    print("Selecionado:", registro.to_string())
    if not confirmar("Confirma a remoção desse animal?"):
        print("Remoção cancelada.")
        return False
    dependencias = controller_animal.quantidade_adocoes(codigo)
    remover_dependencia = False
    if dependencias:
        print("O animal é referenciado por uma adoção.")
        remover_dependencia = confirmar("Deseja remover também a adoção vinculada?")
        if not remover_dependencia:
            print("O animal foi preservado para manter a integridade referencial.")
            return False
    controller_animal.excluir(codigo, remover_dependencia)
    print("Animal removido com sucesso.")
    return True


def remover_adocao() -> bool:
    if not exibir_adocoes():
        return False
    codigo = ler_inteiro("Código da adoção que será removida", 1)
    registro = controller_adocao.buscar_por_id(codigo)
    print("Selecionada:", registro.to_string())
    if not confirmar("Confirma a remoção dessa adoção?"):
        print("Remoção cancelada.")
        return False
    controller_adocao.excluir(codigo)
    print("Adoção removida e animal liberado com sucesso.")
    return True


def menu_remover() -> None:
    while True:
        titulo("REMOVER REGISTROS")
        entidade = selecionar_entidade()
        if entidade == "0":
            return
        try:
            if entidade == "1":
                remover_adotante()
            elif entidade == "2":
                remover_animal()
            else:
                remover_adocao()
        except RegistroReferenciado as erro:
            print(f"Integridade referencial: {erro}")
        except (ValueError, ErroConexao) as erro:
            print(f"Não foi possível remover: {erro}")
        if not confirmar("Deseja remover mais algum registro?"):
            return


def atualizar_adotante() -> bool:
    if not exibir_adotantes():
        return False
    codigo = ler_inteiro("Código do adotante que será atualizado", 1)
    atual = controller_adotante.buscar_por_id(codigo)
    print("Atual:", atual.to_string())
    print("Pressione ENTER para preservar o valor apresentado entre colchetes.")
    atualizado = ler_adotante(atual)
    controller_adotante.atualizar(atualizado)
    print("Registro atualizado:", controller_adotante.buscar_por_id(codigo).to_string())
    return True


def atualizar_animal() -> bool:
    if not exibir_animais():
        return False
    codigo = ler_inteiro("Código do animal que será atualizado", 1)
    atual = controller_animal.buscar_por_id(codigo)
    print("Atual:", atual.to_string())
    print("Pressione ENTER para preservar o valor apresentado entre colchetes.")
    atualizado = ler_animal(atual)
    controller_animal.atualizar(atualizado)
    print("Registro atualizado:", controller_animal.buscar_por_id(codigo).to_string())
    return True


def atualizar_adocao() -> bool:
    if not exibir_adocoes():
        return False
    codigo = ler_inteiro("Código da adoção que será atualizada", 1)
    atual = controller_adocao.buscar_por_id(codigo)
    print("Atual:", atual.to_string())
    print("Pressione ENTER para preservar o valor apresentado entre colchetes.")
    atualizada = ler_adocao(atual)
    if atualizada is None:
        return False
    controller_adocao.atualizar(atualizada)
    print("Registro atualizado:", controller_adocao.buscar_por_id(codigo).to_string())
    return True


def menu_atualizar() -> None:
    while True:
        titulo("ATUALIZAR REGISTROS")
        entidade = selecionar_entidade()
        if entidade == "0":
            return
        try:
            if entidade == "1":
                atualizar_adotante()
            elif entidade == "2":
                atualizar_animal()
            else:
                atualizar_adocao()
        except (ValueError, ErroConexao) as erro:
            print(f"Não foi possível atualizar: {erro}")
        if not confirmar("Deseja atualizar mais algum registro?"):
            return


def menu_relatorios() -> None:
    relatorios = Relatorios()
    while True:
        print(MENU_RELATORIOS)
        opcao = ler_opcao("Escolha uma opção: ", {"0", "1", "2"})
        if opcao == "0":
            return
        try:
            if opcao == "1":
                titulo("RESUMO DE ADOÇÕES POR ESPÉCIE")
                cabecalhos, linhas = relatorios.adocoes_por_especie()
            else:
                titulo("ADOÇÕES DETALHADAS")
                cabecalhos, linhas = relatorios.adocoes_detalhadas()
            print(montar_tabela(cabecalhos, linhas))
        except ErroConexao as erro:
            print(f"Não foi possível gerar o relatório: {erro}")
        pausar()


def executar() -> None:
    try:
        exibir_splash()
    except ErroConexao as erro:
        print(f"\nERRO DE INICIALIZAÇÃO: {erro}")
        print("Consulte a seção de instalação e configuração do README.md.")
        return

    while True:
        print(MENU_PRINCIPAL)
        opcao = ler_opcao("Escolha uma opção: ", {"0", "1", "2", "3", "4"})
        if opcao == "0":
            print("\nObrigado por utilizar o AdotaFá. Até a próxima!")
            return
        if opcao == "1":
            menu_relatorios()
        elif opcao == "2":
            menu_inserir()
        elif opcao == "3":
            menu_remover()
        else:
            menu_atualizar()


if __name__ == "__main__":
    try:
        executar()
    except (KeyboardInterrupt, EOFError):
        print("\nExecução encerrada pelo usuário.")

