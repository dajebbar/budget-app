class Category:
  def __init__(self, cat):
    self.ledger = []
    self.category = cat
  
  def deposit(self, amount, description=''):
    obj = dict(amount=amount, description=description)
    self.ledger.append(obj)
  
  
  def withdraw(self, amount, description=''):
    obj = dict(amount=-amount, description=description)
    if self.check_funds(amount):
      self.ledger.append(obj)
      return True
    return False
    
  def get_balance(self):
    tot = [amount.get('amount') for amount in self.ledger]
    return sum(tot)
  
  def transfer(self, amount, other):
    if self.check_funds(amount):
      self.withdraw(amount, f'Transfer to {other.category}')
      other.deposit(amount, f'Transfer from {self.category}')
      return True
    return False
  

  def check_funds(self, amount):
        return self.get_balance() >= amount
  
  def __str__(self):
    budget = self.category.center(30, '*') + '\n'
    for item in self.ledger:
        budget += f'{item.get("description")[:23]:23}' + f'{item.get("amount"):7.2f}' + '\n'
    budget += f'Total: {self.get_balance():.2f}'
    return budget



def create_spend_chart(categories):
  viz = 'Percentage spent by category\n'
  withdrawals = [-sum([i.get('amount') for i in cat.ledger if i.get('amount') < 0]) for cat in categories]
  with_percents = [round(i / sum(withdrawals) * 100) for i in withdrawals]
  cat_names = [cat.category.lower().title() for cat in categories]
  for i in range(100, -10, -10):
    viz += str(i).rjust(3) + "| "
    for percent in with_percents:
      if percent >= i:
        viz += 'o'+ ' ' * 2
      else:
        viz += ' ' * 3
    viz += "\n"
  
  viz += ' ' * 4 + '-' * (2 * (len(categories) + 1) + 2)
  max_length = len(max(cat_names, key=len))
  cat_names = [i.ljust(max_length) for i in cat_names]

  for i in range(max_length):
        viz += '\n' + ' ' * 5
        for cn in cat_names:
            viz += cn[i] + ' ' * 2

  return viz


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())

clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)

print(create_spend_chart([food, clothing, auto]))