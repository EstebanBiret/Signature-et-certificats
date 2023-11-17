# Signature-et-certificats

Ce dépôt est la trace de nos recherches sur les signatures et certificats en cryptographie.

## Sujet

"Après vous être remis à jour en cryptogtaphie, vous présenterez comment signer numériquement un document et comment vérifier que la signature numérique est bien celle de l’entité cible.

Pour un site web il s’agit d’un certificat SSL et le standard le plus utilisé pour la création des certificats numériques est le X.509. Vous aborderez les architectures PKI avec les préconisations du Référentiel Général de Sécurité (RGS)."

## Sommaire

- [Signatures](#signatures)
  - [Signer numériquement un document](#signer-numériquement-un-document)
  - [Vérifier que la signature est celle de l'entité cible](#vérifier-que-la-signature-est-celle-de-lentité-cible)

- [Certificats](#certificats)
  - [Généreration d'un certificat](#génération-dun-certificat)
  - [Faire certifier sa clé publique](#faire-certifier-sa-clé-publique)
  
- [Sources](#sources)

## Signatures

Petit rappel : La signature numérique est un mécanisme permettant d'authentifier l'auteur d'un document électronique et d'en garantir la non-répudiation (ne peut être remis en cause par l'une des parties), par analogie avec la signature manuscrite d'un document papier

Pourquoi opter pour la signature numérique ? 

Elle présente plusieurs avantages à la signature manuscrite : 
- Gain de temps
- Facilité
- Économies (gain du temps passé, gain d'impression, pas d'envoi postal...)
- Fiabilité (robustesse des algos, on est sûr de l'identité de la personne cible)

### Générer votre paire de clés RSA

Avant de commencer, nous allons générer notre paire de clés RSA (privée & publique) avec OpenSSL 
(déjà installé sous les distributions Linux, il faut l'installer sous Windows), 
qui vont nous permettre d'effectuer les différentes actions de signature et de certificats.

```
openssl genrsa -out key 4096
```

Ici, on utilise la commande genrsa pour générer une paire de clés RSA.
On spécifie le nom du fichier de sortie dans la paire de clés générée
sera enregistrée.
On spécifie enfin la longueur de la clé RSA en bits, plus la clé est longue plus elle est sécurisée.

Ensuite, on chiffre notre paire de clé, et on renseigne un mot de passe : 

```
openssl rsa -in key -des3 -out key_enc
```

On exporte ensuite la partie publique de la clé, en renseignant notre mot de passe : 

```
openssl rsa -in key_enc -pubout -out key.pub
```

On se retrouve avec deux fichiers, l'un contenant la clé privée (key_enc) et l'autre la clé publique (key.pub).

### Signer numériquement un document

Pour signer un "document", on calcule d’abord une empreinte de ce document. 
La commande dgst permet de le faire 
(dgst = digest, une représentation numérique d’un message calculé par un algorithme de hachage cryptographique ou une fonction).
```
openssl dgst -<algo> -out hash file
```

Signer un document c’est signer son empreinte. 
Cela revient à chiffrer cette empreinte avec notre clé privée. 
On utilise l’option -sign de la commande rsautl.
```
openssl pkeyutl -sign -in hash -inkey cle -out signature
```
Ici, on utilise la commande pkeyutl d'OpenSSL, 
qui permet d'effectuer diverses opérations sur une clé privée, 
y compris la signature numérique comme ici.
Ensuite, plusieurs options sont définies : 

- -sign :  Cette option indique à OpenSSL d'effectuer une opération de signature. 
           Dans ce contexte, cela signifie qu'elle va utiliser la clé privée spécifiée pour signer les données d'entrée.


- -in hash : Spécifie le fichier d'entrée contenant la valeur du hash des données que nous souhaitons signer. 
             La signature numérique est générée à partir de ce hachage.

- -inkey cle : Spécifie le fichier contenant la clé privée utilisée pour signer les données (clé.

Et pour vérifier : 

```
openssl pkeyutl -verifyrecover -in signature -pubin -inkey cle -out hash
```

Essayons de comprendre les options de ces commandes !!!!!! ;)

cle publique de la personne ayant signée


### Vérifier que la signature est celle de l'entité cible

## Certificats

### Génération d'un certificat

### Faire certifier sa clé publique

## Sources