from web3 import Web3
from data import zora_mint_contract, zora_url
from module import load_data_from_file

zora_abi = load_data_from_file('zora_abi.json', True)
w3 = Web3(Web3.HTTPProvider(zora_url))
#print(w3.is_connected())
wallet_list = load_data_from_file('wallets.txt')

account = w3.eth.account.from_key(wallet_list[0])
address = account.address
address_bytes = bytes.fromhex(address[2:])
padded_address_hex = '0x' + '00' * (32 - len(address_bytes)) + address[2:]
print(padded_address_hex)

def mint():
    nft_contract = w3.to_checksum_address(zora_mint_contract)
    contract = w3.eth.contract(nft_contract, abi=zora_abi)

    pricenft = w3.to_wei(0.000777, 'ether')
    gasPrice = int(w3.eth.gas_price * 1.1)

    mintnft = contract.functions.mint(
        '0x169d9147dfc9409afa4e558df2c9abeebc020182',
        1,
        1,
        padded_address_hex,

    ).build_transaction({
        'chainId':w3.eth.chain_id,
        'nonce': w3.eth.get_transaction_count(address),
        'gasPrice': gasPrice,
        'value': pricenft,
        'from': address,
    })
    sign_tx = w3.eth.account.sign_transaction(mintnft, wallet_list[0])
    tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction).hex()
    print(f'Mint done with HEX {tx_hash}')

mint()
