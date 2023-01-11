import * as assert from 'assert';
import BIP32Factory from 'bip32';
import * as ecc from 'tiny-secp256k1';
import * as bip39 from 'bip39';
import { payments } from 'bitcoinjs-lib';
import fs from 'fs';
import path from 'path';

const ADDRESS_TO_FIND = 'bc1qk94tpr4538wr2vtraz2kkd9xn2ymrxvzmfkhkj';

const MNEMONIC = 'local panic antenna corn position junior hen supply scrub antique giraffe tuition rally tone discover fetch pride family faint scare soup clay snow dry';

const DERIVE_PATH = {
  PATH_49: "m/49'/0'/0'/0/0", // Starts with 3
  PATH_84: "m/84'/0'/0'/0/0", // Starts with bc
}

const generate_address = (mnemonic: string, passphrase: string, derivePath: string) => {
  const bip32 = BIP32Factory(ecc);

  const seed = bip39.mnemonicToSeedSync(mnemonic, passphrase);
  const root = bip32.fromSeed(seed);

  const address = payments.p2wpkh({ pubkey: root.derivePath(derivePath).publicKey }).address;

  return address;
}


fs.readFile(path.join(__dirname, '..', 'passphrases.txt'), 'utf-8', (err, data) => {
  if (err) throw err;

  const lines = data.split('\n');

  lines.forEach((passphrase, index) => {

    if (index % 100 == 0) {
      fs.writeFile('last_index.txt', `${index}`, () => {
        console.log('Last index updated!');
      });
    }

    const address = generate_address(MNEMONIC, passphrase, DERIVE_PATH.PATH_84);

    console.log(`Decoding ${index} (${passphrase}): ${passphrase}`);

    if (address == ADDRESS_TO_FIND) {
      fs.writeFile('found.txt', passphrase, () => {
        console.log('Written to found.txt');
      });
    }
  });
});
