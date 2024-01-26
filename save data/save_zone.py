import json
from rdflib import Graph, Namespace, URIRef, Literal
import add_plants


def rdf_to_jsonld(subject, rdf_data, output_path):
    # Create an RDF graph
    g = Graph()
    #print(subject)

    # Define a namespace for your properties
    ns = Namespace("https://dbpedia.org/property/")

    # Add triples to the graph
    subject_uri = URIRef(f"http://127.0.0.1:5000/zone/{subject.replace(' ', '%20')}")
    g.add((subject_uri, ns.label, Literal(rdf_data['label'])))
    g.add((subject_uri, ns.list_of_plants, Literal(rdf_data['list_of_plants'])))
    g.add((subject_uri, ns.positioning, Literal(rdf_data['positioning'])))
    g.add((subject_uri, ns.positioning, Literal(rdf_data['description'])))

    # Serialize RDF graph to JSON-LD format
    jsonld_data = {
        "@context": {
            "label": "https://dbpedia.org/property/label",
            "list_of_plants": "https://dbpedia.org/property/list_of_plants",
            "description": "https://dbpedia.org/property/description",
            "positioning": "https://dbpedia.org/property/positioning"
        },
        "@id": f"http://127.0.0.1:5000/zone/{subject.replace(' ', '%20')}",
        **rdf_data
    }

    # Save JSON-LD data to a file
    with open(output_path, 'w') as jsonld_file:
        json.dump(jsonld_data, jsonld_file, indent=2)


def save_zones(zone_name, list_of_plants, positioning, description):
    rdf_data = {'label': zone_name, 'list_of_plants': list_of_plants, 'description': description,
                'positioning': positioning}
    output_path = f'D:/WAD3/WADe-Project/apache jena/dataset/zones/{zone_name}.jsonld'
    rdf_to_jsonld(zone_name, rdf_data, output_path)


save_zones("Zona 1 - Sectia Sistematica", add_plants.create_list_plants("Zona 1 - Sectia Sistematica"), "---",
           "Terenul destinat sectiei este strabatut de o serie de alei radiale si circulare ce permit accesul "
           "vizitatorilor catre straturile de plante si care indeplinesc si un rol stiintific (filogenetic), "
           "prin separarea ordinelor si familiilor intre ele. O alee circulara lata de 3 m separa ordinele cu flori "
           "dialipetale (cu petale libere), dispuse spre centrul sectiei, de cele cu flori simpetale (cu petale unite) "
           "dispuse spre periferia sectiei.Chiar de la intrarea in sectie, pe partea stanga, se pot observa"
           " doua exemplare de Metasequoia gliptostroboides, specie din familia Taxodiaceae, cunoscuta doar ca planta "
           "fosila pana in anul 1941, cand studentii chinezi Cheng si Hu au descoperit-o in stare vie, in padurile din"
           " Centrul Chinei.")

save_zones("Zona 2 - Sectia Fitogeografica", add_plants.create_list_plants("Zona 2 - Sectia Fitogeografica"), "---",
           "In fata stancariei un 'ceas solar' are marcate orele prin 12 trovanti (sfere de gresie) adusi de pe"
           " Dealul Feleacului. In mijlocul 'ceasului' un trovant mai mare, simbolizand globul pamantesc, isi trimite"
           " umbra la fiecare ora din zi pe trovantul corespunzator orei respective. In vecinatatea stancariei "
           "se etaleaza culorile vii, diverse, ale plantelor din America Centrala si de Sud si din Africa, cultivate "
           "in clima noastra ca plante anuale: Ageratum (pufuleti), Cosmos, Eschscholtzia (mac de California),"
           " Portulaca, Mirabilis, Agastache, Zinnia, Tagetes, Argemone, Cuphea, Gomphrena, Gazania, Dimorphoteca etc.")




save_zones("Zona 3 - Complexul de sere", add_plants.create_list_plants("Zona 3 - Complexul de sere"), "---",
           "Complexul de sere adaposteste circa 2.600 taxoni, cu origine în tinuturile subtropicale, tropicale"
           " si ecuatoriale ale globului. Colectiile sunt grupate dupa provenienta geografica a plantelor, tinând"
           " cont de cerintele ecologice, în sere calde, temperate sau reci. Colectia plantelor xerofile reprezinta o"
           " asociatie eterogena de taxoni cu aspect arboricol, care provin din zone cu climat subtropical de tip "
           "mediteranean. Cei mai multi taxoni sunt binecunoscuti: maslinul (Olea europaea), rodiul (Punica granatum),"
           " roscovul (Ceratonia siliqua), oleandrul (Nerium oleander), rosmarinul (Rosmarinus officinalis), "
           "chiparosul (Cupressus sempervirens). Vegetatia din zonele analoage celor mediteraneene, localizata în sudul"
           " Africii de Sud este reprezentata in colectiile noastre prin speciile Myrsine africana, "
           "Agapanthus africanus (crin albastru), Haemanthus albiflos, Clivia miniata (crin rosu).")


