import json, re

# (nome, nasc, fale, nacionalidade, profissao, status, page_url, tem_foto)
R = [
("Akash Bashir",1994,2015,"Paquistão","Segurança voluntário","Servo de Deus","3ac3bb9d990881e29b40c16eb8943b25",1),
("Albertina Berkenbrock",1919,1931,"Brasil","Estudante","Beato","3ac3bb9d9908818f9158fc2a8f3ddf87",0),
("André Bessette",1845,1937,"Canadá","Religioso / Porteiro","Santo","3ac3bb9d990881ef844df5224486fb79",1),
("Antonietta Meo (Nennolina)",1930,1937,"Itália","Criança","Venerável","3ac3bb9d99088191bf8ee76628572642",1),
("Augustus Tolton",1854,1897,"Estados Unidos","Padre","Venerável","3ac3bb9d990881218885d99ac4beb76d",1),
("Bernadette Soubirous",1844,1879,"França","Freira / Enfermeira","Santo","19b3bb9d99088046a7e8df4770dd29fa",1),
("Carlo Acutis",1991,2006,"Itália","Estudante / Web Designer","Santo","19b3bb9d9908800b94cecc749d064caa",1),
("Carlos Manuel Rodríguez",1918,1963,"Porto Rico","Professor","Beato","19b3bb9d990880a28cd6e84a6b332689",1),
("Carmen Hernández",1930,2016,"Espanha","Missionária","Servo de Deus","19b3bb9d990880b5887aee05a15e5a1d",1),
("Charles de Foucauld",1858,1916,"França","Padre / Eremita","Santo","3ac3bb9d99088104b7d8f38cebad6018",1),
("Chiara Badano",1971,1990,"Itália","Estudante","Beato","19b3bb9d990880a99f4bdb286104365e",1),
("Chiara Petrillo",1984,2012,"Itália","Do lar / Mãe","Servo de Deus","19b3bb9d99088055b2aee821a9824266",1),
("Clare Crockett",1982,2016,"Irlanda do Norte","Freira / Atriz","Servo de Deus","19b3bb9d9908809d981cf411f6dac89d",1),
("Clarita Segura",1978,1995,"Argentina","Estudante","Servo de Deus","19b3bb9d9908805eac28c7693883b46d",1),
("Cleusa Carolina Rody Coelho",1933,1985,"Brasil","Freira / Missionária","Servo de Deus","3ac3bb9d99088123b2d0c28aa43fa276",1),
("Cyprien Rugamba",1944,1994,"Ruanda","Missionário","Servo de Deus","19b3bb9d9908809f9a3bd971d5e7a092",1),
("Dom Hélder Câmara",1909,1999,"Brasil","Bispo","Servo de Deus","3ac3bb9d990881a58d8dc7d8f14bc998",1),
("Dorothy Day",1897,1980,"Estados Unidos","Jornalista / Ativista","Servo de Deus","3ac3bb9d99088186a9b9c075b0bcea6b",1),
("Dulce Lopes Pontes (Santa Dulce dos Pobres)",1914,1992,"Brasil","Freira / Enfermeira","Santo","3ac3bb9d99088119b925c90d183469d9",0),
("Edith Stein",1891,1942,"Polônia","Freira","Santo","19b3bb9d99088071a933c3e0ea6deeb6",1),
("Emil Kapaun",1916,1951,"Estados Unidos","Militar / Padre","Servo de Deus","19b3bb9d990880a191e1c18479595dcb",1),
("Enrique Shaw",1921,1962,"Argentina","Empresário","Venerável","19b3bb9d99088076af38fb00e83d7bd9",1),
("Ezequiel Ramin",1953,1985,"Brasil (nascido na Itália)","Padre missionário","Servo de Deus","3ac3bb9d9908816ca6b6c050b9bbd910",1),
("Francis Xavier Nguyễn Văn Thuận",1928,2002,"Vietnã","Bispo / Cardeal","Venerável","3ac3bb9d99088105b32ed88ca5e8f052",1),
("Francisca de Paula de Jesus (Nhá Chica)",1810,1895,"Brasil","Leiga","Beato","3ac3bb9d9908810492f7dad655987aaf",1),
("Francisco Marto",1908,1919,"Portugal","Estudante","Santo","19b3bb9d9908807697faf27c0c035ced",1),
("Franz de Castro Holzwarth",1942,1981,"Brasil","Advogado","Servo de Deus","3ac3bb9d9908814483b8fc664a2a5ac5",1),
("Franz Jägerstätter",1907,1943,"Áustria","Agricultor","Beato","3ac3bb9d9908813fbafefe0794a0c99e",1),
("Frei Damião de Bozzano",1898,1997,"Brasil (nascido na Itália)","Padre missionário","Venerável","3ac3bb9d9908815c801ee8b7ed9c71bb",1),
("Fulton Sheen",1895,1979,"Estados Unidos","Padre / Professor / Apresentador de tv e rádio","Venerável","19b3bb9d990880fb9281c8db15c4bcbb",1),
("Gemma Galgani",1878,1903,"Itália","Estudante","Santo","19b3bb9d9908801da328f833ea595f79",1),
("Gianna Beretta Molla",1922,1962,"Itália","Médica / Esposa / Mãe","Santo","19b3bb9d990880419995d659c7d83f7d",1),
("Giuseppe Moscati",1880,1927,"Itália","Médico / Professor","Santo","19b3bb9d99088009acc7e246412d328d",1),
("Guido Schaffer",1974,2009,"Brasil","Seminarista / Médico","Venerável","19b3bb9d990880c0b871d56cc2e9216e",1),
("Helena Kmiec",1991,2017,"Polônia","Estudante / Missionária","Servo de Deus","19b3bb9d990880f2a95ee9716eea7cd3",1),
("Isabel Cristina Mrad Campos",1962,1982,"Brasil","Estudante de Direito","Beato","3ac3bb9d990881d1a272dee08ca0904c",1),
("Isidore Bakanja",1887,1909,"República Democrática do Congo","Catequista","Beato","3ac3bb9d990881ce8f53cece62d8c828",1),
("Jacinta Marto",1910,1920,"Portugal","Estudante","Santo","19b3bb9d990880eda892cb11c87d5a6d",1),
("Jacques Fesch",1930,1957,"França","Presidiário","Servo de Deus","19b3bb9d99088040b440f4c69f6a1e7c",1),
("James Miller",1944,1982,"Estados Unidos","Padre / Professor / Missionário","Beato","19b3bb9d990880918d05fb50b7590419",1),
("John Henry Newman",1801,1890,"Inglaterra","Cardeal / Teólogo / Escritor","Santo","3ac3bb9d990881ad8c0bdfeb2f9887da",1),
("Josemaría Escrivá",1902,1975,"Espanha","Padre","Santo","19b3bb9d990880709fceea51017d37c3",1),
("Josephine Bakhita",1869,1947,"Sudão","Freira","Santo","3ac3bb9d990881c892e0fe26898ca3de",1),
("José Sánchez del Río",1913,1928,"México","Estudante","Santo","3ac3bb9d99088125a764d05a63cc6ae8",1),
("João Luiz Pozzobon",1904,1985,"Brasil","Diácono / Pai de família","Venerável","3ac3bb9d990881faba44c114f08a80b0",1),
("João Paulo I",1912,1978,"Itália","Papa","Venerável","3ac3bb9d990881438fcbd2165d7f539e",1),
("João XXIII",1881,1963,"Itália","Papa","Santo","3ac3bb9d99088145a4abf92e87b4bc77",1),
("Lindalva Justo de Oliveira",1953,1993,"Brasil","Freira","Beato","3ac3bb9d9908818a8761ec4b891fe20c",1),
("Lucia dos Santos",1907,2005,"Portugal","Freira","Venerável","19b3bb9d990880c6be6decc70bacf21b",1),
("Madre Assunta Marchetti",1871,1948,"Brasil (nascida na Itália)","Freira / Missionária / Cofundadora de congregação","Beato","3ac3bb9d9908812fb2e3f41d981a81d2",0),
("Madre Paulina do Coração Agonizante de Jesus",1865,1942,"Brasil (nascida na Itália)","Freira / Fundadora de congregação","Santo","3ac3bb9d9908816ea6b2ca72ecdfaa07",1),
("Marcel Callo",1921,1945,"França","Operário / Tipógrafo","Beato","3ac3bb9d99088171a2f2d76f8abf7f7f",1),
("Marcello Candia",1916,1983,"Brasil (nascido na Itália)","Empresário / Filantropo","Venerável","3ac3bb9d99088181af43ef38840bd085",1),
("Marcelo Henrique Câmara",1979,2008,"Brasil","Advogado / Promotor de Justiça / Professor universitário","Servo de Deus","3ac3bb9d9908818da68ccaa3afd86574",1),
("Maria Cristina Cella",1969,1995,"Itália","Do lar","Venerável","19b3bb9d99088095a771f14f82d56433",1),
("Maria Faustina Kowalska",1905,1938,"Polônia","Freira","Santo","19b3bb9d990880f8b0fce3336d75f4b2",0),
("Maria Goretti",1890,1902,"Itália","Camponesa / Leiga","Santo","3ac3bb9d9908810a9ac7d616fca5497b",1),
("Marie-Clémentine Anuarite Nengapeta",1939,1964,"República Democrática do Congo","Freira","Beato","3ac3bb9d99088187aec3d178b771c496",0),
("Mary MacKillop",1842,1909,"Austrália","Freira / Educadora","Santo","3ac3bb9d99088177be50cf7d9ed0c898",1),
("María Guggiari Echeverría",1925,1959,"Paraguai","Freira","Beato","19b3bb9d990880619677d5a7108afd05",0),
("Matt Talbot",1856,1925,"Irlanda","Operário","Venerável","3ac3bb9d9908815591f5e50491ff6a4d",0),
("Matteo Farina",1990,2009,"Itália","Estudante / Músico","Venerável","19b3bb9d99088079952ff6b0e02595b6",0),
("Maximiliano Kolbe",1894,1941,"Polônia","Padre franciscano","Santo","3ac3bb9d99088100aaaed2c73dcbc35c",1),
("Michelle Duppong",1984,2015,"Estados Unidos","Missionária","Servo de Deus","19b3bb9d990880ad9111e0a2347e88a1",0),
("Miguel Pro",1891,1927,"México","Padre jesuíta","Beato","3ac3bb9d9908810f8e15d80b1b9bf27e",1),
("Padre Donizetti Tavares de Lima",1882,1961,"Brasil","Padre","Beato","3ac3bb9d990881debb09e4fb0e864e1b",1),
("Padre Eustáquio van Lieshout",1890,1943,"Brasil (nascido na Holanda)","Padre / Fundador de hospitais","Beato","3ac3bb9d990881afa626d15790929493",1),
("Padre Léo (Léo Tarcísio Gonçalves Pereira)",1961,2007,"Brasil","Padre / Fundador de comunidade terapêutica","Servo de Deus","3ac3bb9d9908815cb290c2988a20930f",1),
("Padre Pio",1887,1968,"Itália","Padre","Santo","19b3bb9d990880ecad50f8a1b8f92af2",0),
("Papa João Paulo II",1920,2005,"Polônia","Papa","Santo","19b3bb9d9908804d99c3fa7938576f4a",0),
("Paulo VI",1897,1978,"Itália","Papa","Santo","3ac3bb9d9908815fae1ccc3b5267da70",1),
("Peter To Rot",1912,1945,"Papua Nova Guiné","Catequista","Beato","3ac3bb9d990881b3a50aee2269e01ad3",0),
("Pier Giorgio Frassati",1901,1925,"Itália","Estudante","Santo","19b3bb9d9908808b92d8e74a9b6cc199",0),
("Rosario Livatino",1952,1990,"Itália","Juiz","Beato","19b3bb9d9908801398dfdc2f880b0cd1",0),
("Sandra Sabattini",1961,1984,"Itália","Estudante","Beato","19b3bb9d990880a08634fdb9434a0445",0),
("Solanus Casey",1870,1957,"Estados Unidos","Padre","Beato","3ac3bb9d99088145bbb2e62654636ee3",0),
("Stanley Rother",1935,1981,"Estados Unidos","Padre","Beato","19b3bb9d9908802491eec312875b1af7",0),
("Takashi Nagai",1908,1951,"Japão","Médico","Servo de Deus","19b3bb9d990880a9837de784e515644c",0),
("Teresa de Calcutá",1910,1997,"Índia (nascida em Skopje, atual Macedônia do Norte)","Freira","Santo","3ac3bb9d99088144a72ef5cad6143364",0),
("Thea Bowman",1937,1990,"Estados Unidos","Freira / Professora / Música","Servo de Deus","19b3bb9d9908806bae89f97b1487c186",0),
("Thérèse de Lisieux",1873,1897,"França","Freira","Santo","19b3bb9d990880109136e940ddde8537",0),
("Titus Brandsma",1881,1942,"Holanda","Padre / Jornalista / Professor","Santo","3ac3bb9d990881c0ab22f56810e77f7d",0),
("Zilda Arns",1934,2010,"Brasil","Médica","Servo de Deus","3ac3bb9d99088119b319edf5db2e3ea7",0),
("Óscar Romero",1917,1980,"El Salvador","Bispo","Santo","3ac3bb9d99088173b909ebed949960f4",0),
]

def slug(n):
    s = n.lower()
    for a,b in [("á","a"),("à","a"),("ã","a"),("â","a"),("é","e"),("ê","e"),("í","i"),("ó","o"),("õ","o"),("ô","o"),("ú","u"),("ü","u"),("ç","c"),("ñ","n"),("ě","e"),("ễ","e"),("ă","a"),("ị","i"),("ǵ","g")]:
        s = s.replace(a,b)
    s = re.sub(r"[^a-z0-9]+","-",s).strip("-")
    return s

out = []
for nome,nasc,fale,nac,prof,status,pid,temfoto in R:
    out.append({
        "nome": nome, "nasc": nasc, "fale": fale, "nacionalidade": nac,
        "profissao": prof, "status": status,
        "pageId": pid, "temFoto": bool(temfoto),
        "slug": slug(nome),
        "bio": [], "foto": "", "localNasc": "", "localRepouso": "",
    })

with open("santos.json","w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False,indent=1)

print("total:", len(out))
print("com foto:", sum(1 for s in out if s["temFoto"]))
print("slugs unicos:", len({s["slug"] for s in out}) == len(out))
