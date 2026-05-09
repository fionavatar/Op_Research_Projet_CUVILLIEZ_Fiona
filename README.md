# Op_Research_Projet_CUVILLIEZ_Fiona
Ce projet implémente :

1. Ford-Fulkerson (flot maximal + coupe minimale)
2. Min Cost Flow :
   - Bellman-Ford
   - Dijkstra avec renormalisation des coûts
3. Détection de cycles négatifs

---

## Exécution

```
python3 -u main.py
```

## Exemples
Le fichier exemples.py contient comme son nom l'indique plusieurs exemples d'utilisations des algorithmes implémentés

## Utilisation

Lancer un exemple spécifique :

```
python3 -u exemples.py exempleFF
```
```
python3 -u exemples.py exempleMinCostPosD
```
```
python3 -u exemples.py exempleMinCostPosB
```
```
python3 -u exemples.py exempleMinCostNegD
```
```
python3 -u exemples.py exempleMinCostNegB
```
```
python3 -u exemples.py exempleMinCostCycleD
```
```
python3 -u exemples.py exempleMinCostCycleB
```

       
```
python3 -u exemples.py all
```

## Exercices
Le fichier exercices.py contient les cas à tester avec notre programme du fichier DearStudent.

## Utilisation

Lancer un exercice spécifique :
```
python3 -u exercices.py exo1
```
```
python3 -u exercices.py exo2
```
```
python3 -u exercices.py exo3
```
```
python3 -u exercices.py vital
```
Lancer tous les tests :
```
python3 -u exercices.py all
```