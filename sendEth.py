import os
import argparse


def sendTo(wallet: str, address: str, amount: str):
    return """
import {utils, Wallet} from "zksync-web3";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import * as ethers from "ethers";
import { Deployer } from "@matterlabs/hardhat-zksync-deploy";


export default async function (hre: HardhatRuntimeEnvironment) {

  const wallet = new Wallet("%s");
  // Create deployer object and load the artifact of the contract we want to deploy.
  const deployer = new Deployer(hre, wallet);

  const depositAmount = ethers.utils.parseEther("%s");
  const zkBalance = await deployer.zkWallet.getBalance()
    if(zkBalance <= depositAmount) {
      await deployer.zkWallet.deposit({
        to: deployer.zkWallet.address,
        token: utils.ETH_ADDRESS,
        amount: depositAmount.div(100).mul(110)
      });
    }
  let tx = {
    to: "%s",
    value: depositAmount
  }
  const t = await deployer.zkWallet.sendTransaction(tx)
  t.wait()
}
    """ % (wallet, amount, address)


def create_deploy(wallet: str, address: str, amount: str) -> None:
    if "deploy" not in os.listdir():
        os.mkdir("deploy")
    with open(f"deploy/deploy.ts", "w+") as file:
        file.writelines(sendTo(wallet, address, amount))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-wallet", dest="wallet", required=True)
    parser.add_argument("-addressTo", dest="addressTo", required=True)
    parser.add_argument("-amount", dest="amount", required=True)

    args = parser.parse_args()
    create_deploy(args.wallet, args.addressTo, args.amount)

    stream = os.popen('yarn hardhat deploy-zksync')
    output = stream.read()
    print(output)
