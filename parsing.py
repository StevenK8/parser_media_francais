# Parse a tsv file and return a list of dictionnaries
from os import truncate


def parse_tsv(tsv_file):
    """
    Parse a tsv file and return a list of dictionnaries
    """
    # Open the file
    with open(tsv_file, 'r', encoding='utf-8') as tsv:
        # Create a list of dictionnaries
        tsv_list = []
        j = 0
        # For each line in the file
        for line in tsv:
            # Split the line by tab
            line_list = line.split("\t")
            # Create a dictionnary
            line_dict = {}
            # For each element in the line
            for i in range(0, len(line_list)):
                # Add the element to the dictionnary
                if(j == 0):
                    index_dict = line_list
                if(line_list[i] != "\n"):
                    line_dict[remove_newline(index_dict[i])] = remove_newline(line_list[i])
            # Add the dictionnary to the list
            if(j > 0):
                tsv_list.append(line_dict)
            j += 1

        # Return the list
        return tsv_list

# Removes the newline character from a string
def remove_newline(string):
    """
    Removes the newline character from a string
    """
    return string.replace("\n", "")


# Récupère une chaine de texte entrée par l'utilisateur
def get_user_input(message):
    """
    Récupère une chaine de texte entrée par l'utilisateur
    """
    return input(message)

medias_francais = parse_tsv('tsv/medias_francais.tsv')

relations_medias = parse_tsv('tsv/relations_medias_francais.tsv')

#Affiche le champ "nom" d'un dictionnaire si le champ "mediaType" est "Média"
def affiche_nom_media(media):
    if(media["typeLibelle"] == "Média"):
        print(media["nom"]) 
        
#Parcourt une liste de dictionnaires et appelle affiche_nom_media pour chaque dictionnaire
def affiche_nom_media_list(liste):
    print("Liste des médias : ")
    for media in liste:
        affiche_nom_media(media)
        
affiche_nom_media_list(medias_francais)

#Vérifie si une chaine de caractère est un nombre
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Récupère l'origine d'un média à partir de sa cible
def get_origine_media(nom, valeur):
    printVal = True
    for relation in relations_medias:
        if is_equal(relation["cible"],nom):
            #if relation["valeur"] is a number
            if (is_number(relation["valeur"])):
                get_origine_media(relation["origine"],(float(relation["valeur"])/100)*valeur)
            else:
                get_origine_media(relation["origine"],valeur)
            printVal = False
       
    type_media = get_type_media(nom)
    if printVal and type_media != "notfound":
        if (valeur == 0):
            print("\t", nom, "("+type_media+")")
        else:
            print("\t", str(simplify((float(relation["valeur"])/100)*valeur))+"% par", nom, "("+type_media+")")
    elif printVal:
        print("\tCe média n'existe pas. Veuillez réessayer.")

#Vérifie si deux strings sont égaux (sans tenir compte de la casse)
def is_equal(s1, s2):
    return s1.lower() == s2.lower()

#Récupère le typeLibelle d'un média à partir de son nom
def get_type_media(nom):
    for media in medias_francais:
        if(is_equal(media["nom"],nom)):
            return media["typeLibelle"]
    return "notfound"

        
#Round a float to 2 decimals
def simplify(x):
    return round(x, 2)

nom_media = get_user_input("\nEntrez le nom du media : ")
get_origine_media(nom_media,100)