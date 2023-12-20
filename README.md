# Signature-et-certificats

<div id="gif" style="display: flex;">
  <img src="https://media.giphy.com/media/rMS1sUPhv95f2/giphy.gif">
  <img src="https://media.giphy.com/media/FDZdBGmyXX7wpHduym/giphy-downsized-large.gif" style="width:265px;">
</div>
Ce dépôt est la trace de nos recherches sur les signatures et certificats en cryptographie.

## Sujet

"Après vous être remis à jour en cryptogtaphie, vous présenterez comment signer numériquement un document et comment vérifier que la signature numérique est bien celle de l’entité cible.

Pour un site web il s’agit d’un certificat SSL et le standard le plus utilisé pour la création des certificats numériques est le X.509. Vous aborderez les architectures PKI avec les préconisations du Référentiel Général de Sécurité (RGS)."

## Sommaire

- [Signatures](#signatures)
  - [Générer votre paire de clés RSA](#générer-votre-paire-de-clés-rsa)
  - [Signer numériquement un fichier](#signer-numériquement-un-fichier)
  - [Vérifier que la signature est celle de l'entité cible](#vérifier-que-la-signature-est-celle-de-lentité-cible)

- [Certificats](#certificats)
  - [Généreration d'un certificat autosigné](#génération-dun-certificat-autosigné)
  - [Faire certifier sa clé publique](#faire-certifier-sa-clé-publique)
  
- [Sources](#sources)

## Signatures

La signature numérique est un mécanisme permettant d'authentifier l'auteur d'un document électronique et d'en garantir
la non-répudiation (ne peut être remis en cause par l'une des parties), par analogie avec la signature manuscrite d'un
document papier.

C'est un mécanisme utilisé principalement par le protocole HTTPS pour la signature des certificats, qui sont utilisés
pour chiffrer les échanges entre navigateurs et site web. C'est aussi utilisé pour signer des fichiers d'installation
afin de vérifier leur authenticité.

Pourquoi opter pour la signature numérique ? 

Elle présente plusieurs avantages à la signature manuscrite : 
- Gain de temps
- Facilité
- Économies (gain du temps passé, gain d'impression, pas d'envoi postal...)
- Fiabilité (robustesse des algos, on est sûr de l'identité de la personne cible)

Pour signer un document et vérifier des signatures, il nous faut utiliser un algo de chiffrement asymétrique (RSA, GPG, DSA, ECDSA, EdDSA). Nous allons ici utiliser RSA (Rivest-Shamir-Adleman).

Nous allons donc dans un permier temps générer une paire de clés RSA (privée & publique) : 

### Générer votre paire de clés RSA

#### Comment ça marche ?

RSA, illustration très simplifiée (un groupe le présente déjà, nous n'allons pas rentrer dans les détails ici) :
Tout d'abord calcul de la paire de clés :

Choix des facteurs `p` = 79 et `q` = 127 (il faut choisir des nombres premiers assez grands, pour l'exemple ils sont très petits)

`n` = `p` * `q` = 79 * 127 = 10033 (`n` = modulo).

(`p` - 1) * (`q` - 1) = 78 * 126 = 9828 (`phi`)

Choix d'un nombre dont le PGCD avec 9828 (`phi`) soit égal à 1 (en somme, un nombre premier avec `phi`) : parmi les valeurs possibles on choisit (par exemple) `a` = 97 (clé privée).

Calcul de la clé publique `b`, tel que b vérifie cette égalite :

(`a` * `b`) % 9828 = 1 (`b` est l'inverse modulaire de `a` par rapport à 9828 (`phi`)), `b` = 2533 dans notre cas.

Nous allons désormais le faire à l'aide d'OpenSSL.

Petit zoom sur OpenSSL : 

"OpenSSL est une boîte à outils de chiffrement comportant deux bibliothèques, libcrypto et libssl, fournissant respectivement une implémentation des algorithmes cryptographiques et du protocole de communication SSL/TLS, ainsi qu'une interface en ligne de commande, openssl.
Développée en C, OpenSSL est disponible sur les principaux systèmes d'exploitation et dispose de nombreux wrappers ce qui la rend utilisable dans une grande variété de langages informatiques. En 2014, deux tiers des sites Web l'utilisaient."
OpenSSL voit le jour en 1998, dans le but de mettre à la disposition de tous les outils libres pour le chiffrement.
OpenSSL supporte un grand nombre de types de chiffrement (AES, Blowfish, Camellia...), de fonctions de hachage cryptographique (MD5, SHA-1...), et de types de cryptographie à clé publique (RSA, DSA, courbe elliptique...).

-------------

Nous allons générer notre paire de clés RSA (privée & publique) avec OpenSSL 
(déjà installé sous les distributions Linux, il faut l'installer sous Windows), 
qui vont nous permettre d'effectuer les différentes actions de signature et de certificats.

```
openssl genrsa -out key 4096
```

Ici, on utilise la commande genrsa pour générer une paire de clés RSA.
On spécifie le nom du fichier de sortie dans la paire de clés générée
sera enregistrée.
On spécifie enfin la longueur de la clé RSA en bits, plus la clé est longue plus elle est sécurisée.

En regardant les détails de notre clé privée (openssl rsa -text -in `key`), on trouve ces valeurs : 

`p` (prime1) = 28801848262248049197762633695084565880881233586722034388395275688832434177661677266999925272974178258205011741647898468962326982072652597906022921015943611739007075659157122343510043485770825501079475657875554060522048241398249168825541398970171625917779876200980011561625469723364430589314730540176108455964011383829066803158680944133637867675390766727415130877794378213700515190554113046365211078218257737887705898899773793821168448769958842554019183910178836009446478195439556968970064694317822567132066871889116110557940210750606949464175004967412850865586739080994336557019361582284697467688337957289807759358019

`q` (prime2) = 27169970559125643370877856079755629964904825848552574102394707059866977332153991230937679590591201854798799238018530463186920897922528806245476160205117215167690183239494877099772975846290908425373554822139374459943537770456697335704000271298954327049589341123652974657831205620282820427373842691493337442152355335095336434139146207840227079784812472449239559675183248871887687647691663227673839619346675809931901030724525725009324242045460346703839936924252533162122516560693746526774651501021233033504199581066792621253385206371315972233927312769309427295522960627354403280933536628621685931054854185588648260713661

`n` (modulus) = 782545369333683569161575692448095307542108608775527483716579237517628890688447932325390090872207747891855547467914133160764737008239688654894079067665329108007274872388501437557599229865761038085689060222475367954372147181954735569401397154354372774333502277397471295720784315303580577715910704127895541297963142860880785391929552904661418135532700673207134822987037263930569822818996636293809232263040653204414906901849407896584032228975279736913455834916076120448092018407379877686395268252280683296728261705158959323374743021293159371315310506106050794334268669822910015438719200794955196464000512392828991572242457529093068625590500343075158639254744810118048327659209304736107014237400401712964602265725727562263925448217753717047941664300494004494690233438187022757032336119349019667738235764461124162274134868037993613214060256276838698911178206050108507898150373016628578079040444835201668107517081737084148245847614699050291858142994592825815620338602598350679992202060846039486797729571032436388046518185293620308486123692191450699263757937294070143028441174698612977795514179833822407387558147094092446477831590877399864794508233814941091568567915609652954515968930271622304065329083515169058115475863677513096748143197559

`phi` = 782545369333683569161575692448095307542108608775527483716579237517628890688447932325390090872207747891855547467914133160764737008239688654894079067665329108007274872388501437557599229865761038085689060222475367954372147181954735569401397154354372774333502277397471295720784315303580577715910704127895541297963142860880785391929552904661418135532700673207134822987037263930569822818996636293809232263040653204414906901849407896584032228975279736913455834916076120448092018407379877686395268252280683296728261705158959323374743021293159371315310506106050794334268669822910015438719200794955196464000512392828991572242401557274247251897931702585383799058899024058613053050718514753358314825890586044466664660862162182150921637238087288115792416420498823090538734356965961930125638860450367668294952745129062428347681837557978684693594670264983752406648664379839381945183003799303945092820988159858020856500393163852478799949498332331367454905696765673841755391142395111503337511507868412401209526732786660114007467487728686760666516762567151180433265246478650953770582053864181608623945185077689103891813430898753390877195324424443956062696908397819168646869813291916232237807820571913955325491130616958151732077120485370218292123125880

`a` (privateExponent) = 304936808856731479763314158929146252712366596745493704001617415623620345917597438023190139016043478732047652032219832043877654664028337715621480861651237846716965770344348226381219297989102421389937397500062193063746523257591284876808106573811770021681324765554978438898902754844177194465857875124253419193240196261366457075226161131562984212662070430327354152760165366834900775671018449084811635771145035652140743281801580463905320888407627659509831623542224269710291498940868018315686747343130507805237443694803691093585977192697021591233202613866004321005059024519545843939667835724881605921809742366725159631535261775327978490302720292668653302109742027807328076488231829802573578955759247240544878192610249138773063105906377667026276862391423149428356168240966121973412706794912514907806529185118421598412241920862347370946259680626625495048003320123477396525872156965174239739085743864175261861746906947502397174010258150526854480116295893949655473231594282410814840980955611998045410819746126702870005076593399380540670178755244211771150719866099635138279035117438751696309539834544059452449595364424559624276695823659176491904254904049063978041469113506095133113952974987648787571942452258966343881071539786004617769263780593

`b` (publicExponent) = 65537

L'exposant public est 65537, car c'est le plus utilisé. En effet, la factorisation serait trop simple avec un petit exposant, et un trop grand exposant demande trop de
performances pour une sécurité équivalente ([source](https://fr.wikipedia.org/wiki/65_537#Applications)).
65537 est le plus grand nombre premier de Fermat que l'on connaisse aujourd'hui (avec 3, 5, 17 et 257) (écriture -> 2^2^n + 1). ([source](https://www.techno-science.net/glossaire-definition/Nombre-de-Fermat-page-2.html))

Ensuite, on chiffre notre paire de clé, et on renseigne un mot de passe. 

Pourquoi chiffrer notre paire de clés ?

Pour des raisons de sécurité. Si une personne malveillante (Rémy ou Cédric par exemple) accédait à notre PC, il ne pourrait pas directement accèder à notre clé privée, car elle est protégée par un mot de passe.

```
openssl rsa -in key -des3 -out key_enc
```

Plus de précision : "-des3" sous entend DES-EDE3-CBC, qui sont les algorithmes utilisés pour réaliser le chiffrement,
ce sont les acronymes de :
- DES : Data Encryption Standard, l'algorithme symétrique qui chiffre
- EDE3 : Encryption Decryption Encryption with 3 keys, une méthode qui utiliser 3 clés de chiffrement
- CBC : Cipher Block Chaining, lecture bloc par bloc

Fonctionnement imagé de des3 :

![des3](resources/des3.webp)

Nous allons maintenant voir comment OpenSSL génère un hash du mot de passe : 

- Choix d'un sel (Salt) : OpenSSL génère un sel aléatoire pour renforcer la sécurité du processus. Le sel est utilisé pour rendre le processus de chiffrement aléatoire, ce qui signifie que si on chiffre la même clé privée avec le même mot de passe plusieurs fois, on obtiendra des résultats différents en raison du sel.


- Chiffrement de la clé privée : OpenSSL utilise le mot de passe (et éventuellement le sel) pour dériver une clé à partir du mot de passe en utilisant un algorithme de dérivation de clé. Ensuite, cette clé dérivée est utilisée pour chiffrer la clé privée RSA à l'aide de DES3.


- La clé dérivée elle-même n'est pas directement le hash du mot de passe, mais plutôt une clé symétrique qui est utilisée pour chiffrer et déchiffrer la clé privée.

Si nous renseignons un mot de passe plus court que la taille de la clé, OpenSSL pourrait ajouter du padding au mdp pour atteindre la taille attendue (mais processus de dérivation de clé moins sûr), ou alors utiliser une fonction de hachage
pour traiter le mot de passe avant de le passer à l'algorithme de dérivation de clé. Cela pourrait impliquer l'application d'une fonction de hachage comme SHA-256 ou SHA-512 pour générer une entrée de la taille appropriée pour l'algorithme de dérivation de clé.

Le choix de l'algorithme de dérivation de clé et la gestion du sel sont importants pour la sécurité de cette opération. OpenSSL utilise généralement une forme de dérivation de clé sécurisée, telle que PBKDF2, pour rendre le processus résistant aux attaques par force brute. 

PBKDF2, c'est quoi ?

PBKFD2 (Password-Based Key Derivation Function 2), est une fonction de dérivation de clé, appartenant à la famille des normes Public Key Cryptographic Standards, plus précisément PKCS #5 v2.0. Elle succède au PBKDF1, qui pouvait produire des clés n'allant que jusqu'à 160 bits (PBKDF2 permet de ne pas avoir de limite de taille).
Cette norme est aujourd'hui utilisée pour le hachage de mot de passe (associé à des fonctions comme SHA-256) ou la génération de clé de chiffrement de données.

------------------------

On exporte ensuite la partie publique de la clé, en renseignant notre mot de passe : 

```
openssl rsa -in key_enc -pubout -out key.pub
```

On se retrouve avec deux fichiers, l'un contenant la clé privée (key_enc) et l'autre la clé publique (key.pub).

[Clé publique](resources/key.pub)

On peut voir que la clé publique (et également la clé privée et les certificats) est encodée d'une certaine manière. 

Le format PEM de la clé encode les données binaires en base 64. PEM définit également un en-tête d’une ligne, composé de ----BEGIN, le label du fichier en question et -----, et un pied de page d’une ligne, composé de ----END,  le label du fichier en question et -----.
Le label du fichier détermine le type de message codé. Les types courants comprennent : CERTIFICATE, CERTIFICATE REQUEST, PRIVATE KEY, PUBLIC KEY et X509 CRL.

### Signer numériquement un fichier

Pour garantir l'authenticité d'un fichier, par exemple lorsqu'on échange un document avec un tiers, on peut créer une
signature numérique de ce fichier et en combinaison de notre clé publique, le destinataire pourra vérifier que c'est bien
nous qui avons signé le fichier, ou à l'inverse, que c'est un intrus.

Par exemple, lorsqu'on veut télécharger Linux Mint, on a en plus de l'ISO, deux autres fichiers, une somme de contrôle
SHA256 et une signature GPG, l'un permet de vérifier l'intégrité et l'autre l'authenticité avec leur clé publique.

Nous allons donc voir comment signer un fichier, on commence pas calculer son empreinte. 
La commande dgst permet de le faire (dgst = digest, une représentation numérique d’un message calculé par un algorithme de hachage cryptographique ou une fonction).

```
openssl dgst -sha256 -out hash file
```

Ici, nous avons récupéré le hash du fichier `file` dans le fichier de sortie nommé `hash`.

[Fichier originel](resources/file)

[Le hash de ce fichier](resources/hash)

Nous allons maintenant signer le fichier.

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


- -inkey key_enc : Spécifie le fichier contenant la clé privée utilisée pour signer les données


- -out signature : Spécifie le fichier de sortie

[Signature du fichier](resources/signature)

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

Dans la réalité, il y a par exemple le projet [Linux Mint](https://www.linuxmint.com/) qui fournit des signatures de
leurs fichiers d'installation, voici le [checksum](https://ftp.heanet.ie/mirrors/linuxmint.com/stable/21.2/sha256sum.txt)
et la signature [GPG](https://ftp.heanet.ie/mirrors/linuxmint.com/stable/21.2/sha256sum.txt.gpg) de la version 21.2
(GPG est un autre algorithme utilisé pour la signature de fichiers).

Pour vérifier la signature, il faut récupérer leur clé publique avec :

```
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key "27DE B156 44C6 B3CF 3BD7  D291 300F 846B A25B AE09"
```

Puis se positionner dans le répertoire qui contient le checksum et la signature et utiliser la commande suivante :

```
gpg --verify sha256sum.txt.gpg sha256sum.txt
```

On obtient alors :

```
gpg: Signature made Fri Sep 29 12:41:09 2023 CEST
gpg:                using RSA key 27DEB15644C6B3CF3BD7D291300F846BA25BAE09
gpg: Good signature from "Linux Mint ISO Signing Key <root@linuxmint.com>" [unknown]
```

## Certificats

Un certificat peut être vu comme une carte d'identité numérique.
Il est utilisé principalement pour identifier et authentifier une personne physique ou morale, mais surtout pour chiffrer ses échanges entre navigateurs et sites web.
Il est signé par un tiers de confiance (une autorité de certification) qui atteste du lien entre l’identité physique (vous, un site web...) et l’entité numérique (votre clé publique, celle du site web...). Dans le cas de notre carte d'identité, c'est l'État la CA, qui certifie notre identité.
Pour un site web il s’agit d’un certificat TLS/SSL. Le standard le plus utilisé pour la création des certificats numériques est le [X.509](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-X.509-200811-S!!PDF-E&type=items).

X.509 représente une norme spécifiant les formats pour les certificats à clé publique. Elle repose sur un système hiérarchique d'autorités de certification, à l'inverse des réseaux de confiance (telle la toile de confiance [OpenPGP](https://fr.wikipedia.org/wiki/OpenPGP)), où n'importe qui peut signer les certificats d'autrui.

### Génération d'un certificat autosigné

Normalement, on ne signe pas soi-même son certificat, car si tout le monde faisait ça il faudrait faire confiance à tout
le monde, ce qui revient à ne faire confiance à personne. 

Donc on crée une requête de certification qui servira à créer un
certificat par une  "autorité de certification" (CA en anglais), auquelle tout le monde fait confiance et dont leurs
cetificats d'autorité son implémentés dans les navigateurs web, donc un certificat signé par une de ces CA sera
vérifiable facilement.

Dans notre cas nous allons donc faire un certificat autosigné, car on ne fait que des exemples et pas de projets sérieux
donc le certificat n'a pas besoin d'être de confiance.

Pour pouvoir générer un certificat autosigné, on utilise :

```
openssl req -new -x509 -key key_enc -out CA.crt -days 1095
```

- req : Cette sous-commande est utilisée pour générer ou traiter des requêtes de certificat X.509.

- -new: Cette option indique que l'on veut créer une nouvelle requête de certificat.

- -x509: Cette option indique que l'on veut générer un certificat auto-signé plutôt qu'une demande de signature de certificat (CSR).

- -key key_enc : Notre clé privée.

- -out ca.crt : Notre fichier de sortie qui sera le certificat.

- -days 1095: Cette option spécifie la durée de validité du certificat en jours. Dans cet exemple, le certificat sera valide pendant 1095 jours (environ 3 ans).

Nous devons remplir plusieurs champs, le code de notre pays, le département ou l'état , la ville, le nom de l'organisation,
la section de l'organisation, notre nom, et notre e-mail.

Nous pouvons visualiser le certificat avec cette commande :

```
openssl x509 -text -in CA.crt
```

Sortie :
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            76:14:26:2e:56:28:08:b0:e5:b9:a0:24:10:e1:e5:29:2c:dc:db:92
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = FR, ST = Haute-Garonne, L = Blagnac, O = R\C3\83\C2\A9steban, CN = GUITOSCANO
        Validity
            Not Before: Nov 17 13:31:53 2023 GMT
            Not After : Nov 16 13:31:53 2026 GMT
        Subject: C = FR, ST = Haute-Garonne, L = Blagnac, O = R\C3\83\C2\A9steban, CN = GUITOSCANO
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
...
```

Nous avons accès à plusieurs informations, celles renseignées auparavant, et notre clé publique, la période de validité du certificat, l'algorithme de signature utilisé, notre signature en hexa...

On peut voir la période de validité de notre certificat avec cette commande : 

```
openssl x509 -noout -in CA.crt -dates
```

Nous avons ici créé un serveur web nginx en local, et nous lui avons attribué notre certificat créé précédemment (CA.crt). Voici les lignes ajoutées dans le fichier nginx.conf, dans la clause http :

```
server {
    listen 443 ssl;
    ssl_certificate /etc/ssl/CA.crt;
    ssl_certificate_key /etc/ssl/key;
}
```
![nginx_certif](resources/nginx.png)

### Faire certifier sa clé publique
Pour 'monter en grade dans les certifications', nous devons faire certifier notre clé publique par un tiers de confiance. Par exemple, les gros sites web comme Apple, Amazon, Fnac... doivent avoir un certificat plus 'solide' qu'un simple certificat autosigné.
Dans cet exemple, nous allons créer une demande de certificat, puis la soumettre à une CA (autorité de certification), qui sera dans notre cas le certificat créé dans la partie précédente.

Nous allons dans un premier temps créer une requête de certificat : 

```
openssl req -new -key key_enc -out request
```

Le fichier contient ceci :
```
-----BEGIN CERTIFICATE REQUEST-----
MIICozCCAYsCAQAwSTELMAkGA1UEBhMCRlIxFjAUBgNVBAgMDUhhdXRlLUdhcm9u
bmUxEDAOBgNVBAoMB0NvbXBhbnkxEDAOBgNVBAMMB215IG5hbWUwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQDEEggjW3BII9OO0lXxwnXMRJFT7OCj8qRS
QrfwLrXi72i47ri72mhJv+KUfQArC/p/CIbcSyN5bkDjxYaHmro6dNxZ5u59P3RJ
SEej/yjHkd9I1zPZzElL8qbPHqQF9kGvB51aVyBS1MP9GJ4nGF5yNjjCf8fqX8nY
RsFkS8/TPo/5/qU5U0K6Np3GJ5YjzFhcC4IY6HmV+R5qAVtVej6Z4D4D6Mp9biay
BWT1PdoiU8Dx5unxDouKTnY7GRrX2NXAX6HaI2BOYUfZV9qg30F8pmBjZU30I56X
t2IXTs4VXjUrCK99hPE/qEMxvul2fhJhFrYj3hB/LFF1DLzQms6vAgMBAAGgFTAT
BgkqhkiG9w0BCQcxBgwEcHN3ZDANBgkqhkiG9w0BAQsFAAOCAQEADRNEjkgZ4bOn
4i/8QKYAJ0l0KSXx9VVHSbfx0DuW2opElpDrHw34VMkOJ6IDNKCjHMqQvUZqBGzZ
OJWpDRYnCjXPmmRp0l3qeOQJXFH8GzTRUVYsySVrCf4u2qhHUGyDwgMMBvGFCtpK
JCEEkrc/W5pSymDcVwOf+pE0E4des9fRbEFIMnXe+zqNMiGOTB8E6ifWoPLFFC97
YS4beY8nbHoRgJasrttym2XJN4IJvhQI7O9dRFbEtaJk/SgvitHhj4MA8k37EmUN
95+IQpwNrKtIjwewxwmdqPMg6t5IBpjORyFev1DqxoPxkLM/d7pRE8v7XGcHgZ8z
BEQDXWLb2A==
-----END CERTIFICATE REQUEST-----
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

La CA la plus populaire est Let's Encrypt. Mais dis-donc Jamy, qu'est ce que Let's Encrypt ?

![jamy](resources/jamy.webp)

Let's Encrypt est une autorité de certification à but non lucratif fournissant des certificats gratuits X.509 pour le protocole cryptographique TLS au moyen d'un processus 
automatisé destiné à se passer du processus complexe impliquant la création manuelle, la validation, la signature, 
l'installation et le renouvellement des certificats pour la sécurisation des sites internet.
C'est l'une des autorités de certification les plus connues car ses services sont gratuits et [open source](https://github.com/letsencrypt/boulder),
elle fonctionne sur le modèle des donations.

Quelques autres CA et leurs prix annuel : 

| Nom            | Utilisation | Prix DV | Prix OV     | Prix EV     | Source                                                            |
|----------------|-------------|---------|-------------|-------------|-------------------------------------------------------------------|
| IdenTrust      | 38.5%       | ?       | $242        | $363        | [Lien](https://www.identrust.com/)                                |
| DigiCert Group | 13.1%       | ?       | $268        | $430        | [Lien](https://www.digicert.com/fr)                               |
| Sectigo        | 12.1%       | $99     | $179        | $249        | [Lien](https://www.sectigo.com/ssl-certificates-tls)              |
| GlobalSign     | 16.1%       | $249    | $349        | $599        | [Lien](https://shop.globalsign.com/en/ssl)                        |
| Let's Encrypt  | 5.8%        | Gratuit | Pas proposé | Pas proposé | [Lien](https://letsencrypt.org/fr/)                               |  
| GoDaddy Group  | 4.8%        | $99.99  | $169.99     | $249.99     | [Lien](https://www.godaddy.com/fr-ca/securite-web/certificat-ssl) | 

Mais à quoi correspond DV, OV et EV ?

Il existe trois types de certifications : les certificats à validation de domaine (DV), 
les certificats à validation d'organisation (OV) et les certificats à validation étendue (EV). 
Les niveaux de chiffrement sont les mêmes pour chaque type de certificat. 
Ce qui diffère, ce sont les processus d'audit et de vérification nécessaires pour obtenir le certificat. Plus il y a de vérifications, plus le certificat sera cher et crédible pour l'entreprise.

- DV : l'AC vérifie que l'organisation en question possède le droit exclusif d'utilisation du nom de domaine pour lequel elle souhaite recevoir le certificat. L'identité de l’entreprise ne fait l’objet d’aucune vérification particulière.

- OV : l'AC vérifie que l'organisation en question possède le droit exclusif d'utilisation du nom de domaine pour lequel elle souhaite recevoir le certificat et soumet celle-ci à certaines vérifications.

- EV : l'AC vérifie que l'organisation en question possède le droit exclusif d'utilisation du nom de domaine et soumet celle-ci à un audit très approfondi.


Pourquoi utiliser des CA payantes ?

Un des avantages de payer pour une CA, c'est le support technique qui nous sera fourni, ensuite cela peut renforcer
notre crédibilité en montrant aux consommateurs avertis qu’une transaction potentielle est effectuée avec un
destinataire légitime et que notre site web prend au sérieux la protection de leur données. Une autre raison peut être
la durée de validité du certificat, car un certificat DV est limité à 90 jours, là où les deux autres vont au delà, et
puisqu'il n'existe pas de CA qui fournit gratuitement des certificats OV ou EV cela est un avantage aux CA payantes.

## Sources

TP de Rémi Boulle : [TP9-TP10-signature-certificat-openSSL-prof.html](resources/TP9-TP10-signature-certificat-openSSL-prof.html)

https://lig-membres.imag.fr/prost/M1_MEEF_NSI/openssl.html

http://www.iut-fbleau.fr/sitebp/asr/asr42/openssl/

Documentation de OpenSSL : https://www.openssl.org/docs/man3.0/man1/openssl-dgst.html

http://www.dg77.net/tekno/securite/pubkey.html

Autorités de certification : https://en.wikipedia.org/wiki/Certificate_authority


