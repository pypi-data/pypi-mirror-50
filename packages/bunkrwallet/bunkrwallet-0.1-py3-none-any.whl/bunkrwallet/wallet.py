import os
from bunkrwallet.btc import *
from math import ceil
from random import shuffle
import pickle

from punkr import *


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class BunkrWallet(object):
	"""
	BunkrWallet is a lite bitcoin bunkrwallet working on top of Bunkr secrets
	"""
	def __init__(self, wallet_name, testnet=False, bunkr_address=("127.0.0.1", 7860)):
		"""
		:param wallet_name: bunkrwallet name
		:param testnet: flag to generate mainnet vs testnet bunkrwallet
		:param bunkr_address: (ip, port) tuple containing Bunkr RPC address information
		"""

		self.punkr = Punkr(*bunkr_address)
		new = False
		if not os.path.exists(os.path.join(CURRENT_DIR, wallet_name+".p")):
			print("Creating new bunkrwallet...")
			new_wallet(self.punkr, wallet_name, testnet)
			new = True
		with open(os.path.join(CURRENT_DIR, wallet_name+".p"), 'rb') as f:
			wallet_file = pickle.load(f)
		self.name = wallet_name
		self.header = wallet_file[0]
		self.wallet = wallet_file[1:]
		self.testnet = self.header["NETWORK"] != "BTC"
		if not new:
			self.__update_accounts()

	def send(self, outputs, fee):
		"""
		Send bitcoin to bitcoin addresses
		:param outputs: bitcoin addresses [{"address":address, "value":number_of_satoshis}]
		:param fee: transactions fee in satoshis
		:return: signed transaction hex code
		:raise: RuntimeError
		"""

		total = sum(i['value'] for i in outputs) + fee
		input_accts = self.__choose_inputs(total)
		change_acct = self.fresh_account()
		tx, address_list = unsigned_transaction([i["address"] for i in input_accts], outputs, fee, change_acct["address"], self.testnet)
		acct_list = [self.get_account(address) for address in address_list]
		pubkey_list = [acct["pubkey_hex"] for acct in acct_list]
		sec_name_list = [acct["secret_name"] for acct in acct_list]
		hash_list = [str(base64.b64encode(i), 'utf-8') for i in prepare_signatures(tx, pubkey_list)]
		commands = [
			("sign-ecdsa", {"secret_name": secret_name, "hash_content": _hash}) for secret_name, _hash in zip(sec_name_list, hash_list)
		]
		stdout = list(x.strip().split() for x in self.punkr.batch_commands(*commands))
		sigs = []
		try:
			for r, s in stdout:
				r = int(base64.b64decode(r))
				s = int(base64.b64decode(s))
				if s > N//2:
					s = N - s
				sigs.append((r, s))
		except:
			raise RuntimeError(f"Bunkr Operation SIGN-ECDSA failed with: {stdout}")
		return apply_signatures(tx, pubkey_list, sigs)

	def get_account(self, address):
		"""
		get the accound from a bitcoin address
		:param address: address to be queried
		:return: account
		:raise: ValueError
		"""
		for acct in self.wallet:
			if acct["address"] == address:
				return acct
		raise ValueError("The given address does not exist in the bunkrwallet")

	def fresh_account(self):
		"""
		Randomly selects an unused bunkrwallet account
		:return: account
		:raise: ValueError
		"""
		shuffle(self.wallet)
		for acct in self.wallet:
			if len(get_spent(acct["address"], self.testnet))==0 and len(get_unspent(acct["address"], self.testnet))==0:
				return acct
		raise ValueError("No unused addresses available. Run add_accounts()")

	def __choose_inputs(self, total):
		"""

		:param total:
		:return:
		:raise:
		"""
		out = []
		gross_input = 0
		shuffle(self.wallet)
		for acct in self.wallet:
			utxos = get_unspent(acct["address"], self.testnet)
			if len(utxos) != 0:
				out.append(acct)
				gross_input += sum(i['value'] for i in utxos)
			if gross_input >= total:
				return out
		raise ValueError("Not enough funds in bunkrwallet for this transaction.")

	def add_accounts(self, n=5):
		"""
		adds more addresses to the bunkrwallet
		:param n: number of addresses to be added
		:return: None
		"""
		for i in range(n):
			priv, pub = gen_EC_keypair()
			address = convert_public_to_address(pub, self.testnet)
			name = self.name+"-"+address
			write_private_key_to_bunkr(self.punkr, priv, name)
			self.wallet.append({"address": address, "pubkey_hex":pub, "secret_name":name})
		output = [self.header, *self.wallet]
		with open(os.path.join(CURRENT_DIR, self.name+".p"), 'wb') as f:
			pickle.dump(output, f)

	def show_balance(self):
		"""
		prints and returns the bunkrwallet balance
		:return: None
		"""
		balance = 0
		for acct in self.wallet:
			utxos = get_unspent(acct["address"], self.testnet)
			balance += sum(i['value'] for i in utxos)
		print(f"{self.name} current balance: {str(balance/100000000.0)} BTC")

	def show_accounts(self):
		"""
		prints accounts information
		:return: None
		"""
		for acct in self.wallet:
			utxos = get_unspent(acct["address"], self.testnet)
			balance = sum(i['value'] for i in utxos)
			print(f"Address {acct['address']} BTC: {str(balance/100000000.0)}")

	def show_fresh_address(self):
		"""
		prints the next unused bitcoin address
		:return: None
		"""
		print(self.fresh_account()["address"])

	def delete(self, account):
		"""
		deletes an address from Bunkr
		:param account: account to be deleted
		:return: None
		"""
		stdout = self.punkr.delete(account["secret_name"])
		if stdout != 'Secret deleted\n':
			print(f"Bunkr Operation DELETE failed with: {stdout}")

	def __update_accounts(self):
		"""
		delete any spent and used addresses
		:return: None
		"""
		deletes = []
		for acct in self.wallet:
			if len(get_unspent(acct["address"], self.testnet))==0:
				spent = get_spent(acct["address"], self.testnet)
				confirm = (s["confirmations"] >= 6 for s in spent)
				if len(spent) > 0 and all(confirm):
					deletes.append(acct)
		self.wallet = [acct for acct in self.wallet if acct not in deletes]
		output = [self.header,] + self.wallet
		with open(os.path.join(CURRENT_DIR, f"{self.name}.p"), 'wb') as f:
			pickle.dump(output, f)
		for acct in deletes:
			self.delete(acct)


