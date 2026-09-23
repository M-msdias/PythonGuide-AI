"""
Base de conhecimento do PythonGuide AI.

Domínio:
    Python e sua documentação oficial.

A base é composta por:
    1. Conteúdo introdutório local;
    2. Páginas da documentação oficial do Python;
    3. Quebra dos documentos em chunks.

Fluxo:
    fontes -> documentos -> chunks
"""

import json
from pathlib import Path
CACHE_FILE = Path("data/python_docs_cache.json")

from typing import List, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import json
from pathlib import Path

CACHE_FILE = Path("data/python_docs_cache.json")


# CONFIGURAÇÃO

BASE_URL = "https" + "://" + "docs.python.org/pt-br/3/"

# Páginas da documentação oficial do Python.
#
# A ideia é utilizar várias páginas do mesmo domínio,
# aumentando significativamente o tamanho da base.
#
# Se alguma página não existir em uma determinada versão,
# ela será simplesmente ignorada pelo scraper.

DOCUMENTATION_PAGES = [
    "tutorial/index.html",
    "tutorial/appetite.html",
    "tutorial/interpreter.html",
    "tutorial/introduction.html",
    "tutorial/controlflow.html",
    "tutorial/datastructures.html",
    "tutorial/modules.html",
    "tutorial/inputoutput.html",
    "tutorial/errors.html",
    "tutorial/classes.html",
    "tutorial/stdlib.html",
    "tutorial/stdlib2.html",
    "tutorial/venv.html",
    "tutorial/whatnow.html",
    "tutorial/interactive.html",
    "tutorial/floatingpoint.html",
    "tutorial/appendix.html",

    "library/index.html",
    "library/functions.html",
    "library/stdtypes.html",
    "library/exceptions.html",
    "library/os.html",
    "library/pathlib.html",
    "library/json.html",
    "library/re.html",
    "library/datetime.html",
    "library/math.html",
    "library/random.html",
    "library/statistics.html",
    "library/collections.html",
    "library/itertools.html",
    "library/functools.html",
    "library/typing.html",
    "library/dataclasses.html",
    "library/asyncio.html",
    "library/logging.html",
    "library/sqlite3.html",
    "library/csv.html",
    "library/secrets.html",
    "library/subprocess.html",
    "library/threading.html",
    "library/multiprocessing.html",
    "library/unittest.html",
    "library/venv.html",

    "reference/index.html",
    "reference/compound_stmts.html",
    "reference/simple_stmts.html",
    "reference/expressions.html",
    "reference/datamodel.html",
    "reference/import.html",
    "reference/executionmodel.html",
    "reference/lexical_analysis.html",
]


# CONTEÚDO MANUAL

