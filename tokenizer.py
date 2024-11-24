#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Modules to import
import re


# User functions
def get_next_token(i: int, tokens: list[str]) -> str:
    """
    Retourne le prochain token dans la liste s'il existe, sinon une chaîne vide.

    Parameters:
    i (int): L'index actuel dans la liste des tokens.
    tokens (list[str]): La liste des tokens dans une ligne.

    Returns:
    str: Le prochain token ou une chaîne vide si l'index dépasse la longueur de la liste.
    """
    return tokens[i + 1] if i < len(tokens) - 1 else ""


def input_tokenizer(input_file: str) -> list[str]:
    """
    Tokenize un fichier source de langage de programmation imitant la machine de Turing.

    Le tokenizer lit ligne par ligne le fichier d'entrée, identifie les tokens basés sur des regex,
    et retourne une liste d'éléments reconnus.

    Parameters:
    input_file (str): Le chemin du fichier à tokenizer.

    Returns:
    list[str]: Une liste de tokens reconnus ou None en cas d'erreur de parsing.
    """

    # Ouverture et lecture du fichier source
    with open(input_file, "r", encoding="latin-1") as f:
        input_brut = f.read().split("\n")

    list_elements = []

    # Dictionnaire associant les symboles du langage aux regex correspondantes
    symbol2re = {
        "I": r"^[\s\t\n]*I[\s\t\n]*",
        "si": r"^[\s\t\n]*si[\s\t\n]*",
        "%": r"^%.*",  # Commentaire de la ligne (commençant par %)
        "}": r"^[\s\t\n]*}[\s\t\n]*",
        "D": r"^[\s\t\n]*D[\s\t\n]*",
        "boucle": r"^[\s\t\n]*boucle[\s\t\n]*",
        "fin": r"^[\s\t\n]*fin[\s\t\n]*",
        "G": r"^[\s\t\n]*G[\s\t\n]*",
        "#": r"^[\s\t\n]*#[\s\t\n]*",
        "0": r"^[\s\t\n]*0[\s\t\n]*",
        "1": r"^[\s\t\n]*1[\s\t\n]*",
    }

    # Inversion du dictionnaire pour obtenir une correspondance regex -> symbole
    re2symbol = {v: k for k, v in symbol2re.items()}

    # Parcours de chaque ligne du fichier
    for line in input_brut:
        if line.strip().startswith("%"):
            continue  # Ignore la ligne et passe à la suivante
        
        # Prétraitement : normalise les conditions "si(...)" en "si (...)"
        line = re.sub(r"si\(", "si (", line)

        
        # # Réorganise les commentaires pour qu'ils soient au début de la ligne
        # comment_match = re.match(r"(.*?)(%\s*.*)", line)
        # if comment_match:
        #     # Si un commentaire est détecté, le repositionner en début de ligne
        #     code_part = comment_match.group(1).strip()
        #     comment_part = comment_match.group(2).strip()
        #     line = f"{comment_part} {code_part}".strip()
                
        # # Gestion des commentaires (lignes commençant par %)
        # if re.match(symbol2re["%"], line):
        #     list_elements.append(line)
        #     continue

        # Tokenisation basique d'une ligne en fonction des espaces
        tokens = line.split()

        # Parcours de chaque token dans la ligne
        for i, token in enumerate(tokens):
            detected = 0  # Marqueur pour signaler qu'un token a été reconnu
            next_token = get_next_token(
                i, tokens
            )  # Prochain token pour certaines règles contextuelles

            # Recherche du token à partir des regex définies
            for regex in re2symbol.keys():
                matched = re.match(regex, token)
                if matched:
                    detected = 1  # Token reconnu
                    valid_token = re2symbol[regex]

                    # Gestion des syntaxes de condition "si (1)", "si (0)", les transformer en "si(1)", "si(0)"
                    if valid_token == "si" and next_token in ["(1)", "(0)"]:
                        valid_token += f"{next_token}"

                    list_elements.append(
                        valid_token
                    )  # Ajout du token reconnu à la liste
                    break

            # Gestion des tokens non reconnus (erreurs de parsing)
            if not detected and token not in ["(1)", "(0)"]:
                print(f"Élément inattendu : {token}, aborting...")
                return None

    return list_elements
