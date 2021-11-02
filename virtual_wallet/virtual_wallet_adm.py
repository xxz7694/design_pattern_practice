# coding=utf-8
"""
贫血模型的传统开发
"""
import time

from enum import Enum


class VirtualWalletController:
    """
    Controller负责暴露接口
    """
    def __init__(self, virtual_wallet_service):
        self.virtual_wallet_service = virtual_wallet_service

    def get_balance(self, wallet_id):
        """查询余额"""
        self.virtual_wallet_service.get_balance()

    def debit(self, wallet_id, amount):
        """出账"""
        self.virtual_wallet_service.debit()

    def credit(self, wallet_id, amount):
        """入账"""
        self.virtual_wallet_service.credit()

    def transfer(self, wallet_id, to_wallet_id, amount):
        """支付接口"""
        self.virtual_wallet_service.trabsfer()


TransactionType = Enum('TransactionType', ('DEBIT', 'CREDIT', 'TRANSFER'))


class VirtualWalletBo:
    """Service 和 BO 负责核心业务逻辑"""
    def __init__(self, id, create_time, balance):
        self.id = id
        self.create_time = create_time
        self.balance = balance


class VirtualWalletService:
    """Service 和 BO 负责核心业务逻辑"""
    def __init__(self, wallet_repo, transaction_repo):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    def get_virtual_wallet(self, wallet_id):
        """
        获得虚拟钱包的BO
        """
        wallet_entity = self.wallet_repo.get_wallet_entity(wallet_id)
        wallet_bo = convert(wallet_entity)
        return wallet_bo

    def get_balance(self, wallet_id):
        """获得当前钱包的余额"""
        return self.wallet_repo.get_balance(wallet_id)

    def debit(self, wallet_id, amount):
        """出账"""
        wallet_entity = self.wallet_repo.get_wallet_entity(wallet_id)
        balance = wallet_entity.get_balance()
        if balance.compare_to(amount) < 0:
            raise Exception
        transaction_entity = VirtualWalletTransactionEntity()
        transaction_entity.set_amount(amount)
        transaction_entity.set_createtime(time.time())
        transaction_entity.set_type(TransactionType.DEBIT)
        transaction_entity.set_from_wallet_id(wallet_id)
        self.transaction_repo.save_transaction(transaction_entity)
        self.wallet_repo.update_balance(wallet_id, balance.subtract(amount))

    def credit(self, wallet_id, amount):
        """入账"""
        wallet_entity = self.wallet_repo.get_wallet_entity(wallet_id)
        balance = wallet_entity.get_balance()
        transaction_entity = VirtualWalletTransactionEntity()
        transaction_entity.set_amount(amount)
        transaction_entity.set_createtime(time.time())
        transaction_entity.set_type(TransactionType.CREDIT)
        transaction_entity.set_from_wallet_id(wallet_id)
        self.transaction_repo.save_transaction(transaction_entity)
        self.wallet_repo.update_balance(wallet_id, balance.add(amount))

    def transfer(self, from_wallet_id, to_wallet_id, amount):
        transaction_entity = VirtualWalletTransactionEntity()
        transaction_entity.set_amount(amount)
        transaction_entity.set_createtime(time.time())
        transaction_entity.set_type(TransactionType.CREDIT)
        transaction_entity.set_from_wallet_id(from_wallet_id)
        transaction_entity.set_to_wallet_id(to_wallet_id)
        self.transaction_repo.save_transaction(transaction_entity)
        self.debit(from_wallet_id, amount)
        self.credit(to_wallet_id, amount)


class WalletRepo:
    def __init__(self):
        pass


class TransactionRepo:
    def __init__(self):
        pass











