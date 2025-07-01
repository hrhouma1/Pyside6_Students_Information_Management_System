------------------------------------
# Récupérer un checkout
------------------------------------

## 1. Cloner le dépôt (si nécessaire)

```bash
git clone https://github.com/utilisateur/nom-du-repo.git
cd nom-du-repo
```

## 2. Se placer sur le commit cible (ex. `a665923`)

```bash
git checkout a665923    # HEAD devient detached sur ce commit
```

## 3. Vérifier que vous êtes bien sur le bon commit

```bash
git log -1              # affiche uniquement le commit courant
# ou
git rev-parse --short HEAD
```

La valeur retournée doit être `a665923`.

## 4. Créer un nouveau projet à partir de ce commit (facultatif)

### 4.1 Copier les fichiers et réinitialiser le dépôt

```bash
mkdir ../projet_depuis_commit
cp -r . ../projet_depuis_commit
cd ../projet_depuis_commit
rm -rf .git             # on supprime l’historique
git init
git add .
git commit -m "Initialisation depuis le commit a665923"
```

### 4.2 Ou bien créer une branche pour continuer le développement

```bash
git checkout -b base_a665923   # tout en restant dans le repo original
```


------------------------------------
# Récupérer une branche spécifique
------------------------------------



Pour **cloner une branche spécifique** d’un dépôt Git, il existe deux méthodes :

* cloner **seulement cette branche** (plus rapide, moins de données),
* ou cloner **tout le dépôt**, puis te positionner sur cette branche.


###  Méthode 1 : Cloner uniquement une branche spécifique (léger)

```bash
git clone --branch nom-de-la-branche --single-branch https://github.com/utilisateur/nom-du-repo.git
```

> Exemple :

```bash
git clone --branch develop --single-branch https://github.com/mon-org/mon-projet.git
```

Cela télécharge uniquement la branche `develop` et rien d’autre.



###  Méthode 2 : Cloner tout le dépôt puis basculer sur une branche

```bash
git clone https://github.com/utilisateur/nom-du-repo.git
cd nom-du-repo
git checkout nom-de-la-branche
```

> Exemple :

```bash
git checkout feature/login
```



###  Vérification (optionnel)

Après le clone, tu peux vérifier la branche active avec :

```bash
git branch
```

La branche choisie apparaîtra avec un `*`.



