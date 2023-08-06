#!/usr/bin/env python3

import time
import datetime
import argparse
import codecs

from time import  sleep
from progress.bar import Bar

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

# importations des modules neccessaires pour le certificat
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


"""
DESCRIPTION:

	Comme son nom l'indique, oudirasign est un module de signature électronique, 
	elle permet de signer numériquement les documents électronique. En plus elle permet 
	également de chiffrer/chiffre de message et bien d'autre.
	
"""# importations des modules neccessaires pour le certificat



__author__="Oumar Djimé Ratou"
__copyright__="Copy Right 2019, ITS"


# Generate rsa keys
def generatersakeys(length=2048):
	""" Fonction rsakeys(bits) permet  générer une paire de clé RSA 
	elle prend en paramètre la taille de clé et reourne un tuple (privatekey, publickey).

	=============================================

	Exemple :
		(privatekey, publickey) = generatersakeys(taille) // par defaut taille=2048
	"""
	generate_random_number = Random.new().read
	key=RSA.generate(length, generate_random_number)
	privatekey = key.exportKey()
	publickey=key.publickey().exportKey()
	return privatekey, publickey

# Importation de clé privée
def importPrivateKey(privatekey):
	""" Cette fonction permet de importer la clé privé,
	 elle prend en paramètre use clé privée """
	return RSA.importKey(privatekey)

# Importation de clé public
def importPublicKey(publickey):
	""" Cette fonction permet de exporter la clé public, 
	elle prend en paramètre use clé public """
	return RSA.importKey(publickey)

# Chiffrement un message
def chiffre(message,pubkey):
	""" Cette fonction permet de chiffrer un message,
	 elle prend en paramètre le message et la clé public et retourne le message chiffré.

	 ==========================================
	
	Exemple :
		message_chiffre = chiffre(message_clair, publickey) 
	  """
	#key = RSA.importKey(open(pubkey).read()) # Si la clé est stocker sur un fichier
	cipher = PKCS1_OAEP.new(pubkey)
	ciphertext = cipher.encrypt(message.encode("utf-8"))

	return  ciphertext

# Dehiffrement d'un message
def dechiffre(ciphertext,privbkey):
	""" Cette fonction permet de déchiffrer un message, 
	elle prend en paramètre le message chiffré et la clé privée
	et retourne le message en claire.

	========================================

	Exemple :
		dechiffre = dechiffre(message_chiffre, privatekey)
	 """
	#key = RSA.importKey(open(privbkey).read()) # Si la clé est stocker sur un fichier
	cipher = PKCS1_OAEP.new(privbkey)
	message = cipher.decrypt(ciphertext).decode("utf-8")

	return message

# Fonction de hachage
def hacher(message):
	""" Cette fonction permet de hacher un message,
	 elle prend en paramètre le message en claire .
	 Elle retourne le hache d'un message.

	 =======================================

	 Exemple :
	 	hache = hacher(message_clair)
	 """
	
	return SHA256.new(message.encode("utf-8"))

def hacherdocs(nomdoc):
	""" 
	Cette fonction permet de hacher un fichier(txt,pdf, docx etc),
	elle prend en paramètre le fichier en claire .
	Elle retourne le hache d'un message.

	=======================================

	Exemple :
		hache = hacherdocs(nomdoc)

	"""
	f = open(nomdoc, "rb")
	doc_read = f.read()
	hach = SHA256.new(doc_read)
	# hach = hach.hexdigest()
	return hach

def signerdocs(hach,privatekey):
	""" Cette fonction permet de signer un fichier (txt,pdf,docx,etc), 
	elle prend en paramètre 02 arguments, 
	le haché et la clé privée et retourne la signature.

	=========================================

	Exemple :
		signature = signerdocs(hach,privatekey)
	"""
	sig = PKCS1_v1_5.new(privatekey)
	return sig.sign(hach)


def verifierdocs(hach,publickey, signature):
	""" Cette fonction permet de verifier un fichier (txt,pdf,docx,etc), 
	elle prend en paramètre 03 arguments, 
	le message, la clé public et la signature. Retourne un boolean (True or False)

	=========================================

	Exemple :
		verif = verifierdocs(hach,publickey, signature)
	"""
	sig = PKCS1_v1_5.new(publickey)
	return sig.verify(hach, signature)


# Fonction de Signature
def signer(message,privatekey):
	""" Cette fonction permet de signer un message, 
	elle prend en paramètre 02 arguments, 
	le haché et la clé privée et retourne la signature.

	=========================================

	Exemple :
		signature = signer(message_claire, privatekey)
	"""
	hache = SHA256.new(message.encode("utf-8"))
	hache.hexdigest()
	sig = PKCS1_v1_5.new(privatekey)
	signature = sig.sign(hache)
	hexfy = codecs.getencoder('hex')
	ms = hexfy(signature)[0]

	# return signature
	return ms.decode("utf-8")


# Fonction de Verification
def verifier(message, publickey, signature):
	""" Cette fonction permet de verifier la signature d'un message, 
	elle prend en paramètre 03 arguments, 
	le message, la clé public et la signature. Retourne un boolean (True or False)

	=======================================

	Exemple : 
		verifier = verifier(message, publickey, signature)
	"""
	hache = SHA256.new(message.encode("utf-8"))
	# hache.hexdigest()
	signer = PKCS1_v1_5.new(publickey)

	hexfy = codecs.getdecoder('hex')
	ms = hexfy(signature)[0]

	return signer.verify(hache, ms)

