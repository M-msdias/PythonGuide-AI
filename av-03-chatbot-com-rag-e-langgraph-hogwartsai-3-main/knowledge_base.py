"""
Base de conhecimento do chatbot - Harry Potter
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any

TEXTOS_CONHECIMENTO_MANUAL = [
    """
    Harry James Potter é o protagonista da série. Nasceu em 31 de julho de 1980, filho de Tiago e Lílian Potter.
    É conhecido como "O Menino Que Sobreviveu" por ter sobrevivido ao ataque de Lord Voldemort quando bebê.
    Possui uma cicatriz em forma de raio na testa. Estuda na Casa Grifinória em Hogwarts.
    Sua varinha é de azevinho com núcleo de pena de fênix (a mesma de Voldemort). Seu patrono é um cervo.
    """,
    """
    Hermione Jean Granger é uma bruxa nascida trouxa, considerada a mais inteligente de sua geração.
    Nasceu em 19 de setembro de 1979. É da Casa Grifinória, amiga de Harry e Rony.
    Possui um gato chamado Bichento. Seu patrono é uma lontra. Tornou-se Ministra da Magia anos depois.
    Sua varinha é de videira com núcleo de corda de coração de dragão.
    """,
    """
    Ronald Bilius Weasley, conhecido como Rony, é o melhor amigo de Harry. Nasceu em 1 de março de 1980.
    É da Casa Grifinória, sexto filho da família Weasley. Tem medo de aranhas. Possui um rato chamado Perebas.
    Mais tarde casou-se com Hermione. Seu patrono é um Jack Russell Terrier.
    """,
    """
    Lord Voldemort, nascido Tom Marvolo Riddle, é o principal antagonista. Nasceu em 31 de dezembro de 1926.
    Foi o herdeiro de Salazar Sonserina. Criou 7 Horcruxes para buscar a imortalidade.
    Era o líder dos Comensais da Morte. Tinha grande habilidade em magia das trevas e parseltongue (língua das cobras).
    """,
    """
    Alvo Dumbledore foi o diretor de Hogwarts por muitas décadas. Nasceu em 1881, considerado o bruxo mais poderoso de sua época.
    Era um bruxo sangue puro, irmão de Aberforth e Ariana Dumbledore. Derrotou Grindelwald em 1945.
    Possuía a Varinha das Varinhas (Varinha de Sabugueiro). Era mestre em diversas formas de magia.
    """,
    """
    Severo Snape foi professor de Poções e depois diretor de Hogwarts. Nasceu em 9 de janeiro de 1960.
    Era um mestre em poções e oclumência. Trabalhou como espião duplo para Dumbledore.
    Amava Lílian Potter (mãe de Harry). Seu patrono era uma corça, o mesmo de Lílian.
    """,
    """
    Rúbeo Hagrid é o guarda-caça e professor de Tratamento das Criaturas Mágicas em Hogwarts.
    É um meio-gigante, com 3,5 metros de altura. Foi quem apresentou o mundo mágico a Harry.
    Possui um dragão chamado Norberto e um cão gigante chamado Fofo.
    """,
    """
    Draco Malfoy é o rival de Harry em Hogwarts. Nasceu em 5 de junho de 1980, filho de Lúcio e Narcisa Malfoy.
    É da Casa Sonserina. Seu pai era um Comensal da Morte. Possui um corujão chamado Pichitinho.
    """,
    """
    Grifinória é uma das quatro casas de Hogwarts, fundada por Godric Gryffindor.
    Valoriza coragem, determinação, audácia e cavalheirismo. Suas cores são vermelho e dourado.
    Seu animal símbolo é o leão. A fantasma da casa é o Barão Sangrento.
    O Chapéu Seletor quase sempre coloca estudantes corajosos na Grifinória. Membros famosos incluem Harry, Hermione, Rony e Dumbledore.
    """,
    """
    Sonserina é a casa fundada por Salazar Slytherin. Valoriza ambição, astúcia, liderança e pureza de sangue.
    Suas cores são verde e prata. Seu animal símbolo é a serpente. O fantasma da casa é o Barão Sangrento.
    A Sala Comunal fica nas masmorras do castelo. Membros famosos incluem Merlin, Voldemort e Snape.
    """,
    """
    Corvinal é a casa fundada por Rowena Ravenclaw. Valoriza inteligência, criatividade, aprendizado e sabedoria.
    Suas cores são azul e bronze. Seu animal símbolo é a águia. O fantasma da casa é a Dama Cinzenta.
    A entrada da Sala Comunal exige responder a uma charada. Membros famosos incluem Luna Lovegood e Cho Chang.
    """,
    """
    Lufa-Lufa é a casa fundada por Helga Hufflepuff. Valoriza lealdade, paciência, trabalho duro e justiça.
    Suas cores são amarelo e preto. Seu animal símbolo é o texugo. O fantasma da casa é o Frei Gorducho.
    A Sala Comunal fica perto das cozinhas. Membros famosos incluem Cedrico Diggory e Newt Scamander.
    """,
    """
    Harry Potter e a Pedra Filosofal é o primeiro livro (1997). Harry descobre que é bruxo e vai para Hogwarts.
    Ele faz amizade com Rony e Hermione. Descobre a Pedra Filosofal e enfrenta o Professor Quirrell (possuído por Voldemort).
    """,
    """
    Harry Potter e a Câmara Secreta é o segundo livro (1998). O Monstro da Câmara Secreta é aberto.
    Harry descobre que é um Parselmouth (fala com cobras). Enfrenta o basilisco e destrói o primeiro Horcrux de Voldemort.
    """,
    """
    Harry Potter e o Prisioneiro de Azkaban é o terceiro livro (1999). Sirius Black escapa de Azkaban.
    Harry descobre que Sirius é seu padrinho. Aprende o feitiço do Patrono para afastar Dementadores.
    """,
    """
    Harry Potter e o Cálice de Fogo é o quarto livro (2000). Harry é misteriosamente inscrito no Torneio Tribruxo.
    Competidores: Harry, Cedrico Diggory, Viktor Krum e Fleur Delacour. Cedrico é morto por Pettigrew.
    Voldemort retorna ao corpo físico. Ocorre a Dança de Inverno.
    """,
    """
    Harry Potter e a Ordem da Fênix é o quinto livro (2003). A Ordem da Fênix é reformada contra Voldemort.
    Harry ensina a Armada de Dumbledore. Batalha no Departamento de Mistérios. Sirius Black é morto por Bellatrix.
    Dumbledore revela a profecia sobre Harry e Voldemort.
    """,
    """
    Harry Potter e o Enigma do Príncipe é o sexto livro (2005). Harry descobre o antigo livro de poções do Príncipe Mestiço.
    Dumbledore ensina sobre Horcruxes. Snape mata Dumbledore. Ocorre a invasão de Hogwarts pelos Comensais da Morte.
    """,
    """
    Harry Potter e as Relíquias da Morte é o sétimo livro (2007). Harry, Rony e Hermione procuram os Horcruxes.
    Descobrem as Relíquias da Morte: Varinha das Varinhas, Pedra da Ressurreição e Capa da Invisibilidade.
    Batalha Final de Hogwarts. Harry descobre que é o verdadeiro mestre da Varinha das Varinhas.
    Voldemort é derrotado. Epílogo: 19 anos depois, seus filhos vão para Hogwarts.
    """,
    """
    Expecto Patronum é o feitiço que conjura um Patrono, uma força positiva que repele Dementadores.
    Requer uma memória muito feliz. O Patrono de Harry é um cervo, de Hermione é uma lontra, de Rony é um Jack Russell Terrier.
    Dumbledore pode conjurar um Patrono sem varinha, que é uma fênix.
    """,
    """
    Avada Kedavra é a Maldição Mortal, uma das três Maldições Imperdoáveis. Causa morte instantânea.
    Não tem contra-feitiço. Foi usada por Voldemort para matar os pais de Harry e tentar matar Harry.
    """,
    """
    Expelliarmus é o feitiço de desarmamento, um dos favoritos de Harry. Desarma o oponente, enviando sua varinha para o usuário.
    Harry usou contra Voldemort na batalha final, revelando que era o mestre da Varinha das Varinhas.
    """,
    """
    A Poção Polissuco permite ao bebedor assumir a aparência de outra pessoa por uma hora.
    É extremamente difícil de preparar. Hermione a usou no segundo ano para se transformar em Pansy Parkinson.
    Harry e Rony usaram para se transformar em Crabbe e Goyle.
    """,
    """
    A Poção Felix Felicis é chamada de "Sorte Líquida". Dá sorte a quem a bebe.
    É extremamente perigosa se usada em excesso. Harry a usou para obter memórias de Slughorn sobre Horcruxes.
    """,
    """
    Dragões são criaturas extremamente perigosas. Existem várias espécies: Ucraniano, Chinês, Húngaro.
    Harry enfrentou um dragão no Torneio Tribruxo. Hagrid tem um dragão chamado Norberto (fêmea).
    """,
    """
    Hipogrifos são criaturas com corpo de cavalo e cabeça de águia. Requerem respeito.
    Bicuço é um hipogrifo amigo de Hagrid e Harry. Foi condenado à morte após atacar Draco, mas foi salvo.
    """,
    """
    Dementadores são criaturas que sugam a felicidade e podem dar o Beijo da Morte.
    Guardam a prisão de Azkaban. Harry os repeliu com o feitiço Patrono.
    """,
    """
    O Basilisco é uma serpente gigante, o Rei das Cobras. Seu olhar mata instantaneamente.
    Viver na Câmara Secreta por 1000 anos. Harry o matou com a Espada de Gryffindor no segundo ano.
    """,
    """
    A Varinha das Varinhas (Varinha de Sabugueiro) é a varinha mais poderosa que existe.
    Foi criada por Death, uma das Relíquias da Morte. Pertenceu a Dumbledore, Draco e depois Harry.
    Sua lealdade é conquistada ao derrotar o dono anterior.
    """,
    """
    A Capa da Invisibilidade é uma das Relíquias da Morte, herdada por Harry de seu pai.
    Esconde o usuário da morte. É uma das mais perfeitas capas de invisibilidade que existem.
    """,
    """
    A Pedra da Ressurreição é uma das Relíquias da Morte, pode trazer os mortos de volta.
    Foi deixada por Dumbledore para Harry. Ele a usou para ver seus pais, Sirius e Lupin antes da morte.
    """,
    """
    O Chapéu Seletor é um artefato mágico que decide em qual casa de Hogwarts um aluno será colocado.
    Pertenceu a Godric Gryffindor. Contém a inteligência dos quatro fundadores.
    """,
    """
    A Pedra Filosofal pode transformar qualquer metal em ouro e produzir o Elixir da Vida (imortalidade).
    Foi destruída por Dumbledore após o primeiro ano para evitar que Voldemort a obtivesse.
    """,
    """
    Hogwarts é a Escola de Magia e Bruxaria, fundada há mais de 1000 anos pelos quatro fundadores.
    Localizada na Escócia, é considerada a melhor escola de magia do mundo.
    Possui escadarias móveis, retratos falantes, salas secretas e uma grande área de árvore proibida.
    """,
    """
    O Beco Diagonal é uma rua escondida em Londres onde bruxos compram material escolar.
    Pode ser acessado através do Caldeirão Furado. Lá ficam o Banco Gringotes, Ollivanders, e a Floreios e Borrões.
    """,
    """
    Azkaban é a prisão dos bruxos, guardada por Dementadores. Localizada em uma ilha remota.
    Sirius Black foi o único prisioneiro a escapar. Dementadores foram removidos após a ascensão de Kingsley Shacklebolt.
    """,
    """
    A Casa dos Weasley, chamada Toca, fica em Ottery St. Catchpole. É uma construção torta, claramente sustentada por magia.
    Possui um jardim com gnomos, um galinheiro e um relógio mágico que mostra onde cada membro da família está.
    """,
    """
    O Ministério da Magia é o governo do mundo bruxo britânico, localizado em Londres.
    Possui diversos departamentos: Execução das Leis da Magia, Regulamentação de Criaturas Mágicas, Transportes Mágicos.
    Seus ministros incluem Cornelius Fudge, Rufus Scrimgeour e mais tarde Hermione Granger.
    """,
    """
    A Ordem da Fênix é uma organização secreta fundada por Dumbledore para combater Voldemort.
    Membros incluem Sirius Black, Remo Lupin, Nymphadora Tonks, Kingsley Shacklebolt e os Weasley.
    """,
    """
    Os Comensais da Morte são seguidores de Voldemort. Marca na mão esquerda (Marca Negra).
    Membros incluem Lúcio Malfoy, Bellatrix Lestrange, Peter Pettigrew e Severo Snape (como espião).
    """,
    """
    A Quadribol é o esporte mais popular do mundo bruxo. Quatro bolas: Goles, Balaços e Pomo de Ouro.
    Times têm 7 jogadores: 3 artilheiros, 2 batedores, 1 goleiro e 1 apanhador (Harry jogava como apanhador).
    """,
]


class HarryPotterWebScraper:
    """Classe para fazer web scraping de conteúdo sobre Harry Potter"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def scrape_wikipedia(self, character: str) -> str:
        """Scrape de informações da Wikipedia"""
        try:

            name_formatted = character.replace(" ", "_")
            url = f"https://pt.wikipedia.org/wiki/{name_formatted}"

            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                content_div = soup.find("div", {"class": "mw-parser-output"})
                if content_div:
                    paragraphs = content_div.find_all("p")
                    text = " ".join([p.get_text() for p in paragraphs[:3]])

                    if len(text) > 100:
                        return (
                            f"Informações sobre {character} (Wikipedia):\n{text[:1000]}"
                        )

            return ""
        except Exception as e:
            print(f"Erro ao scraper Wikipedia para {character}: {e}")
            return ""

    def scrape_potter_fandom(self, character: str) -> str:
        """Scrape do Fandom Harry Potter"""
        try:
            name_formatted = character.replace(" ", "_")
            url = f"https://harrypotter.fandom.com/pt/wiki/{name_formatted}"

            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                content = soup.find("div", {"class": "mw-parser-output"})
                if content:
                    paragraphs = content.find_all("p")
                    text = " ".join([p.get_text() for p in paragraphs[:2]])

                    if len(text) > 100:
                        return f"Informações sobre {character} (Fandom):\n{text[:800]}"

            return ""
        except Exception as e:
            print(f"Erro ao scraper Fandom para {character}: {e}")
            return ""

    def scrape_harrypotter_fandom(self):
        """Scrape da página principal do Fandom"""
        texts = []
        urls = [
            "https://harrypotter.fandom.com/pt/wiki/Harry_Potter_(s%C3%A9rie)",
            "https://harrypotter.fandom.com/pt/wiki/Hogwarts",
            "https://harrypotter.fandom.com/pt/wiki/Magia",
            "https://harrypotter.fandom.com/pt/wiki/Varinhas",
            "https://harrypotter.fandom.com/pt/wiki/Feiti%C3%A7os",
        ]

        for url in urls:
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    content = soup.find("div", {"class": "mw-parser-output"})

                    if content:
                        paragraphs = content.find_all("p")
                        text = " ".join([p.get_text() for p in paragraphs[:4]])

                        if len(text) > 200:
                            texts.append(
                                f"Informações (Harry Potter Wiki):\n{text[:1200]}"
                            )

                time.sleep(1)
            except Exception as e:
                print(f"Erro ao scraper {url}: {e}")

        return texts

    def scrape_all(self) -> List[str]:
        """Executa todos os scrapers"""
        print("Iniciando web scraping para enriquecer a base de conhecimento...")
        all_texts = []

        characters = [
            "Harry_Potter",
            "Hermione_Granger",
            "Ron_Weasley",
            "Albus_Dumbledore",
            "Lord_Voldemort",
        ]

        for character in characters:
            wiki_text = self.scrape_wikipedia(character)
            if wiki_text:
                all_texts.append(wiki_text)

            fandom_text = self.scrape_potter_fandom(character)
            if fandom_text:
                all_texts.append(fandom_text)

            time.sleep(1)

        general_texts = self.scrape_harrypotter_fandom()
        all_texts.extend(general_texts)

        print(f"Web scraping concluído! {len(all_texts)} novos textos adicionados.")
        return all_texts


def criar_base_conhecimento():
    """Cria os documentos e chunks da base de conhecimento com web scraping"""

    all_texts = TEXTOS_CONHECIMENTO_MANUAL.copy()

    try:
        scraper = HarryPotterWebScraper()
        scraped_texts = scraper.scrape_all()
        all_texts.extend(scraped_texts)
    except Exception as e:
        print(f"⚠️ Web scraping falhou: {e}")
        print("Continuando apenas com base de conhecimento manual...")

    documentos = [
        Document(page_content=texto, metadata={"fonte": f"harry_potter_doc_{i}"})
        for i, texto in enumerate(all_texts)
    ]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documentos)

    print(f"Base de conhecimento criada:")
    print(f"   - Documentos: {len(documentos)}")
    print(f"   - Chunks: {len(chunks)}")
    print(f"   - Origem: Manual + Web Scraping")

    return documentos, chunks


def get_textos_base():
    """Retorna os textos da base de conhecimento"""
    return TEXTOS_CONHECIMENTO_MANUAL
