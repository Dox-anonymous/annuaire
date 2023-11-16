import getpass
import os

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpass"

def inscription():
    print("Bienvenue! Veuillez vous inscrire.")

    nom_utilisateur = input("Nom d'utilisateur : ")
    mot_de_passe = getpass.getpass("Mot de passe : ")

    with open("utilisateurs.txt", "a") as fichier:
        fichier.write(f"{nom_utilisateur},{mot_de_passe}\n")

    print("Inscription réussie!")

def connexion():
    print("Bienvenue! Veuillez vous connecter.")

    while True:
        nom_utilisateur = input("Nom d'utilisateur : ")
        mot_de_passe = getpass.getpass("Mot de passe : ")

        if nom_utilisateur == ADMIN_USERNAME and mot_de_passe == ADMIN_PASSWORD:
            print("Connexion en tant qu'administrateur réussie!")
            return nom_utilisateur

        with open("q.txt", "r") as fichier:
            lignes = fichier.readlines()

        utilisateur_trouve = False

        for ligne in lignes:
            nom, mot_de_passe_stocke = ligne.strip().split(',')
            if nom == nom_utilisateur and mot_de_passe == mot_de_passe_stocke:
                utilisateur_trouve = True
                break

        if utilisateur_trouve:
            print("Connexion réussie!")
            return nom_utilisateur
        else:
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")

def deconnexion(nom_utilisateur):
    if nom_utilisateur:
        print("Déconnexion réussie!")
        return None
    else:
        print("Vous n'êtes pas connecté.")
        return nom_utilisateur

def renseigner_infos(nom_utilisateur):
    if nom_utilisateur:
        print(f"Bienvenue, {nom_utilisateur}! Renseignez vos informations.")

        num_telephone = input("Entrez votre numéro de téléphone : ")

        with open("informations_utilisateurs.txt", "a") as fichier:
            fichier.write(f"{nom_utilisateur},{num_telephone}\n")

        print("Informations enregistrées avec succès!")
    else:
        print("Vous devez être connecté pour renseigner des informations.")

def consulter_infos(nom_utilisateur):
    if nom_utilisateur:
        print(f"Consultation des informations pour {nom_utilisateur}.")

        with open("informations_utilisateurs.txt", "r") as fichier:
            lignes = fichier.readlines()

        infos_utilisateur = [ligne.split(',')[1] for ligne in lignes if ligne.startswith(f"{nom_utilisateur},")]

        if infos_utilisateur:
            print(f"Votre numéro de téléphone enregistré : {', '.join(infos_utilisateur)}")
        else:
            print("Aucune information trouvée.")
    else:
        print("Vous devez être connecté pour consulter des informations.")

def consulter_infos_admin():
    print("Consultation de toutes les informations enregistrées.")

    with open("informations_utilisateurs.txt", "r") as fichier:
        lignes = fichier.readlines()

    for ligne in lignes:
        nom_utilisateur, num_telephone = ligne.strip().split(',')
        print(f"Utilisateur: {nom_utilisateur}, Numéro de téléphone: {num_telephone}")

def supprimer_numero(nom_utilisateur):
    if nom_utilisateur:
        print(f"Supprimer un numéro pour {nom_utilisateur}.")

        num_telephone_a_supprimer = input("Entrez le numéro de téléphone à supprimer : ")

        with open("informations_utilisateurs.txt", "r") as fichier:
            lignes = fichier.readlines()

        nouvelles_informations = []

        for ligne in lignes:
            if not (ligne.startswith(f"{nom_utilisateur},{num_telephone_a_supprimer}") or
                    ligne.startswith(f"{nom_utilisateur}, {num_telephone_a_supprimer}")):
                nouvelles_informations.append(ligne)

        with open("informations_utilisateurs.txt", "w") as fichier:
            fichier.writelines(nouvelles_informations)

        print("Numéro supprimé avec succès!")
    else:
        print("Vous devez être connecté pour supprimer un numéro.")

def supprimer_compte(nom_utilisateur):
    if nom_utilisateur:
        print(f"Supprimer le compte pour {nom_utilisateur}.")

        confirmation = input("Êtes-vous sûr de vouloir supprimer votre compte? (o/n) : ").lower()

        if confirmation == 'o':
            with open("utilisateurs.txt", "r") as fichier:
                lignes = fichier.readlines()

            nouveaux_utilisateurs = []

            for ligne in lignes:
                nom, _ = ligne.strip().split(',')
                if nom != nom_utilisateur:
                    nouveaux_utilisateurs.append(ligne)

            with open("utilisateurs.txt", "w") as fichier:
                fichier.writelines(nouveaux_utilisateurs)

            # Supprimer également les informations associées
            with open("informations_utilisateurs.txt", "r") as fichier_infos:
                lignes_infos = fichier_infos.readlines()

            nouvelles_informations = []

            for ligne in lignes_infos:
                if not ligne.startswith(f"{nom_utilisateur},"):
                    nouvelles_informations.append(ligne)

            with open("informations_utilisateurs.txt", "w") as fichier_infos:
                fichier_infos.writelines(nouvelles_informations)

            print("Compte supprimé avec succès!")
            return True
        else:
            print("Suppression de compte annulée.")
            return False
    else:
        print("Vous devez être connecté pour supprimer votre compte.")

def confirmer_sortie():
    confirmation = input("Voulez-vous vraiment quitter? (o/n) : ").lower()
    return confirmation == 'o'

def main():
    nom_utilisateur = None

    while True:
        choix = input("Choisissez une option (inscription/i, connexion/c, deconnexion/dc, renseigner/r, consulter/q, supprimer numéro/s, supprimer compte/d, consulter admin/a, quitter/x) : ").lower()

        if choix == 'inscription' or choix == 'i':
            inscription()
        elif choix == 'connexion' or choix == 'c':
            nom_utilisateur = connexion()
        elif choix == 'deconnexion' or choix == 'dc':
            nom_utilisateur = deconnexion(nom_utilisateur)
        elif choix == 'renseigner' or choix == 'r':
            renseigner_infos(nom_utilisateur)
        elif choix == 'consulter' or choix == 'q':
            consulter_infos(nom_utilisateur)
        elif choix == 'consulter admin' or choix == 'a':
            if nom_utilisateur == ADMIN_USERNAME:
                consulter_infos_admin()
            else:
                print("Vous n'avez pas les droits d'administrateur.")
        elif choix == 'supprimer numéro' or choix == 's':
            supprimer_numero(nom_utilisateur)
        elif choix == 'supprimer compte' or choix == 'd':
            if supprimer_compte(nom_utilisateur):
                nom_utilisateur = None
        elif choix == 'quitter' or choix == 'x':
            if confirmer_sortie():
                break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
