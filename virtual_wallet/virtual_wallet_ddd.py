# coding=utf-8
"""
充血模型的开发模式
"""
import time


class VirtualWallet:
    def __init__(self, pre_allocated_id):
        self.id = pre_allocated_id
        self.create_time = time.time()
        self.balance = 0

    def debit(self, amount):
        if self.balance < amount:
            raise Exception("余额不足")
        self.balance = self.balance - amount

    def credit(self, amount):
        if amount < 0:
            raise Exception("金额不能为负数")
        self.balance = self.balance + amount


class VirtualWalletService:
    def __init__(self, wallet_repo, transaction_repo):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    



