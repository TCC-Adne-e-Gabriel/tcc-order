def greater_than_zero(total): 
    if(total and total <= 0):
        raise ValueError(f'Total value {total} is equal or less than 0')
    return total
