import hashlib
import json

from time import time

class Blockchain(object):
    def __init__(self) -> None:
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None) -> dict: 
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

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:

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


    def proof_of_work(self, last_proof) -> int:
        proof = 0 

        while self.valid_proof(last_proof, proof) is False: 
            proof += 1

        return proof
    
    @staticmethod
    def hash(block) -> str:
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()

    def last_block(self) -> dict:
        return self.chain[-1]

    def valid_proof(last_proof, proof) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:4] == "0000"
    







