from flask import Flask, render_template, request, redirect
from web3 import Web3
import os

app = Flask(__name__)

# Environment variable for Infura Project ID
infura_url = f"https://mainnet.infura.io/v3/{os.getenv('INFURA_PROJECT_ID')}"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Ensure connection is successful
if not web3.is_connected():
    print("Failed to connect to Ethereum node.")
    exit(1)
else:
    print("Connected to Ethereum node.")

# Your contract address and ABI (Application Binary Interface)
contract_address = "0xYourContractAddress"
contract_abi = [
    # Your contract ABI goes here
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/register_pet', methods=['POST'])
def register_pet():
    pet_name = request.form['pet_name']
    # Transaction details
    txn = contract.functions.registerPet(pet_name).buildTransaction({
        'from': web3.eth.accounts[0], # Your account address
        'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0])
    })
    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=os.getenv('PRIVATE_KEY'))
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return redirect('/')

@app.route('/adopt_pet', methods=['POST'])
def adopt_pet():
    pet_id = int(request.form['pet_id'])
    # Transaction details
    txn = contract.functions.adoptPet(pet_id).buildTransaction({
        'from': web3.eth.accounts[0], # Your account address
        'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0])
    })
    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=os.getenv('PRIVATE_KEY'))
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return redirect('/')

@app.route('/follow_up_check', methods=['POST'])
def follow_up_check():
    pet_id = int(request.form['pet_id'])
    # Transaction details
    txn = contract.functions.followUpCheck(pet_id).buildTransaction({
        'from': web3.eth.accounts[0], # Your account address
        'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0])
    })
    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=os.getenv('PRIVATE_KEY'))
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
