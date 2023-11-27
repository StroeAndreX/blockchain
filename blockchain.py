import hashlib
import json

from time import time
from urllib.parse import urlparse

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None): 
        """
        Create a new Block in the Blockchain
            :param proof: <int> The proof given by the Proof of Work algorithm
            :param previous_hash: (Optional) <str> Hash of previous Block
            :return: <dict> New Block
        """
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        
        return block

    def new_transaction(self, sender, recipient, amount):

        """
         Creates a new transaction to go into the next mined Block
            :param sender: <str> Address of the Sender
            :param recipient: <str> Address of the Recipient
            :param amount: <int> Amount
            :return: <int> The index of the Block that will hold this transaction
        """


        self.current_transactions.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount})
        
        return self.last_block['index'] + 1


    def proof_of_work(self, last_proof):
        proof = 0 

        while self.valid_proof(last_proof, proof) is False: 
            proof += 1

        return proof
    
    def register_node(self, address):
        """
            dd a new node to the list of nodes
            :param address: <str> Address of node. Eg. 'http://192.168.0.5:5050'
            :return: NoneA
        """
        
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    
    @staticmethod
    def hash(block):
        
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:4] == "0000"
        
    @property
    def last_block(self):
        return self.chain[-1]






