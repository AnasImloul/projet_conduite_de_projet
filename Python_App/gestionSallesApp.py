import mysql.connector    # enables python to access mysql databases using an API
from tkinter import *


# établir la connexion avec la base de données
mydb = mysql.connector.connect(
    host="localhost",        # sinon tu dois ajouter l'adresse IP
    user="root",
    passwd="foriinrange(len(L)):",
    database="gestion_salles"
)

# on doit définir un curseur, c'est l'objet qui agit sur la base de données
my_cursor = mydb.cursor()


# on crée l'interface tkinter
screen = Tk()
screen.geometry("500x600")
screen.title("Réserver une salle CC ")

# ajouter les labels
jour = Label(screen, text="Choisir le jour :")
horaire = Label(screen, text="choisir horaire :")

# les choix pour le jour
# dans python, on cree une seule variable aux radiobuttons, et chaque button donne une valeur à cette variable
jour_choisi = StringVar()
lundi = Radiobutton(screen, text="Lundi", variable=jour_choisi, value="lundi", height=2, width=10)
jour_choisi.set("lundi")      # la valeur par defaut
mardi = Radiobutton(screen, text="Mardi", variable=jour_choisi, value="mardi", height=2, width=10)
mercredi = Radiobutton(screen, text="Mercredi", variable=jour_choisi, value="mercredi", height=2, width=10)
jeudi = Radiobutton(screen, text="Jeudi", variable=jour_choisi, value="jeudi", height=2, width=10)
vendredi = Radiobutton(screen, text="Vendredi", variable=jour_choisi, value="vendredi", height=2, width=10)

# les choix des horaires
vacation1 = IntVar()
firstVacation = Checkbutton(screen, text="09 -> 10:30", variable=vacation1)
vacation2 = IntVar()
secondVacation = Checkbutton(screen, text="11 -> 12:30", variable=vacation2)
vacation3 = IntVar()
thirdVacation = Checkbutton(screen, text="14 -> 15:30", variable=vacation3)
vacation4 = IntVar()
fourthVacation = Checkbutton(screen, text="16 -> 17:30", variable=vacation4)


def colonnes_concernees():
    vacations = []
    # vacation1 is a global variable, you can access it!
    if vacation1.get() == 1:  # vérfier si le professeur a réserver la 1ère vacation
        vacations.append("vacation1")
    if vacation2.get() == 1:
        vacations.append("vacation2")
    if vacation3.get() == 1:
        vacations.append("vacation3")
    if vacation4.get() == 1:
        vacations.append("vacation4")
    columns = [jour_choisi.get() + vacation for vacation in vacations]
    # columns contient les chaînes de caractère "jourvacation#", ce qui correspond au nom de la colonne dans le tableau de données
    return columns


# definir la fonction du boutton reserver
def reserver():
    # cette fonction a pour but de générer la liste des salles dispo pour le créneau spécifé
    columns = colonnes_concernees()  # la liste des colonnes qu'on doit checker
    # on commence à preparer notre requête
    query = "Select id from salles where "
    is_first_column = True
    for column in columns:
        if is_first_column:
            query += column + " = 1"
            is_first_column = False
        else:
            query += " and " + column + " = 1"
    query += " ;"
    # la requête est prête à cette étape, temps pour l'exécuter ! (sous la forme select if from salles where jourvacation# = 1)
    my_cursor.execute(query)
    salles_dispo = my_cursor.fetchall()   # les resultas sont des tuples !!
    # on affiche les résultats sur la même interface,
    # on n'affiche que les salles dispo pour le créneau spécifié
    result = Label(screen, text="les salles disponibles sont les suivantes, vueillez choisr une : ")
    result.grid(row=7, column=0)
    row_index = 8
    for i in range(len(salles_dispo)):
        if salles_dispo[i][0] == 1:
            salle1.grid(row=row_index, column=0)
            row_index += 1
        elif salles_dispo[i][0] == 2:
            salle2.grid(row=row_index, column=0)
            row_index += 1
        elif salles_dispo[i][0] == 3:
            salle3.grid(row=row_index, column=0)
            row_index += 1
        elif salles_dispo[i][0] == 4:
            salle4.grid(row=row_index, column=0)
            row_index += 1
        elif salles_dispo[i][0] == 5:
            salle5.grid(row=row_index, column=0)
            row_index += 1
        elif salles_dispo[i][0] == 6:
            salle6.grid(row=row_index, column=0)
            row_index += 1
        elif salles_dispo[i][0] == 7:
            salle7.grid(row=row_index, column=0)
            row_index += 1

        if i == 0:
            id_salle_reserve.set(salles_dispo[i][0])
    valider.grid(row=row_index, column=1)
    return columns


def submit():
    # après la submit, on change l'état des salles concernées
    columns_toUpdate = colonnes_concernees()
    # on prepare notre requête
    query = "update gestion_salles.salles set "
    is_first = True
    for column in columns_toUpdate:
        if is_first:
            query += column + " = 0"
            is_first = False
        else:
            query += ", " + column + " = 0"
    query += " where id = " + str(id_salle_reserve.get()) + " ;"
    # notre requete est prête. Elle est sous la forme: "update gestion_salles.salles set jourvacation# = 0 where id = #;"
    my_cursor.execute(query)
    mydb.commit()


# le boutton reserver
reserverBtn = Button(screen, text="réserver", command=reserver)

# le choix d'une salle
id_salle_reserve = IntVar()
salle1 = Radiobutton(screen, text="CC 1", variable=id_salle_reserve, value=1)
salle2 = Radiobutton(screen, text="CC 2", variable=id_salle_reserve, value=2)
salle3 = Radiobutton(screen, text="CC 3", variable=id_salle_reserve, value=3)
salle4 = Radiobutton(screen, text="CC 4", variable=id_salle_reserve, value=4)
salle5 = Radiobutton(screen, text="CC 5", variable=id_salle_reserve, value=5)
salle6 = Radiobutton(screen, text="CC 6", variable=id_salle_reserve, value=6)
salle7 = Radiobutton(screen, text="CC 7", variable=id_salle_reserve, value=7)

# boutton submit
valider = Button(screen, text="submit", command=submit)

# positionner les elements dans l'interface
jour.grid(row=0, column=0)
lundi.grid(row=2, column=0)
mardi.grid(row=3, column=0)
mercredi.grid(row=4, column=0)
jeudi.grid(row=5, column=0)
vendredi.grid(row=6, column=0)
horaire.grid(row=0, column=1)
firstVacation.grid(row=2, column=1, padx=180)
secondVacation.grid(row=3, column=1)
thirdVacation.grid(row=4, column=1)
fourthVacation.grid(row=5, column=1)
reserverBtn.grid(row=7, column=1)


# la boucle infinie qui assurera la presence de l'inteface à tout instant
screen.mainloop()


































