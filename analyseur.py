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

    # Liste des symboles qui ne sont pas valides à l'état initial (q0)
    not_q0_symbols = ["fin", "}"]
    K = 0  # Compteur pour suivre l'ouverture et la fermeture des boucles/conditions

    # Si la liste est vide, la syntaxe est invalide
    if not list_elements:
        return False

    # Récupération du premier symbole pour vérifier la validité initiale
    symbol0 = list_elements[0]

    if symbol0 not in not_q0_symbols:
        # Parcours de tous les symboles du programme
        for i, symbol in enumerate(list_elements):
            # Récupère le symbole suivant pour traiter les enchaînements
            next_symbol = get_next_token(i, list_elements)

            # Ignorer les lignes de commentaires
            if symbol.startswith("%"):
                print(f"commentaire : {symbol.replace('%', '').strip()}")
                continue  # Les commentaires n'ont pas d'impact sur la syntaxe

            if next_symbol.startswith("%"):
                print(f"Commentaire ignoré après {symbol}: {next_symbol}")
                continue

            # Traite les symboles d'instruction d'affichage de la bande ('I') ; pause et affichage de la bande ('P')
            if symbol in ["I", "P"]:
                print(f"symbol actuel : {symbol}")
                if next_symbol in ["0", "1", "G", "D", "fin", "P", "#"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    print(f"Commentaire ignoré après {symbol}: {next_symbol}")
                    continue
                elif next_symbol in ["si(1)", "si(0)", "boucle"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                    print(f"DEBUG: K incremented to {K}")
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                    print(f"DEBUG: K decremented to {K}")
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des commentaires (symboles commençant par %)
            elif symbol.startswith("%"):
                print(f"commentaire : {symbol.replace('%', '').strip()}")
                if next_symbol not in [
                    "I",
                    "P",
                    "%",
                    "si(0)",
                    "si(1)",
                    "0",
                    "1",
                    "G",
                    "D",
                    "fin",
                    "}",
                    "boucle",
                    "#",
                ]:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des conditions (si(0), si(1))
            elif symbol in ["si(0)", "si(1)"]:
                print(f"symbole actuel : {symbol}, Condition commence")
                if next_symbol in ["G", "D", "0", "1", "fin", "P", "I"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    continue
                elif next_symbol == "boucle":
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                    print(f"DEBUG: K incremented to {K}")
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des symboles d'écrire 0 et d'écrire 1
            elif symbol in ["0", "1"]:
                print(f"symbol actuel : {symbol}")
                if next_symbol in ["G", "D", "fin", "P", "I"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol in ["boucle", "si(1)", "si(0)"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                    print(f"DEBUG: K incremented to {K}")
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                    print(f"DEBUG: K decremented to {K}")
                elif symbol.startswith("%"):
                    print(f"Commentaire ignoré après {symbol}: {next_symbol}")
                    continue
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des mouvements de tête G (gauche) et D (droite)
            elif symbol in ["G", "D"]:
                print(f"symbol actuel : {symbol}")
                if next_symbol in ["G", "D", "0", "1", "fin", "P", "I"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    print(f"Commentaire ignoré après {symbol}: {next_symbol}")
                    continue
                elif next_symbol in ["boucle", "si(1)", "si(0)"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                    print(f"DEBUG: K incremented to {K}")
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                    print(f"DEBUG: K decremented to {K}")
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement du symbole de la fin de boucles ('fin')
            elif symbol == "fin":
                print(f"symbol actuel : {symbol}")
                if next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                    print(f"DEBUG: K decremented to {K}")
                elif next_symbol in ["P", "I"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    print(f"Commentaire ignoré après {symbol}: {next_symbol}")
                    continue
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des accolades fermantes (})
            elif symbol == "}":
                print(
                    f"symbole actuel {symbol}, Accolade fermant, boucle ou condition terminée"
                )
                if next_symbol in ["G", "D", "0", "1", "I", "P", "#"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    print(f"Commentaire ignoré après {symbol}: {next_symbol}")
                    continue
                elif next_symbol in ["si(1)", "si(0)", "boucle"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                    print(f"DEBUG: K incremented to {K}")
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                    print(f"DEBUG: K decremented to {K}")
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des boucles
            elif symbol == "boucle":
                print(f"symbole actuel {symbol}, Boucle commence")
                if next_symbol in ["G", "D", "0", "1", "P", "I"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol in ["si(1)", "si(0)", "boucle"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                    print(f"DEBUG: K incremented to {K}")
                elif next_symbol.startswith("%"):
                    print(f"Commentaire ignoré après {symbol}: {next_symbol}")
                    continue
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement du symbole Fin du programme ('#')
            elif symbol == "#":
                print(
                    f"symbole actuel : {symbol}, Programme Terminé, Vérification de la fermeture des conditions et des boucles..."
                )
                if next_symbol:
                    print("Erreur de Syntaxe : symbole après la fin du programme")
                    return False
    else:
        print(f"Syntaxe invalide, l'état 0 ne prend pas {symbol}")

    if K < 0:
        print(f"Erreur : Trop de fermetures rencontrées à symbol = {symbol}")
        return False

    # Vérifie si toutes les boucles/conditions sont bien fermées
    if K != 0:
        print("Erreur : Boucle ou Condition non fermée")
        print(f"Erreur : Il reste {K} boucle(s) ou condition(s) non fermée(s).")
        return False
    else:
        print("Les boucles et les conditions sont bien fermées : Syntaxe Valide")

    return True


def clean_condition(condition):
    return condition.replace(" ", "")


def ajouter_instruction(
    current_block, type_, instruction, numero_noeud, suivant=None, contenu=None
):
    entry = {"type": type_, "instruction": instruction, "numero_noeud": numero_noeud}
    if suivant:
        entry["suivant"] = suivant
    if contenu is not None:
        entry["contenu"] = contenu
    current_block.append(entry)


def json_file(list_elements: list, output_file: str) -> None:
    """
    Transforme la structure syntaxique d'un programme en JSON avec numérotation des nœuds.

    Parameters:
    - list_elements : Liste de symboles représentant un programme de machine de Turing.
    - output_file : Chemin du fichier de sortie JSON.

    Returns:
    - None
    """
    # Structure principale pour le JSON
    structure_syntaxique = []
    context_stack = [structure_syntaxique]  # Pile des contextes
    current_block = context_stack[-1]  # Bloc courant
    numero_noeud = 0  # Compteur de nœuds

    for i, symbol in enumerate(list_elements):
        # Standardiser les conditions et récupérer le symbole suivant
        next_symbol = get_next_token(i, list_elements)

        if symbol in ["I", "P", "0", "1", "G", "D", "fin", "#"]:
            # Ajouter une instruction simple
            ajouter_instruction(
                current_block,
                "instruction",
                symbol,
                suivant=next_symbol,
                numero_noeud=numero_noeud,
            )
            numero_noeud += 1

        elif symbol in ["si(0)", "si(1)"]:
            # Commencer un nouveau bloc conditionnel
            condition_block = []
            ajouter_instruction(
                current_block,
                "condition",
                symbol,
                suivant=next_symbol,
                contenu=condition_block,
                numero_noeud=numero_noeud,
            )
            numero_noeud += 1
            context_stack.append(condition_block)
            current_block = context_stack[-1]

        elif symbol == "boucle":
            # Commencer un nouveau bloc de boucle
            boucle_block = []
            ajouter_instruction(
                current_block,
                "boucle",
                symbol,
                suivant=next_symbol,
                contenu=boucle_block,
                numero_noeud=numero_noeud,
            )
            numero_noeud += 1
            context_stack.append(boucle_block)
            current_block = context_stack[-1]

        elif symbol == "}":
            # Ajouter une fermeture de bloc
            ajouter_instruction(
                current_block,
                "fermeture",
                symbol,
                suivant=next_symbol,
                numero_noeud=numero_noeud,
            )
            numero_noeud += 1
            if context_stack:  # Vérifie qu'il reste des contextes à sortir
                context_stack.pop()
                if context_stack:
                    current_block = context_stack[-1]

    # Vérifie si tous les contextes ont été correctement fermés
    if len(context_stack) > 1:
        print("Erreur : Certains blocs n'ont pas été fermés correctement.")
        return

    # Écriture dans le fichier JSON
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(structure_syntaxique, json_file, ensure_ascii=False, indent=4)
        print(f"Fichier JSON généré avec succès : {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier JSON : {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", help="Fichier d'entrée")
    args = parser.parse_args()
    input_file = args.input_file_path
    list_elements = input_tokenizer(input_file)
    json_file(list_elements, "structure_syntaxique.json")

    if analyseur_syntaxique(list_elements):
        json_file(list_elements, "structure_syntaxique.json")
    return None


# Main procedure
if __name__ == "__main__":
    main()
