import __init__
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            return subscription
        
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        return results
    
    def list_all_payments(self):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()
        return results

    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()
            
    def delete_payment(self, id):
        with Session(self.engine) as session:
            statement = select(Payments).where(Payments.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()
                              
    def _has_pay(self,results):
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.company==subscription.company)
            results = session.exec(statement).all()
            if self._has_pay(results):
                question = input("Essa conta já foi paga esse mês, deseja pagar novamente? Y ou N: ")
                if not question.upper() == 'Y':
                            return
                        
            pay = Payments(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()        
            
    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        total = 0
        for result in results:
            total += result.value
            
            
        return float(total)

    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        return last_12_months[::-1]

    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            # Seleciona todos os pagamentos
            statement = select(Payments)
            results = session.exec(statement).all()

            # Lista para armazenar valores por mês
            value_for_months = []
            
            # Itera pelos últimos 12 meses
            for month, year in last_12_months:
                # Calcula o valor total para o mês atual
                total_value = sum(
                    float(result.subscription.value)
                    for result in results
                    if result.date.month == month and result.date.year == year and result.subscription is not None
                )
                value_for_months.append(total_value)

        return value_for_months

    def gen_chart(self):
        # Obter os últimos 12 meses
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_months(last_12_months)
        # Obter os rótulos dos meses (nomes dos meses, indo do atual ao mais antigo)
        import calendar
        last_12_months_labels = [
            calendar.month_abbr[month] for month, year in last_12_months
        ]
        # Inverter os valores para garantir que o mês mais recente esteja à esquerda
        last_12_months_labels = last_12_months_labels[::1]
        values_for_months = values_for_months[::1]
        import matplotlib.pyplot as plt
        plt.plot(last_12_months_labels, values_for_months, marker='o')  # Adiciona pontos para clareza
        plt.xlabel("Meses")
        plt.ylabel("Gastos (R$)")
        plt.title("Gastos Mensais em Assinaturas")
        plt.grid(True)  # Adiciona grade para visualização melhor
        plt.show()


"""

PARA ADICIONAR UM PAGAMENTO DE TESTE 

assignatures = ss.list_all()
for i,s in enumerate(assignatures):
    print(f"[{i}] -> {s.company}")
    
x = int(input())
ss.pay(assignatures[x])
"""