TEXTOS_CONHECIMENTO_MANUAL = [
    """
    Python é uma linguagem de programação de alto nível, interpretada,
    de propósito geral e conhecida por sua sintaxe relativamente simples.
    Pode ser utilizada para desenvolvimento web, automação, análise de dados,
    inteligência artificial, scripts, aplicações desktop e diversas outras áreas.
    """,

    """
    Variáveis em Python são utilizadas para armazenar referências a valores.
    A linguagem possui tipagem dinâmica, portanto o tipo associado a uma variável
    pode mudar durante a execução do programa. Exemplos de tipos comuns incluem
    int, float, str, bool, list, tuple, set e dict.
    """,

    """
    Listas em Python são coleções ordenadas e mutáveis. Elas podem armazenar
    elementos de diferentes tipos. É possível adicionar elementos com append(),
    remover elementos com remove() ou pop(), acessar posições por índice e
    percorrer os elementos utilizando estruturas de repetição.
    """,

    """
    Tuplas são coleções ordenadas que, ao contrário das listas, são imutáveis.
    São úteis quando um conjunto de valores não deve ser alterado depois de
    criado. Uma tupla pode conter elementos de tipos diferentes.
    """,

    """
    Dicionários representam estruturas de dados baseadas em pares chave-valor.
    Uma chave permite acessar o valor associado. Dicionários são muito utilizados
    para representar registros, configurações e dados estruturados.
    """,

    """
    Conjuntos, representados pelo tipo set, armazenam elementos únicos e não
    possuem a mesma semântica de ordenação das listas. São úteis para operações
    como união, interseção, diferença e eliminação de duplicidades.
    """,

    """
    A estrutura if permite executar código condicionalmente. Python também
    possui elif e else para representar condições alternativas. A indentação
    é parte da sintaxe da linguagem e define os blocos de código.
    """,

    """
    Os laços for e while são utilizados para repetição. O for é especialmente
    comum para percorrer elementos de uma coleção ou um intervalo. O while
    continua executando enquanto uma condição permanecer verdadeira.
    """,

    """
    Funções são definidas em Python utilizando a palavra-chave def.
    Elas podem receber parâmetros e retornar valores utilizando return.
    Funções ajudam a organizar o programa em unidades reutilizáveis.
    """,

    """
    Uma função pode possuir argumentos posicionais, argumentos nomeados,
    valores padrão, parâmetros somente posicionais e parâmetros somente nomeados.
    Python também permite receber um número variável de argumentos utilizando
    *args e **kwargs.
    """,

    """
    Classes permitem implementar programação orientada a objetos em Python.
    Uma classe pode possuir atributos e métodos. Objetos são instâncias de classes.
    O método __init__ normalmente é utilizado para inicializar atributos de uma
    nova instância.
    """,

    """
    Herança permite criar uma classe baseada em outra classe. A classe derivada
    pode reutilizar atributos e métodos da classe base e também pode sobrescrever
    comportamentos quando necessário.
    """,

    """
    Exceções representam situações anormais durante a execução de um programa.
    Python utiliza try, except, else e finally para tratamento de exceções.
    Também é possível criar exceções personalizadas herdando de Exception.
    """,

    """
    Módulos permitem organizar código Python em arquivos separados.
    O comando import permite utilizar funcionalidades de outro módulo.
    Pacotes agrupam módulos relacionados em uma estrutura de diretórios.
    """,

    """
    Ambientes virtuais permitem criar ambientes isolados para projetos Python.
    Isso evita conflitos entre versões de dependências utilizadas por diferentes
    projetos. O módulo venv é uma das formas padrão de criar ambientes virtuais.
    """,

    """
    O pip é uma ferramenta utilizada para instalar e gerenciar pacotes Python.
    Em projetos, as dependências podem ser registradas em um arquivo
    requirements.txt e instaladas posteriormente com pip install.
    """,

    """
    O módulo pathlib fornece uma abordagem orientada a objetos para trabalhar
    com caminhos de arquivos e diretórios. A classe Path pode ser utilizada
    para criar caminhos, verificar existência, ler arquivos e navegar por diretórios.
    """,

    """
    O módulo json permite converter dados entre objetos Python e o formato JSON.
    json.dumps() transforma um objeto Python em uma string JSON e json.loads()
    realiza a operação inversa. Também existem dump() e load() para trabalhar
    diretamente com arquivos.
    """,

    """
    O módulo re implementa expressões regulares em Python. Ele pode ser utilizado
    para localizar padrões em textos, validar formatos e realizar substituições.
    Funções importantes incluem search(), match(), findall() e sub().
    """,

    """
    O módulo datetime fornece classes para trabalhar com datas e horários.
    Entre seus principais objetos estão date, time, datetime e timedelta.
    """,

    """
    O módulo logging fornece uma infraestrutura para registrar eventos de uma
    aplicação. Logs podem ser classificados em níveis como DEBUG, INFO, WARNING,
    ERROR e CRITICAL.
    """,

    """
    O módulo asyncio fornece recursos para programação assíncrona em Python.
    Ele é utilizado especialmente em aplicações que realizam muitas operações
    de entrada e saída e podem se beneficiar de concorrência cooperativa.
    """,

    """
    O módulo sqlite3 fornece uma interface para utilização do SQLite através
    da API DB-API 2.0. SQLite é um banco de dados embutido que não exige um
    servidor separado para funcionar.
    """,

    """
    O módulo unittest oferece ferramentas para criação de testes automatizados.
    Testes podem ser agrupados em classes que herdam de unittest.TestCase.
    Métodos de teste normalmente começam com test_.
    """,

    """
    O módulo threading permite trabalhar com threads. Threads podem ser úteis
    em aplicações que realizam operações de entrada e saída e precisam lidar
    com múltiplas tarefas concorrentes.
    """,

    """
    O módulo subprocess permite iniciar e controlar processos externos.
    Ele pode ser utilizado para executar programas do sistema e capturar
    suas entradas e saídas.
    """,

    """
    O módulo secrets fornece funções para geração de valores aleatórios
    adequados para aplicações relacionadas a segurança, como tokens,
    senhas temporárias e identificadores secretos.
    """,
]


# SCRAPER


