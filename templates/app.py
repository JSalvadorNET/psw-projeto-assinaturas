import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import datetime
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)
        
    def start(self):
        while True:
            print("""
         
            ______                          _           __                       
            / ____/__  ________  ____  _____(_)___ _____/ /___  _____             
            / / __/ _ \/ ___/ _ \/ __ \/ ___/ / __ `/ __  / __ \/ ___/             
            / /_/ /  __/ /  /  __/ / / / /__/ / /_/ / /_/ / /_/ / /                 
            \____/\___/_/   \___/_/ /_/\___/_/\__,_/\__,_/\____/_/                  
            ____/ /__     ____ ___________(_)___  ____ _/ /___  ___________ ______
            / __  / _ \   / __ `/ ___/ ___/ / __ \/ __ `/ __/ / / / ___/ __ `/ ___/
            / /_/ /  __/  / /_/ (__  |__  ) / / / / /_/ / /_/ /_/ / /  / /_/ (__  ) 
            \__,_/\___/   \__,_/____/____/_/_/ /_/\__,_/\__/\__,_/_/   \__,_/____/  
                                                                        
                       Por Julyana Salvador @JSalvadorNET
                                                                            
            """)

            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Remover pagamento
            [6] -> Pagar assinatura
            [7] -> Sair
            ''')

            choice = int(input('Escolha uma opção: '))

            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.delete_payment()
            elif choice == 6:
                self.pay_subscription()  # Chamando a função de pagamento
            else:
                break

    def add_subscription(self):
        company = input('Empresa: ')
        site = input('Site: ')
        date_assignature = datetime.strptime(input('Data de assinatura: '), '%d/%m/%Y')
        value = Decimal(input('Valor: '))

        subscription = Subscription(company=company, site=site, date_assignature=date_assignature, value=value)
        self.subscription_service.create(subscription)
        print('Assinatura adicionada com sucesso.')

    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja excluir')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.company}')

        choice = int(input('Escolha a assinatura: '))
        self.subscription_service.delete(choice)
        print('Assinatura excluída com sucesso.')
        
    def delete_payment(self):
        payments = self.subscription_service.list_all_payments()  
        if not payments:
            print("Nenhum pagamento encontrado para remover.")
            return
        print("Escolha qual pagamento deseja excluir")
        for payment in payments:
            print(f'[{payment.id}] -> {payment.date}')
        choice = int(input("Digite o ID do pagamento a ser removido: "))
        self.subscription_service.delete_payment(choice)

    def pay_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print("Escolha qual assinatura deseja pagar:")

        for i in subscriptions:
            print(f'[{i.id}] -> {i.company}')

        choice = int(input('Escolha a assinatura: '))
        subscription_to_pay = next((sub for sub in subscriptions if sub.id == choice), None)

        if subscription_to_pay:
            self.subscription_service.pay(subscription_to_pay)
            print(f"Pagamento para a assinatura '{subscription_to_pay.company}' realizado com sucesso.")
        else:
            print("Assinatura não encontrada.")

    def total_value(self):
        print(f'Seu valor total mensal em assinaturas: {self.subscription_service.total_value()}')

if __name__ == '__main__':
    UI().start()
