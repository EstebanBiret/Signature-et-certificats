# Signature-et-certificats

Ce dépôt est la trace de nos recherches sur les signatures et certificats en cryptographie.

## Sujet

"Après vous être remis à jour en cryptogtaphie, vous présenterez comment signer numériquement un document et comment vérifier que la signature numérique est bien celle de l’entité cible.

Pour un site web il s’agit d’un certificat SSL et le standard le plus utilisé pour la création des certificats numériques est le X.509. Vous aborderez les architectures PKI avec les préconisations du Référentiel Général de Sécurité (RGS)."

## Sommaire

- [Signatures](#signatures)
  - [Signer numériquement un fichier](#signer-numériquement-un-fichier)
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
(des3 est un algorithme de chiffrement symétrique par bloc)

On exporte ensuite la partie publique de la clé, en renseignant notre mot de passe : 

```
openssl rsa -in key_enc -pubout -out key.pub
```

On se retrouve avec deux fichiers, l'un contenant la clé privée (key_enc) et l'autre la clé publique (key.pub).

### Signer numériquement un fichier

Pour signer un fichier, on calcule d’abord son empreinte. 
La commande dgst permet de le faire 
(dgst = digest, une représentation numérique d’un message calculé par un algorithme de hachage cryptographique ou une fonction).

```
openssl dgst -sha256 -out hash file
```

Ici, nous avons récupéré le hash du fichier `file` dans le fichier de sortie nommé `hash`.
Nous allons maintenant signer le fichier, c'est-à-dire chiffrer son hash.

```
openssl pkeyutl -sign -in hash -inkey key_enc -out signature
```

Ici, on utilise la commande pkeyutl d'OpenSSL, 
qui permet d'effectuer diverses opérations sur une clé privée ou publique, 
y compris la signature numérique comme ici.
Ensuite, plusieurs options sont définies : 

- -sign :  Cette option indique à OpenSSL d'effectuer une opération de signature. 
           Dans ce contexte, cela signifie qu'elle va utiliser la clé privée spécifiée pour signer les données d'entrée.


- -in hash : Spécifie le fichier d'entrée contenant la valeur du hash des données que nous souhaitons signer. 
             La signature numérique est générée à partir de ce hachage.


- -inkey key_enc : Spécifie le fichier contenant la clé privée utilisée pour signer les données (clé.


- -out signature : Spécifie le fichier de sortie


### Vérifier que la signature est celle de l'entité cible

```
openssl pkeyutl -verify -sigfile signature -in hash -pubin -inkey key.pub
```

Si le fichier a été bien signé, on aura d'affiché dans le terminal : `Signature Verified Successfully`, 
sinon `Signature Verification Failure`.

Voici les options de cette commande : 

- -verify : Cette option indique à OpenSSL d'effectuer une opération de vérification de signature.


- -sigfile signature : Le fichier contenant le hash de la signature.


- -in hash : Le hash de la signature calculé auparavant.


- -pubin -inkey key.pub : On précise la clé à utiliser, ici la clé publique de la personne ayant signé le fichier.
-pubin permet de dire à OpenSSL que nous allons renseigner une clé publique, si nous mettons simplement -inkey key.pub, il va vouloir une clé privée.

## Certificats

Un certificat peut être vu comme une carte d'identité numérique.
Il est utilisé principalement pour identifier et authentifier une personne physique ou morale, mais aussi pour chiffrer des échanges.
Il est signé par un tiers de confiance (une autorité de certification) qui atteste du lien entre l’identité physique (vous, un site web...) et l’entité numérique (votre clé publique, celle du site web...).
Pour un site web il s’agit d’un certificat SSL. Le standard le plus utilisé pour la création des certificats numériques est le X.509.

### Génération d'un certificat autosigné

Pour pouvoir générer un certificat d’autorité de certification sans passer par une certification externe, on utilise :

```
openssl req -new -x509 -key key_enc -out CA.crt -days 1095
```

- req : Cette sous-commande est utilisée pour générer ou traiter des requêtes de certificat X.509.

- -new: Cette option indique que l'on veut créer une nouvelle requête de certificat.

- -x509: Cette option indique que l'on veut générer un certificat auto-signé plutôt qu'une demande de signature de certificat (CSR).

- -key key_enc : Notre clé privée.

- -out ca.crt : Notre fichier de sortie qui sera le certificat.

- -days 1095: Cette option spécifie la durée de validité du certificat en jours. Dans cet exemple, le certificat sera valide pendant 1095 jours (environ 3 ans).

Nous pouvons visualiser le certificat avec cette commande : 

```
openssl x509 -text -in CA.crt
```
Nous devons remplir plusieurs champs, le code de notre pays, le département ou l'état , la ville, le nom de l'organisation,
la section de l'organisation, notre nom, et notre e-mail.


Nous avons accès à plusieurs informations, celles renseignées auparavant, et notre clé publique, la période de validité du certificat, l'algorithme de signature utilisé, notre signature en hexa...


On peut voir la période de validité de notre certificat avec cette commande : 

```
openssl x509 -noout -in CA.crt -dates
```

### Faire certifier sa clé publique
Pour 'monter en grade dans les certifications', nous devons faire certifier notre clé publique par un tiers de confiance. Par exemple, les gros sites web comme Apple, Amazon, Fnac... doivent avoir un certificat plus 'solide' qu'un simple certificat autosigné.
Dans cet exemple, nous allons créer une demande de certificat, puis la soumettre à une CA (autorité de certification), qui sera dans notre cas le certificat créé dans la partie précédente.

Nous allons dans un premier temps créer une requête de certificat : 

```
openssl req -new -key key_enc -out request
```

Ensuite, nous allons contacter une CA qui nous délivrera un certificat signé, après avoir procédé (normalement) à quelques vérifications nous concernant... 
Nous allons à présent jouer le rôle de la CA qui voit arriver une requête d’un tiers voulant certifier sa clé publique.

```
openssl x509 -days 90 -CA CA.crt -CAkey key_enc -in request -req -out CA.crt
```

- -CA CA.crt : Le certificat de la CA (dans notre cas, c'est le certificat que nous avons généré à la partie précédente).

- -CAkey key_enc : C'est la clé privée de la CA qui a servi à créer le certificat de la CA.

- -in request : C'est la requête de la personne ayant voulu faire certifier sa clé publique

- -req : On indique ici que le fichier en entrée est une demande de certificat (requête).

- -out certificat2.crt : Le certificat créé et signé par la CA.

On peut vérifier avec cette commande que `certificat` a été crée et signé par `CA`, celui de la CA.

```
openssl verify -CAfile CA.crt certificate.crt
```

## Sources

TP de Rémi Boulle : [TP9-TP10-signature-certificat-openSSL-prof.html](resources/TP9-TP10-signature-certificat-openSSL-prof.html)

https://lig-membres.imag.fr/prost/M1_MEEF_NSI/openssl.html

http://www.iut-fbleau.fr/sitebp/asr/asr42/openssl/

https://www.openssl.org/docs/man3.0/man1/openssl-dgst.html


###  expliquer les parties de la clé privée et publique  (pk ca amrche) = calcul)

### comment a partir d'un mdp, des3 fais une hash ? nombre de bits fixes ?