def new_wallet(punkr, wallet_name, testnet):
	"""
	generates a new bunkrwallet file
	:param punkr: punkr instance
	:param wallet_name: bunkrwallet file name
	:param testnet: flag to enable/disable mainnet vs testnet
	:return: None
	"""
	network = 'BTCTEST' if testnet else 'BTC'
	n_accounts = 5
	wallet_file = [{"NETWORK": network}]
	for i in range(n_accounts):
		priv, pub = gen_EC_keypair()
		address = convert_public_to_address(pub, testnet)
		name = wallet_name+"-"+address
		write_private_key_to_bunkr(punkr, priv, name)
		wallet_file.append({"address": address, "pubkey_hex":pub, "secret_name":name})
	with open(os.path.join(CURRENT_DIR, f"{wallet_name}.p"), 'wb') as f:
		pickle.dump(wallet_file, f)

def write_private_key_to_bunkr(punkr, private_key, name):
	"""
	writes a bitcoin private key to bunkr
	:param punkr: punkr instance
	:param private_key: bitcoin private key
	:param name: bunkr secret name
	:return: None
	"""
	for _ in punkr.batch_commands(
		("create", {"secret_name":name, "secret_type":"ECDSA-SECP256k1"}),
		("write",  {"secret_name": name, "content": "b64 "+ str(base64.b64encode(private_key.to_bytes(ceil(private_key.bit_length() / 8), 'big')), 'utf-8')})
	):
		pass