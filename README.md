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

