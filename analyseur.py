#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Modules to import
from tokenizer import get_next_token, input_tokenizer
import argparse
import json


# User functions
def analyseur_syntaxique(list_elements: list) -> bool:
    """
    Analyse un programme sous forme de liste de symboles pour vérifier la syntaxe
    et le bon enchaînement des instructions dans une machine de Turing simulée.

    Paramètres :
    - list_elements : Liste de symboles représentant un programme de machine de Turing.

    Retourne :
    - bool : True si la syntaxe est valide, False sinon.
    """
    # Liste des symboles non valides à l'état initial (q0)
    not_q0_symbols = ["fin", "}"]
    valid_symbols = [
        "I",
        "P",
        "0",
        "1",
        "G",
        "D",
        "fin",
        "boucle",
        "si(0)",
        "si(1)",
        "}",
        "#",
    ]
    K = 0  # Compteur pour suivre l'ouverture et la fermeture des boucles/conditions

    # Si la liste est vide, la syntaxe est invalide
    if not list_elements:
        print("Liste vide : syntaxe invalide")
        return False

    # Récupération du premier symbole pour vérifier la validité initiale
    symbol0 = list_elements[0]

    if symbol0 not in not_q0_symbols:
        # Parcours de tous les symboles du programme
        for i, symbol in enumerate(list_elements):
            # Récupère le symbole suivant pour traiter les enchaînements
            next_symbol = get_next_token(i, list_elements)

            # Ignorer les commentaires
            if symbol.startswith("%"):
                continue

            if next_symbol and next_symbol.startswith("%"):
                next_symbol = get_next_token(i + 1, list_elements)

            # Vérifier si le symbole est valide
            if symbol not in valid_symbols and not symbol.startswith("%"):
                print(f"Symbole invalide : {symbol}")
                return False

            # Traite les symboles d'instruction d'affichage de la bande ('I') ; pause et affichage de la bande ('P')
            if symbol in ["I", "P"]:
                if next_symbol and next_symbol not in [
                    "0",
                    "1",
                    "G",
                    "D",
                    "fin",
                    "P",
                    "#",
                    "si(1)",
                    "si(0)",
                    "boucle",
                    "}",
                ]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                elif next_symbol in ["si(1)", "si(0)", "boucle"]:
                    K += 1

            # Traitement des conditions (si(0), si(1))
            elif symbol in ["si(0)", "si(1)"]:
                if next_symbol and next_symbol not in [
                    "G",
                    "D",
                    "0",
                    "1",
                    "fin",
                    "P",
                    "I",
                    "boucle",
                ]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                if next_symbol == "boucle":
                    K += 1

            # Traitement des symboles d'écrire 0 et d'écrire 1
            elif symbol in ["0", "1"]:
                if next_symbol and next_symbol not in [
                    "G",
                    "D",
                    "fin",
                    "P",
                    "I",
                    "boucle",
                    "si(1)",
                    "si(0)",
                    "}",
                ]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                if next_symbol in ["boucle", "si(1)", "si(0)"]:
                    K += 1
                elif next_symbol == "}":
                    K -= 1

            # Traitement des mouvements de tête G (gauche) et D (droite)
            elif symbol in ["G", "D"]:
                if next_symbol and next_symbol not in [
                    "G",
                    "D",
                    "0",
                    "1",
                    "fin",
                    "P",
                    "I",
                    "boucle",
                    "si(1)",
                    "si(0)",
                    "}",
                ]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                if next_symbol in ["boucle", "si(1)", "si(0)"]:
                    K += 1
                elif next_symbol == "}":
                    K -= 1

            # Traitement du symbole de la fin de boucles ('fin')
            elif symbol == "fin":
                if next_symbol and next_symbol not in ["}", "P", "I"]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                if next_symbol == "}":
                    K -= 1

            # Traitement des accolades fermantes (})
            elif symbol == "}":
                if next_symbol and next_symbol not in [
                    "G",
                    "D",
                    "0",
                    "1",
                    "I",
                    "P",
                    "#",
                    "si(1)",
                    "si(0)",
                    "boucle",
                    "}",
                ]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                if next_symbol in ["si(1)", "si(0)", "boucle"]:
                    K += 1
                elif next_symbol == "}":
                    K -= 1

            # Traitement des boucles
            elif symbol == "boucle":
                if next_symbol and next_symbol not in [
                    "G",
                    "D",
                    "0",
                    "1",
                    "P",
                    "I",
                    "si(1)",
                    "si(0)",
                    "boucle",
                ]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                if next_symbol in ["si(1)", "si(0)", "boucle"]:
                    K += 1

            # Traitement du symbole Fin du programme ('#')
            elif symbol == "#":
                if next_symbol:
                    print("Erreur de Syntaxe : symbole après la fin du programme")
                    return False
    else:
        print(f"Syntaxe invalide, l'état initial ne peut pas commencer par {symbol0}")
        return False

    # Vérifications finales
    if K < 0:
        print("Erreur : Trop de fermetures de blocs")
        return False
    if K > 0:
        print(f"Erreur : Il reste {K} boucle(s) ou condition(s) non fermée(s)")
        return False

    print("Analyse syntaxique réussie : la syntaxe est valide")
    return True


def json_file(list_elements: list, output_file: str) -> None:
    """
    Transforme la structure syntaxique d'un programme en JSON avec numérotation des nœuds.
    """
    structure_syntaxique = []
    context_stack = [structure_syntaxique]
    current_block = structure_syntaxique
    numero_noeud = 0

    for i, symbol in enumerate(list_elements):
        if symbol.startswith("%"):
            continue

        next_symbol = get_next_token(i, list_elements)
        while next_symbol and next_symbol.startswith("%"):
            i += 1
            next_symbol = get_next_token(i, list_elements)

        entry = {
            "type": (
                "instruction"
                if symbol not in ["si(0)", "si(1)", "boucle", "}", "#"]
                else (
                    "condition"
                    if symbol in ["si(0)", "si(1)"]
                    else ("boucle" if symbol == "boucle" else "fermeture")
                )
            ),
            "instruction": symbol,
            "numero_noeud": numero_noeud,
        }

        if next_symbol:
            entry["suivant"] = next_symbol

        if symbol in ["si(0)", "si(1)", "boucle"]:
            nouveau_bloc = []
            entry["contenu"] = nouveau_bloc
            current_block.append(entry)
            context_stack.append(current_block)
            current_block = nouveau_bloc
        elif symbol == "}":
            current_block.append(entry)
            if len(context_stack) > 0:
                current_block = context_stack.pop()
        else:
            current_block.append(entry)

        numero_noeud += 1

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structure_syntaxique, f, ensure_ascii=False, indent=4)
        print(f"Fichier JSON généré avec succès : {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier JSON : {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyseur syntaxique pour machine de Turing"
    )
    parser.add_argument("input_file_path", help="Fichier d'entrée à analyser")
    args = parser.parse_args()

    list_elements = input_tokenizer(args.input_file_path)
    if list_elements is None:
        print("Erreur lors de la tokenization")
        return

    if analyseur_syntaxique(list_elements):
        json_file(list_elements, "structure_syntaxique.json")


if __name__ == "__main__":
    main()
