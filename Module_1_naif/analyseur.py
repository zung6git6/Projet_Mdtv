#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Modules to import
from tokenizer import get_next_token, input_tokenizer
import argparse

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
    not_q0_symbols = ['fin', '}']
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

            # Traite les symboles d'instruction d'affichage de la bande ('I') ; pause et affichage de la bande ('P')
            if symbol in ['I', 'P']:
                print(f"symbol actuel : {symbol}")
                if next_symbol in ["0", "1", "G", "D", "fin", "P", "#"]:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    pass
                elif next_symbol in ["si(1)", "si(0)", "boucle"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des commentaires (symboles commençant par %)
            elif symbol.startswith("%"):
                print(f"commentaire : {symbol.replace('%', '').strip()}")
                if next_symbol not in ['I', 'P', '%', 'si(0)', 'si(1)', '0', '1', 'G', 'D', 'fin', '}', 'boucle', '#']:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des conditions (si(0), si(1))
            elif symbol in ['si(0)', 'si(1)']:
                print(f"symbole actuel : {symbol}, Condition commence")
                if next_symbol in ['G', 'D', '0', '1', 'fin', 'P', 'I']:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    pass
                elif next_symbol == "boucle":
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()
            
            # Traitement des symboles d'écrire 0 et d'écrire 1    
            elif symbol in ['0', '1']:
                print(f"symbol actuel : {symbol}")
                if next_symbol in ['G', 'D', 'fin', 'P', 'I']:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol == "boucle":
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                elif symbol.startswith("%"):
                    pass
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des mouvements de tête G (gauche) et D (droite)
            elif symbol in ['G', 'D']:
                print(f"symbol actuel : {symbol}")
                if next_symbol in ['G', 'D', '0', '1', 'fin', 'P', 'I']:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    pass
                elif next_symbol == "boucle":
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
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
                elif next_symbol in ["P", 'I']:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    pass
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des accolades fermantes (})
            elif symbol == "}":
                print(f"symbole actuel {symbol}, Accolade fermant, boucle ou condition terminée")
                if next_symbol in ['G', 'D', '0', '1', 'I', 'P', '#']:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol.startswith("%"):
                    pass
                elif next_symbol in ["si(1)", "si(0)"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                elif next_symbol == "boucle":
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                elif next_symbol == "}":
                    print(f"{symbol} rencontre {next_symbol}")
                    K -= 1
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement des boucles
            elif symbol == "boucle":
                print(f"symbole actuel {symbol}, Boucle commence")
                if next_symbol in ['G', 'D', '0', '1', 'P', 'I']:
                    print(f"{symbol} rencontre {next_symbol}")
                elif next_symbol in ["si(1)", "si(0)"]:
                    print(f"{symbol} rencontre {next_symbol}")
                    K += 1
                elif next_symbol.startswith("%"):
                    pass
                else:
                    print(f"Erreur de syntaxe : {symbol} suivi de {next_symbol}")
                    return False
                print()

            # Traitement du symbole Fin du programme ('#')
            elif symbol == "#":
                print(f"symbole actuel : {symbol}, Programme Terminé, Vérification de la fermeture des conditions et des boucles...")
                if next_symbol:
                    print("Erreur de Syntaxe : symbole après la fin du programme")
                    return False                
    else:
        print(f"Syntaxe invalide, l'état 0 ne prend pas {symbol}")

    # Vérifie si toutes les boucles/conditions sont bien fermées
    if K != 0:
        print("Erreur : Boucle ou Condition non fermée")
        return False
    else:
        print("Les boucles et les conditions sont bien fermées : Syntaxe Valide")

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path', help='Fichier d\'entrée')
    args = parser.parse_args()
    input_file = args.input_file_path
    list_elements = input_tokenizer(input_file)
    analyseur_syntaxique(list_elements)
    return None

# Main procedure
if __name__ == "__main__":
    main()