save_zones("Zona 4 - Sectia Flora si Vegetatia Romaniei",
           add_plants.create_list_plants("Zona 4 - Sectia Flora si Vegetatia Romaniei"), "---",
           "Principiul de baza este cel al reprezentarii pe verticala a principalelor zone si etaje de vegetatie din "
           "tara noastra (favorizata de formele de relief naturale existente), iar pe orizontala a florei si "
           "vegetatiei specifice fiecarei provincii istorice a Romaniei. Un alt principiu este cel al conservarii "
           "prin cultura a unui fond genetic vegetal cat mai variat din flora tarii noastre (popularea acestei sectii "
           "se realizeaza cu material autentic, colectat din flora spontana a tinuturilor respective).")

save_zones("Zona 5 - Sectia Silvostepa Moldovei",
           add_plants.create_list_plants("Zona 5 - Sectia Silvostepa Moldovei"), "---",
           "Sectia Silvostepa Moldovei se gaseste in partea de nord a Gradinii Botanice, ocupand o suprafata de 13,"
           "92 hectare. Se invecineaza la sud cu sectiile Flora si Vegetatia Romaniei si Flora Globului, la nord si "
           "vest cu Ferma Agricola Copou, iar la est cu proprietati particulare.")

save_zones("Zona 6 - Sectia Biologica", add_plants.create_list_plants("Zona 6 - Sectia Biologica"), "---",
           "La intrarea in sectie, strajuita de o parte si de alta de coloanele arborelui vietii (Thuja occidentalis "
           "‘Fastigiata’), sunt amenajate doua grupuri de stancarii care prezinta unele aspecte ale evolutiei "
           "vietuitoarelor.Stancaria din partea nordica a sectorului, alcatuita din calcar de la Repedea - Iasi, "
           "prezinta vizitatorului unele dovezi paleontologice ale procesului de evolutie, printr-o bogata fauna "
           "fosila, mai ales moluste, sedimentate in gresiile calcaroase de varsta sarmatianului mijlociu. In aceasta "
           "stancarie sunt prezentate aspecte ale evolutiei florii de la cea actinomorfa spre cea zigomorfa si "
           "respectiv, de la floarea dialipetala (cu petale libere) spre gamopetala (cu petale concrescute).")

save_zones("Zona 7 - Sectia Plante Utile", add_plants.create_list_plants("Zona 7 - Sectia Plante Utile"), "---",
           "Prin tematica sectiei si transpunerea acesteia în teren se urmareste reprezentarea a peste 450 de taxoni "
           "vegetali pe principale grupe de utilitati, fiind expuse catre public colectii de plante utilizate în "
           "industria alimentara, specii de plante medicinale, aromatice si condimentare, melifere si furajere, "
           "tanante si tinctoriale, dar si specii de plante toxice.")

save_zones("Zona 8 - Sectia Dentrarium", add_plants.create_list_plants("Zona 8 - Sectia Dentrarium"), "---",
           "Colectiile de arbori si arbusti au fost grupate pe genuri si in functie de cerintele ecologice ale "
           "plantelor, urmarindu-se valorificarea potentialului stational local. In amenajarea sectiei s-a folosit "
           "stilul mixt, cu inclinatie spre cel peisager. La contact cu orasul, sectia este protejata de o perdea "
           "perimetrala arborescenta alcatuita, preponderent, din specii indigene rustice care au coronament des. "
           "Dendrarium-ul are o forma oarecum dreptunghiulara si prezinta o axa de simetrie orientata nord-sud ce "
           "marcheaza limita dintre subsectiile Gymnospermae si Angiospermae. Aleile pietonale, mai inguste, "
           "intersecteaza din loc in loc axa de simetrie si fac legatura cu toate punctele din sectie, inclusiv cu "
           "cele perimetrale.")

save_zones("Zona 9 - Sectia Ornamentala", add_plants.create_list_plants("Zona 9 - Sectia Ornamentala"), "---",
           "Grupate in colectii, genurile Tulipa, Narcissus, Crocus, Hyacinthus, Muscari, sunt prezentate in spatiile "
           "tranzitorii ale sectiei, acestea oferind o gama coloristica foarte variata si trecand prin tot spectrul, "
           "devin o adevarata expozitie de culoare. In ultimii 10 ani, aceste genuri au dobandit o reala importanta "
           "datorita diversitatii soiurilor introduse in cultura in spatiile destinate sectiei ornamentale.")

save_zones("Zona 10 - Sectia Rosarium", add_plants.create_list_plants("Zona 10 - Sectia Rosarium"), "---",
           "Pentru a evidentia prezenta colectiei de roze pe fondul verde al peluzei inierbate, in ansamblul "
           "compozitional al Rosarium-ului, la periferie, s-au plantat conifere de talie inalta: Pinus nigra, "
           "Pinus sylvestris, Thuja orientalis, Taxus baccata, precum si specii de talie mica spre centru: Buxus "
           "sempervirens si Juniperus horizontalis. Ca elemente de contrast, sunt plantate intercalat sau in grupuri "
           "speciile: Betula pendula, Larix decidua, Picea pungens 'Argentea', Albizia julibrissin, "
           "Cercis siliquastrum, Magnolia kobus, Spiraea × vanhouttei si Tamarix ramosissima.")