class PythonDocumentationScraper:
    """
    Coleta conteúdo textual da documentação oficial do Python.
    """

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "PythonGuideAI/1.0 "
                    "(educational RAG project)"
                )
            }
        )

    def build_url(self, page: str) -> str:
        return urljoin(BASE_URL, page)

    def scrape_page(self, page: str) -> str:
        """
        Faz o download de uma página da documentação e extrai
        o conteúdo textual principal.
        """

        url = self.build_url(page)

        try:
            response = self.session.get(
                url,
                timeout=15,
            )

            if response.status_code != 200:
                print(
                    f"[AVISO] Página ignorada: "
                    f"{page} - HTTP {response.status_code}"
                )
                return ""

            soup = BeautifulSoup(
                response.content,
                "html.parser",
            )

            # Remove elementos que normalmente não fazem parte
            # do conteúdo principal.
            for element in soup(
                [
                    "script",
                    "style",
                    "nav",
                    "footer",
                    "header",
                    "aside",
                ]
            ):
                element.decompose()

            main_content = (
                soup.find("main")
                or soup.find(
                    "div",
                    {"role": "main"},
                )
                or soup.find(
                    "div",
                    class_="body",
                )
                or soup.body
            )

            if not main_content:
                return ""

            text = main_content.get_text(
                separator=" ",
                strip=True,
            )

            # Evita inserir documentos praticamente vazios.
            if len(text) < 300:
                return ""

            # Limita cada página para evitar que uma única página
            # domine a base.
            text = text[:20000]

            return (
                f"Fonte: Documentação oficial do Python\n"
                f"Página: {page}\n\n"
                f"{text}"
            )

        except requests.RequestException as error:
            print(
                f"[AVISO] Erro ao acessar {page}: {error}"
            )
            return ""

        except Exception as error:
            print(
                f"[AVISO] Erro inesperado em {page}: {error}"
            )
            return ""

    def scrape_all(self) -> List[str]:
        """
        Executa o scraping das páginas cadastradas.
        """

        print("=" * 60)
        print("INICIANDO COLETA DA DOCUMENTAÇÃO DO PYTHON")
        print("=" * 60)

        texts = []

        for index, page in enumerate(
            DOCUMENTATION_PAGES,
            start=1,
        ):
            print(
                f"[{index}/{len(DOCUMENTATION_PAGES)}] "
                f"Coletando {page}"
            )

            text = self.scrape_page(page)

            if text:
                texts.append(text)

        print("=" * 60)
        print(
            f"COLETA FINALIZADA: "
            f"{len(texts)} páginas obtidas"
        )
        print("=" * 60)

        return texts


# CONSTRUÇÃO DA BASE
def salvar_cache(documentos: List[Document]) -> None:
    """
    Salva os documentos da base de conhecimento em JSON.
    """

    CACHE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dados = []

    for documento in documentos:
        dados.append(
            {
                "page_content": documento.page_content,
                "metadata": documento.metadata,
            }
        )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"\n[CACHE] Base salva em: {CACHE_FILE}"
    )


def carregar_cache() -> List[Document]:
    """
    Carrega os documentos previamente salvos.
    """

    if not CACHE_FILE.exists():
        return []

    print(
        f"\n[CACHE] Carregando base de: {CACHE_FILE}"
    )

    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8",
    ) as arquivo:
        dados = json.load(arquivo)

    documentos = []

    for item in dados:
        documentos.append(
            Document(
                page_content=item["page_content"],
                metadata=item.get("metadata", {}),
            )
        )

    print(
        f"[CACHE] {len(documentos)} documentos carregados."
    )

    return documentos

def criar_base_conhecimento() -> Tuple[
    List[Document],
    List[Document],
]:
    """
    Cria os documentos e chunks utilizados pelo RAG.

    Se existir um cache local, ele será utilizado para evitar
    uma nova coleta da documentação.
    """

    print("\nCriando base de conhecimento...")

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    documentos_cache = carregar_cache()

    if documentos_cache:
        documentos = documentos_cache

        print(
            "[CACHE] Utilizando a base de conhecimento salva."
        )

    else:
        # ----------------------------------------------------
        # CONTEÚDO MANUAL
        # ----------------------------------------------------

        all_texts = list(
            TEXTOS_CONHECIMENTO_MANUAL
        )

        # ----------------------------------------------------
        # WEB SCRAPING
        # ----------------------------------------------------

        try:
            scraper = PythonDocumentationScraper()

            scraped_texts = scraper.scrape_all()

            all_texts.extend(
                scraped_texts
            )

        except Exception as error:
            print(
                "[AVISO] O web scraping falhou."
            )
            print(
                f"Motivo: {error}"
            )
            print(
                "O sistema continuará utilizando "
                "o conteúdo manual."
            )

        # ----------------------------------------------------
        # DOCUMENTOS
        # ----------------------------------------------------

        documentos = []

        for index, texto in enumerate(all_texts):
            documento = Document(
                page_content=texto,
                metadata={
                    "fonte": "python_documentation",
                    "document_id": index,
                },
            )

            documentos.append(
                documento
            )

        # ----------------------------------------------------
        # SALVAR CACHE
        # ----------------------------------------------------

        salvar_cache(documentos)

    # --------------------------------------------------------
    # CHUNKING
    # --------------------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = text_splitter.split_documents(
        documentos
    )

    print("\nBASE DE CONHECIMENTO")
    print("-" * 40)
    print(
        f"Documentos: {len(documentos)}"
    )
    print(
        f"Chunks: {len(chunks)}"
    )
    print(
        "Origem: documentação oficial + "
        "conteúdo introdutório"
    )
    print("-" * 40)

    return documentos, chunks


def get_textos_base():
    """
    Retorna os textos manuais da base.
    """
    return TEXTOS_CONHECIMENTO_MANUAL