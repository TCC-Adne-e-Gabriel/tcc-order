from uuid import UUID
import random
from app.models.payment import PaymentMethodEnum, PaymentStatusEnum

class PaymentMockService():
    def mock_payment(self, method): 
        if method == PaymentMethodEnum.credit_card: 
            return random.choice([PaymentStatusEnum.failed, PaymentStatusEnum.paid])
        return PaymentStatusEnum.pending
    
    def bloco(self, n): 
        return ''.join(str(random.randint(0, 9)) for _ in range(n))
    
    def mock_barcode(self):
        return (
            f"{self.bloco(5)}.{self.bloco(5)} "
            f"{self.bloco(5)}.{self.bloco(6)} "
            f"{self.bloco(5)}.{self.bloco(6)} "
            f"{random.randint(1, 9)} {self.bloco(14)}"
        )