def generate_keys_rsa(taille=2048,mypass=b'password'):
	""" Fonction generate_keys_rsa(taille=2048,mypass=b'password') permet  générer une paire de clé RSA 
	elle prend en paramètre la taille de clé et le mot de passe pour protéger le clef privée
	et reourne un tri-tuple (key, privatekey, publickey).Par défaut le mot de passe est "password"

	=============================================

	Exemple :
		(key, privatekey, publickey) = generatersakeys(taille) // par defaut taille=2048
	"""
	# Generation de nos clés
	key = rsa.generate_private_key(
	        public_exponent=65537,
	        key_size=taille,
	        backend=default_backend()
	)
	private = key.private_bytes(
	        encoding=serialization.Encoding.PEM,
	        format=serialization.PrivateFormat.PKCS8,
	        encryption_algorithm=serialization.BestAvailableEncryption(mypass)
	)
	public_key = key.public_key()
	public = public_key.public_bytes(
	        encoding=serialization.Encoding.PEM,
	        format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	return key, private, public


def generate_certificat_auto_sign():
	""" Cette fonction permet de générer un certificat auto-signé, il ne prend aucun paramètre,
	elle retoune un certificat.
		
	=====================================================

		Exemple :
			certificat = generate_certificat_auto_sign()	
	"""
	contry_name = input("Entrer le nom de votre pays : [Ex. CM, pour Cameroun] : ")
	city_name = input("Entrer le nom de l'État ou de la province : [Ex. Centre] : ")
	locality_name = input("Entrer le nom de votre ville : [Ex. Yaoundé] : ")
	organi_name = input("Entrer le nom de votre organisation : [Ex. ITS] : ")
	common_name = input("Entrer le nom de votre section : [Ex. SECURITÉ] : ")
	nom_domaine = input("Entrer le nom de domaine : [Ex. groupits.cm] : ")

	key,private, public = generate_keys_rsa()

	# Generation de CSR(Certificate Signing Request)
	# Divers détails sur qui nous sommes. Pour un certificat auto-signé, le sujet et l'émetteur sont toujours les mêmes
	subject = issuer = x509.Name([
	    x509.NameAttribute(NameOID.COUNTRY_NAME,  contry_name),
	    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, city_name),
	    x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
	    x509.NameAttribute(NameOID.ORGANIZATION_NAME, organi_name),
	    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
	])

	cert = x509.CertificateBuilder().subject_name(
	        subject
	).issuer_name(
	        issuer
	).public_key(
	        key.public_key()
	).serial_number(
	        x509.random_serial_number()
	).not_valid_before(
	        datetime.datetime.utcnow()
	).not_valid_after(
	        # notre certificate sera valide pour 10 jours
	        datetime.datetime.utcnow() + datetime.timedelta(days=30)
	).add_extension(
	        x509.SubjectAlternativeName([x509.DNSName(nom_domaine)]),
	        critical=False,
	# Signer notre certificat avec notre clé privé
	).sign(key, hashes.SHA256(), default_backend())


	certif = cert.public_bytes(serialization.Encoding.PEM)

	return certif

def savekeys(privakeyname, publickeyname):
	""" Fonction qui permet de sauvegarder les clefs dans les fichiers 
	privatekey.pem respectivement publickey.pem"""

	with open("privatekey.pem", "wb") as f_private:
		f_private.write(privakeyname)
		f_private.close()

	with open("publickey.pem", "wb") as f_public:
		f_public.write(publickeyname)
		f_public.close()

def main():
	""" Fonction principale """
	# create argument parser object 
	parser = argparse.ArgumentParser(description = "Comme son nom l'indique, oudirasign est un module de signature électronique, elle permet de signer numériquement les documents et chiffrer/chiffre de message.") 
  
	parser.add_argument("-t", "--taille", type = int, nargs = 1, 
	                    metavar="taille", default = None, help = "génère une paire da clef RSA de taille t.") 


	# parse the arguments from standard input 
	args = parser.parse_args()


	bar = Bar('génération de paire de clefs...', fill='@', suffix='%(percent)d%%')
	for i in range(100):
		sleep(0.001)
		key, private, public = generate_keys_rsa(args.taille[0])
		savekeys(private, public)
		bar.next()
	print()
	print("\nLes clefs sont générées avec succès et sont stockées dans les fichiers ci-dessous.")
	print("privatekey.pem, publickey.pem")

	print()
	reponse = input('Voulez-vous générer un certificat associé à votre votre paire de clef(Y/n) : ')
	if reponse == 'Y' or reponse =='y' or reponse == '':
		print("génération du certificat en cours...")
		for i in range(100):
			sleep(0.001)
		cert = generate_certificat_auto_sign()
		with open("cert_auto_signe.pem", "wb") as ct:
			ct.write(cert)
			ct.close()
		print("Le certificat est généré avec succès.")
	elif reponse == "N" or reponse=='n':
		 
		print("Bye............:)")

	else:
		print("Bye............:)")


	


if __name__ == "__main__":
	main()


